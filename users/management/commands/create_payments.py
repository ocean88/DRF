from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms_app.models import Course, Lesson
from users.models import Payment
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates sample course, lesson, and payment records'

    def handle(self, *args, **kwargs):
        # Создаем пользователя
        user = User.objects.create(email='user@example.com', password='password')

        # Создаем курс
        course = Course.objects.create(title='Sample Course', description='Description for Sample Course')

        # Создаем урок для курса
        lesson = Lesson.objects.create(title='Sample Lesson', description='Description for Sample Lesson', course=course)

        # Создаем платежи
        Payment.objects.create(user=user, payment_date=date.today(), course=course, amount=50.00, payment_method='cash')
        Payment.objects.create(user=user, payment_date=date.today(), lesson=lesson, amount=30.00, payment_method='transfer')

        self.stdout.write(self.style.SUCCESS('Sample course, lesson, and payment records created successfully'))