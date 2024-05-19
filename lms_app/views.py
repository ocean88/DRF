from rest_framework import viewsets, generics
from lms_app.models import Course, Lesson
from lms_app.serializer import CourseSerializer, LessonSerializer, CourseWithLessonsSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from users.models import Payment
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseWithLessonsSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_date', 'course', 'lesson', 'amount', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']  # Default ordering