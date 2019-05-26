from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Exam, Task


class ExamTests(APITestCase):
    def setUp(self):
        u1 = User.objects.create(username="user1", password="Password1")
        u2 = User.objects.create(username="user2", password="Password1")
        Exam.objects.create(name="Exam", examiner=u1, examinee=u1)
        Exam.objects.create(name="Exam 2", examiner=u1, examinee=u2)

    def test_create_exam(self):
        """Ensure that exams can be created"""
        self.client.force_authenticate(user=User.objects.get(pk=2))
        url = reverse("exam-list")
        data = {"name": "Exam name", "examiner": 1, "examinee": 2}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_other_user_permissions(self):
        """Ensure that users that are not associated with exams can only see them and nothing else."""
        self.client.force_authenticate(user=User.objects.get(pk=2))
        # GET is allowed
        url = reverse("exam-detail", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The rest is not allowed
        data = {"name": "You shall not pass!", "examiner": 2, "examinee": 2}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        url = reverse("exam-archivize", kwargs={"pk": 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_examinees_cannot_edit_exam(self):
        """Ensure that examinees cannot edit exams assigned to them"""
        self.client.force_authenticate(user=User.objects.get(pk=2))
        url = reverse("exam-detail", kwargs={"pk": 2})
        data = {"name": "You shall not pass!"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_examiners_can_edit_exam(self):
        """Ensure that examiners can edit exams assigned by them"""
        self.client.force_authenticate(user=User.objects.get(pk=1))
        url = reverse("exam-detail", kwargs={"pk": 2})
        data = {"name": "You shall pass!"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_examiners_can_delete_exam(self):
        """Ensure that examiners can delete exams assigned by them"""
        self.client.force_authenticate(user=User.objects.get(pk=1))
        url = reverse("exam-detail", kwargs={"pk": 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_examiners_can_archivize_exam(self):
        """Ensure that examiners can archivize and dearchivize exams assigned by them"""
        self.client.force_authenticate(user=User.objects.get(pk=1))
        url = reverse("exam-archivize", kwargs={"pk": 2})
        # Archivize
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Exam.objects.get(pk=2).archived_on)
        # Dearchivize
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(Exam.objects.get(pk=2).archived_on)

    def test_examiners_can_give_grade(self):
        """Ensure that examiners can give grades for exams."""
        self.client.force_authenticate(user=User.objects.get(pk=1))
        url = reverse("exam-detail", kwargs={"pk": 2})
        data = {"grade": 5}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Exam.objects.get(pk=2).grade, "5")


class TaskTests(APITestCase):
    def setUp(self):
        u1 = User.objects.create(username="user1", password="Password1")
        u2 = User.objects.create(username="user2", password="Password1")
        e1 = Exam.objects.create(name="Exam", examiner=u1, examinee=u1)
        e2 = Exam.objects.create(name="Exam 2", examiner=u1, examinee=u2)
        e3 = Exam.objects.create(
            name="Exam 3", examiner=u1, examinee=u2, archived_on=timezone.now()
        )
        Task.objects.create(exam=e1, question="Is this the real life?")
        Task.objects.create(exam=e1, question="Is this just fantasy?")
        Task.objects.create(exam=e2, question="Caught in a landslide")
        Task.objects.create(exam=e3, question="No escape from reality")

    def test_only_examiners_create_tasks(self):
        """
        Ensure that only examiners can create tasks for their exams.
        """
        self.client.force_authenticate(user=User.objects.get(pk=2))
        url = reverse("task-list")
        data = {"exam": 2, "question": "Open your eyes"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_examiners_can_create_tasks(self):
        """Ensure that examiners can create tasks"""
        self.client.force_authenticate(user=User.objects.get(pk=1))
        url = reverse("task-list")
        data = {"exam": 2, "question": "Look up to the skies and see"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_examinees_cannot_edit_tasks(self):
        """Ensure that examinees cannot edit any other field than answer"""
        self.client.force_authenticate(user=User.objects.get(pk=2))
        url = reverse("task-detail", kwargs={"pk": 2})
        data = {"exam": 2, "question": "I'm just a poor boy, I need no sympathy"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_examiners_can_edit_tasks(self):
        """Ensure that examinees cannot edit any other field than answer"""
        self.client.force_authenticate(user=User.objects.get(pk=1))
        url = reverse("task-detail", kwargs={"pk": 2})
        data = {"exam": 2, "question": "Because I'm easy come, easy go"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_examinees_can_add_answers(self):
        """Ensure that examinees can add answers to tasks"""
        self.client.force_authenticate(user=User.objects.get(pk=2))
        url = reverse("task-detail", kwargs={"pk": 3})
        data = {"answer": "A little high, little low"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tasks_from_archivized_exams(self):
        """Ensure that tasks from archivized exams cannot be edited"""
        self.client.force_authenticate(user=User.objects.get(pk=2))
        url = reverse("task-detail", kwargs={"pk": 4})
        data = {"answer": "Anyway the wind blows, doesn't really matter to me, to me"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
