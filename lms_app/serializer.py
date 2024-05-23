from rest_framework import serializers
from lms_app.models import Course, Lesson
from users.models import Payment
from django.core.exceptions import ObjectDoesNotExist


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        if hasattr(obj, 'lessons'):
            return obj.lessons.count()
        else:
            # Логика для случаев, когда у пользователя нет доступа к атрибуту 'lessons'
            return 0  # Или другое значение по умолчанию

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lesson_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'