from django import forms
from .models import Genre
from .models import Book
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class BookForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].initial = ''
    class Meta:
        model = Book
        fields = ['title', 'description', 'year', 'pages', 'publisher', 'author', 'genres']

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Удовлетворительно'),
        (2, 'Неудовлетворительно'),
        (1, 'Плохо'),
        (0, 'Ужасно')
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Оценка', widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-4 py-2 w-full'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'border border-gray-300 rounded px-4 py-2 w-full'}), label='Текст рецензии')

    class Meta:
        model = Review
        fields = ['rating', 'text']

class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'shadow appearance-none border-2 border-blue-500 rounded w-full px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'shadow appearance-none border-2 border-blue-500 rounded w-full px-3 mb-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
