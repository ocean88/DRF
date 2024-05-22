from rest_framework import viewsets, generics
from lms_app.models import Course, Lesson
from lms_app.permissions import IsOwnerOrStaff, IsOwner, IsModerOrReadOnly, IsModer
from lms_app.serializer import LessonSerializer, CourseWithLessonsSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseWithLessonsSerializer
    queryset = Course.objects.all()
    permission_classes = (~IsModer,)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsAuthenticated,)
        elif self.action == 'list':
            self.permission_classes = (IsAuthenticated,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerOrReadOnly, IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_date', 'course', 'lesson', 'amount', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']  # Default ordering