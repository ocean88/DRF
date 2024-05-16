from django.db import models

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100)
    preview = models.ImageField(upload_to='previews/', verbose_name='Превью', help_text='Загрузите превью', **NULLABLE)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/', verbose_name='Превью', help_text='Загрузите превью', **NULLABLE)
    video_url = models.URLField(**NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'