from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email='sample@example.com')
        user.set_password('123qwe')
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
