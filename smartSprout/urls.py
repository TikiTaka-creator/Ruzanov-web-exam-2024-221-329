from django.contrib import admin
from django.urls import path,include
from myapp import views

from myapp.views import CustomLoginView
from myapp.views import SignUpView
from myapp.views import book_detail
from myapp.views import delete_book
from myapp.views import add_book
from myapp.views import edit_book
from myapp.views import add_review

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include




urlpatterns = [
    path('', views.home, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('login/', include('social_django.urls', namespace='social')), 
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('delete-book/<int:book_id>/',delete_book, name='delete-book'),
    path('add-book/',add_book, name='book-add'),
    path('edit-book/<int:book_id>/',edit_book, name='book-edit'),
    path('add_review/<int:book_id>',add_review, name='add-review'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
