from django.db import models
from django.contrib.auth.models import User
import hashlib
import mimetypes


class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    def __str__(self):
        return self.name 



class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='profiles')

    def __str__(self):
        return self.user.username 

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Cover(models.Model):
    cover = models.ImageField(upload_to='book_covers/', default='book_covers/base.jpg')
    mime_type = models.CharField(max_length=50)
    md5_hash = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        # Вычисляем MIME-тип и MD5-хеш перед сохранением
        if self.cover:
            mime_type, _ = mimetypes.guess_type(self.cover.path)
            self.mime_type = mime_type if mime_type else 'application/octet-stream'
            self.md5_hash = hashlib.md5(self.cover.file.read()).hexdigest()
            self.cover.file.seek(0)  # Сбросим курсор, чтобы можно было прочитать файл позже
        super().save(*args, **kwargs)

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name 

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveSmallIntegerField()
    publisher = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    pages = models.PositiveIntegerField()
    cover = models.ForeignKey(Cover, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title 


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


