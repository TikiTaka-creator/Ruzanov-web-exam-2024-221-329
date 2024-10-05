from django.contrib import admin
from myapp.models import (
    Profile,
    Book,
    Review,
    Role,
    Cover,
    Genre
)


admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Role)
admin.site.register(Cover)
admin.site.register(Genre)


