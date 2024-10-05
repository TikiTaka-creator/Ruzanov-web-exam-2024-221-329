from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'количество зарегистрированных пользователей'

    def handle(self, *args, **options):
        user_count = User.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Всего зарегистрировано: {user_count}'))
