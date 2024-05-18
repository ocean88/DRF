from lms_app.apps import LmsAppConfig
from rest_framework.routers import DefaultRouter
from django.urls import path
from lms_app.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = LmsAppConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
urlpatterns = [
    path(
     'lesson/create/',
     LessonCreateAPIView.as_view(),
     name='lesson-create'
    ),
    path(
     'lessons/',
     LessonListAPIView.as_view(),
     name='lesson-list'
    ),
    path(
     'lesson/<int:pk>/',
     LessonRetrieveAPIView.as_view(),
     name='lesson-view'
    ),
    path(
     'lesson/<int:pk>/update/',
     LessonUpdateAPIView.as_view(),
     name='lesson-update'
    ),
    path(
     'lesson/<int:pk>/delete/',
     LessonDestroyAPIView.as_view(),
     name='lesson-delete'
    ),
              ] + router.urls
