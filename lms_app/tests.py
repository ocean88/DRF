from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from lms_app.models import Course, Lesson, Subscription


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@example.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description"
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        url = reverse("course:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson_data = response.json()
        print(lesson_data)

    def test_lesson_create(self):
        url = reverse("course:lesson-create")
        data = {
            "title": "New Test Lesson",
            "description": "New Test Lesson Description",
            "course": self.course.pk,
            "video_url": "https://www.youtube.com/watch?v=M9btPMhM4kQ",
        }
        response = self.client.post(url, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().title, "New Test Lesson")

    def test_lesson_retrieve(self):
        url = reverse("course:lesson-view", args=[self.lesson.pk])
        response = self.client.get(url)
        print(
            f"URL: {url}, Response status code: {response.status_code}, Response data: {response.data}"
        )  # Отладочный вывод
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), self.lesson.title)

    def test_lesson_update(self):
        url = reverse("course:lesson-update", args=[self.lesson.pk])
        data = {
            "title": "Updated Test Lesson",
            "description": "Updated Test Lesson Description",
            "course": self.course.pk,
            "video_url": "https://www.youtube.com/watch?v=M9btPMhM4kQ",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Test Lesson")
        self.assertEqual(self.lesson.description, "Updated Test Lesson Description")

    def test_lesson_delete(self):
        url = reverse("course:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class ManageSubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@example.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description"
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("course:manage-subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
