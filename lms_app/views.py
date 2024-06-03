from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from lms_app.models import Course, Lesson
from lms_app.paginators import CustomPageNumberPagination
from lms_app.permissions import IsOwnerOrStaff, IsOwner, IsModerOrReadOnly, IsModer
from lms_app.serializer import (
    LessonSerializer,
    CourseWithLessonsSerializer,
    PaymentSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from lms_app.models import Subscription, Course
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseWithLessonsSerializer
    queryset = Course.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="moder").exists():
                return Course.objects.all()
            else:
                return Course.objects.filter(owner=user)
        else:
            return Course.objects.none()

    @swagger_auto_schema(
        operation_description="Создать новый курс",
        request_body=CourseWithLessonsSerializer,
        responses={201: CourseWithLessonsSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить информацию о курсе",
        responses={200: CourseWithLessonsSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить информацию о курсе",
        request_body=CourseWithLessonsSerializer,
        responses={200: CourseWithLessonsSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить информацию о курсе",
        request_body=CourseWithLessonsSerializer,
        responses={200: CourseWithLessonsSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить курс", responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить список курсов",
        responses={200: CourseWithLessonsSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = (IsOwner | IsModer,)
        elif self.action == "retrieve":
            self.permission_classes = (IsAuthenticated,)
        elif self.action == "list":
            self.permission_classes = (IsAuthenticated,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer | IsOwner,
            )
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModer, IsAuthenticated]
    """Создание урока"""

    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_description="Получить список уроков",
        responses={200: LessonSerializer(many=True)},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    @swagger_auto_schema(
        operation_description="Просмотр урока",
        responses={200: LessonSerializer(many=True)},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    @swagger_auto_schema(
        operation_description="Обновление урока",
        responses={200: LessonSerializer(many=True)},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_description="Удаление урока",
        responses={200: LessonSerializer(many=True)},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["payment_date", "course", "lesson", "amount", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]  # Default ordering

    @swagger_auto_schema(
        operation_description="Получить список платежей",
        responses={200: PaymentSerializer(many=True)},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)


class ManageSubscription(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Управление подпиской",
        responses={200: LessonSerializer(many=True)},
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        # Проверка существования подписки
        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )

        if created:
            message = "Подписка добавлена"
            status_code = status.HTTP_201_CREATED
        else:
            subscription.delete()
            message = "Подписка удалена"
            status_code = status.HTTP_204_NO_CONTENT

        return Response({"message": message}, status=status_code)
