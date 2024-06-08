from django.utils import timezone
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from lms_app.models import Course, Subscription
from users.models import User


@shared_task
def send_course_update_email(course_id, created):
    """Отправлять письма всем подписчикам курса."""
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    subject = "Новый курс создан" if created else "Курс обновлен"
    message = f'Курс "{course.title}" был {"создан" if created else "обновлен"}.'

    for subscription in subscribers:
        user = subscription.user
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def send_lesson_update_email(course_id, created):
    """Отправлять письма всем подписчикам о новом уроке курса."""
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    subject = "Новый урок создан" if created else "Урок добавлен"
    message = f'Урок "{course.title}" был {"создан" if created else "обновлен"}.'

    for subscription in subscribers:
        user = subscription.user
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def check_inactive_users():
    timer = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=timer, is_active=True, is_staff=False, is_superuser=False)

    for user in inactive_users:
        user.is_active = False
        user.save()
