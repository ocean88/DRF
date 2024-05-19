from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from lms_app.models import Course, Lesson

# Create your models here.

NULLABLE = {'blank': True, 'null': True}
PAYMENT_METHOD_CHOICES = [
    ('cash', 'Наличные'),
    ('transfer', 'Перевод на счет'),
]


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', help_text='Загрузите аватар', **NULLABLE)
    phone = PhoneNumberField(verbose_name="Номер телефона",**NULLABLE)
    city = models.CharField(max_length=100, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f" Оплата{self.id} - Пользователь: {self.user}, Сумма: {self.amount}, метод оплаты: {self.get_payment_method_display()}"