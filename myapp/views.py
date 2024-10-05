from django.shortcuts import render, redirect,get_object_or_404
from .models import Profile,Book,Review,Cover
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Avg,Count
from django.core.paginator import Paginator
from django.conf import settings
from bleach import clean

import os

from .forms import UserRegistrationForm,UserLoginForm,BookForm,ReviewForm

from rest_framework.pagination import PageNumberPagination
from django.utils.crypto import get_random_string
from hashlib import md5



class SignUpView(generic.CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


@login_required
def home(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    try:
        books = Book.objects.annotate(
        average_rating=Avg('review__rating'),  # Assuming `rating` is a field in the Review model
        review_count=Count('review')
        ).order_by('-year')  # Sorting by year (newest first)
        
        paginator = Paginator(books, 6)  # 6 books per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'profile':profile,
            'page_obj':page_obj
        }
        return render(request, 'index.html', context)
    except:
        return redirect('/')

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(book=book, user=request.user).first()

    return render(request, 'book_detail.html', {'book': book, 'user_review': user_review})

def delete_book(request, book_id):
    if request.method == 'DELETE':
        book = get_object_or_404(Book, id=book_id)

        # Удаляем файл обложки, если он существует
        if book.cover:
            cover_path = os.path.join(settings.MEDIA_ROOT, str(book.cover))  # Здесь предполагается, что путь к файлу обложки хранится в поле cover
            if os.path.isfile(cover_path):
                os.remove(cover_path)

        book.delete()  # Удаляем книгу
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # Убедитесь, что обработка файла добавлена
        if form.is_valid():
            # Получаем данные о книге
            book = form.save(commit=False)

            # Обработка загрузки файла обложки
            cover_file = request.FILES.get('cover')
            if cover_file:
                # Генерация хеша и пути для хранения файла
                file_hash = md5(cover_file.read()).hexdigest()
                cover_file.seek(0)  # Вернем указатель в начало файла
                book_cover = Cover.objects.filter(md5_hash=file_hash).first()

                if book_cover is None:
                    book_cover = Cover(md5_hash=file_hash)
                    book_cover.save()

                    # Генерация пути для сохранения файла в папке 'myapp/book_covers'
                    cover_file_name = f'{book_cover.id}_{get_random_string(10)}.jpg'
                    cover_file_path = os.path.join('myapp', 'book_covers', cover_file_name)

                    # Сохранение файла в 'myapp/book_covers'
                    with open(cover_file_path, 'wb+') as destination:
                        for chunk in cover_file.chunks():
                            destination.write(chunk)

                    # Сохранение пути к файлу в модели обложки
                    book_cover.cover = cover_file_path
                    book_cover.save()

                book.cover = book_cover

            # Сохранение данных книги
            book.save()

            form.save_m2m()
            return redirect('book_detail', book.id)
        else:
            return render(request, 'add_book.html', {'form': form, 'error': 'Ошибка при сохранении данных. Проверьте корректность введённых данных.'})
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # Получаем данные о книге
            book = form.save(commit=False)

            # Обработка загрузки файла обложки
            cover_file = request.FILES.get('cover')
            if cover_file:
                # Генерация хеша и пути для хранения файла
                file_hash = md5(cover_file.read()).hexdigest()
                cover_file.seek(0)  # Вернем указатель в начало файла
                book_cover = Cover.objects.filter(md5_hash=file_hash).first()

                if book_cover is None:
                    book_cover = Cover(md5_hash=file_hash)
                    book_cover.save()

                    # Генерация пути для сохранения файла в папке 'myapp/book_covers'
                    cover_file_name = f'{book_cover.id}_{get_random_string(10)}.jpg'
                    cover_file_path = os.path.join('myapp', 'book_covers', cover_file_name)

                    # Сохранение файла в 'myapp/book_covers'
                    with open(cover_file_path, 'wb+') as destination:
                        for chunk in cover_file.chunks():
                            destination.write(chunk)

                    # Сохранение пути к файлу в модели обложки
                    book_cover.cover = cover_file_path
                    book_cover.save()

                # Устанавливаем новую обложку для книги
                book.cover = book_cover

            # Сохранение данных книги
            book.save()
            form.save_m2m()
            return redirect('book_detail', book.id)
        else:
            return render(request, 'edit_book.html', {'form': form, 'error': 'Ошибка при сохранении данных. Проверьте корректность введённых данных.'})
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if Review.objects.filter(book=book, user=request.user).exists():
        return redirect('book_detail', book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            # Санация текста рецензии
            review.text = clean(form.cleaned_data['text'], tags=[], strip=True)
            review.save()
            return redirect('book_detail', book_id)
        else:
            return render(request, 'add_review.html', {'form': form, 'error': 'Ошибка при сохранении рецензии. Проверьте введённые данные.'})
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'book': book})