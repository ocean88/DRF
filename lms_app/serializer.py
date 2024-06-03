from rest_framework import serializers
from lms_app.models import Course, Lesson, Subscription
from lms_app.validators import TitleValidator
from users.models import Payment
from lms_app.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(validators=[validate_video_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseWithLessonsSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        if hasattr(obj, "lessons"):
            return obj.lessons.count()
        else:
            # Логика для случаев, когда у пользователя нет доступа к атрибуту 'lessons'
            return 0  # Или другое значение по умолчанию

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "lesson_count",
            "lessons",
            "is_subscribed",
        ]
        validators = [
            TitleValidator(field="title"),
            serializers.UniqueTogetherValidator(
                queryset=Course.objects.all(),
                fields=["title", "description"],
            ),
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["user", "course"]
