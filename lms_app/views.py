from django.contrib.auth.models import AnonymousUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from lms_app.models import Course, Lesson, Subscription
from lms_app.paginators import CustomPageNumberPagination
from lms_app.permissions import IsOwnerOrStaff, IsOwner, IsModerOrReadOnly, IsModer
from lms_app.serializer import LessonSerializer, CourseWithLessonsSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from lms_app.tasks import send_course_update_email, send_lesson_update_email


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
        response = super().create(request, *args, **kwargs)
        course_id = response.data['id']
        send_course_update_email.delay(course_id, created=True)
        return response

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
        response = super().update(request, *args, **kwargs)
        course_id = kwargs['pk']
        send_course_update_email.delay(course_id, created=False)
        print('курс обновлен')
        return response

    @swagger_auto_schema(
        operation_description="Частично обновить информацию о курсе",
        request_body=CourseWithLessonsSerializer,
        responses={200: CourseWithLessonsSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        course_id = kwargs['pk']
        send_course_update_email.delay(course_id, created=False)
        return response

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
        new_course = serializer.save(owner=self.request.user)
        new_course.save()
        send_course_update_email.delay(new_course.id, created=True)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModer]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsOwner | IsModer]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, (~IsModer | IsOwner)]
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
        new_lesson = serializer.save(owner=self.request.user)
        course_id = new_lesson.course_id
        send_lesson_update_email.delay(course_id, created=True)


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
        if getattr(self, 'swagger_fake_view', False):
            return Lesson.objects.none()  # Return an empty queryset for schema generation
        return super().get_queryset()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    @swagger_auto_schema(
        operation_description="Просмотр урока",
        responses={200: LessonSerializer},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        if getattr(self, 'swagger_fake_view', False):
            return Lesson.objects.none()  # Return an empty queryset for schema generation
        if isinstance(self.request.user, AnonymousUser):
            return Lesson.objects.none()  # Optionally handle AnonymousUser cases separately
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    @swagger_auto_schema(
        operation_description="Обновление урока",
        request_body=LessonSerializer,
        responses={200: LessonSerializer},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        if getattr(self, 'swagger_fake_view', False):
            return Lesson.objects.none()
        if isinstance(self.request.user, AnonymousUser):
            return Lesson.objects.none()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        updated_lesson = serializer.save()
        course_id = updated_lesson.course_id
        send_lesson_update_email.delay(course_id, created=False)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    @swagger_auto_schema(
        operation_description="Удаление урока",
        responses={204: "No Content"},
    )
    def get_queryset(self):
        if self.request.user.groups.filter(name="moder").exists():
            return Lesson.objects.all()
        if getattr(self, 'swagger_fake_view', False):
            return Lesson.objects.none()
        if isinstance(self.request.user, AnonymousUser):
            return Lesson.objects.none()
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
        if getattr(self, 'swagger_fake_view', False):
            return Payment.objects.none()  # Return an empty queryset for schema generation
        return super().get_queryset()


class ManageSubscription(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Управление подпиской",
        responses={200: openapi.Response('Подписка добавлена или удалена')},
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
