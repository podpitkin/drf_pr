from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", email="owner@test.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@test.com", password="testpass123"
        )
        self.moderator = User.objects.create_user(
            username="moderator", email="moderator@test.com", password="testpass123"
        )
        self.moderator_group = Group.objects.create(name="Модераторы")
        self.moderator.groups.add(self.moderator_group)

        # Курсы
        self.owner_course = Course.objects.create(
            owner=self.owner, name="Курс владельца"
        )
        self.other_course = Course.objects.create(
            owner=self.other_user, name="Чужой курс"
        )

        # Уроки
        self.owner_lesson = Lesson.objects.create(
            owner=self.owner,
            name="Урок владельца",
            link="https://www.youtube.com/watch?v=abc123",
            course=self.owner_course,
        )
        self.other_lesson = Lesson.objects.create(
            owner=self.other_user,
            name="Чужой урок",
            link="https://youtube.com/watch?v=xyz789",
            course=self.other_course,
        )

        # URL-адреса
        self.list_create_url = reverse("materials:lessons-list-create")
        self.owner_detail_url = reverse(
            "materials:lessons-retrieve-update-delete",
            args=[self.owner_lesson.pk],
        )
        self.other_detail_url = reverse(
            "materials:lessons-retrieve-update-delete",
            args=[self.other_lesson.pk],
        )

    # ---------- CREATE ----------

    def test_unauthenticated_user_cannot_create_lesson(self):
        """ Неавторизованный пользователь не может создать урок """
        response = self.client.post(
            self.list_create_url,
            data={
                "name": "Новый урок",
                "link": "https://www.youtube.com/watch?v=new123",
                "course": self.owner_course.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_moderator_cannot_create_lesson(self):
        """ Модератор не может создавать уроки """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(
            self.list_create_url,
            data={
                "name": "Новый урок",
                "link": "https://www.youtube.com/watch?v=new123",
                "course": self.owner_course.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_owner_can_create_lesson(self):
        """ Авторизованный владелец может создать урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_create_url,
            data={
                "name": "Новый урок",
                "link": "https://www.youtube.com/watch?v=new123",
                "course": self.owner_course.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lesson = Lesson.objects.get(pk=response.data["id"])
        self.assertEqual(lesson.owner, self.owner)
        self.assertEqual(lesson.name, "Новый урок")
        self.assertEqual(lesson.course, self.owner_course)

    def test_create_lesson_rejects_non_youtube_link(self):
        """ Нельзя создать урок со ссылкой не на youtube.com """
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_create_url,
            data={
                "name": "Новый урок",
                "link": "https://vimeo.com/video/12345",
                "course": self.owner_course.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 2)

    # ---------- LIST ----------

    def test_unauthenticated_user_cannot_list_lessons(self):
        """ Неавторизованный пользователь не может получить список уроков """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_sees_only_own_lessons(self):
        """ Обычный пользователь видит только свои уроки """
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], self.owner_lesson.pk)

    def test_moderator_sees_all_lessons(self):
        """ Модератор видит все уроки """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    # ---------- RETRIEVE ----------

    def test_unauthenticated_user_cannot_retrieve_lesson(self):
        """ Неавторизованный пользователь не может получить урок """
        response = self.client.get(self.owner_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_retrieve_own_lesson(self):
        """ Владелец может получить свой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.owner_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.owner_lesson.pk)

    def test_owner_cannot_retrieve_foreign_lesson(self):
        """ владелец не может получить чужой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_moderator_can_retrieve_any_lesson(self):
        """ Модератор может получить любой урок """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.other_lesson.pk)

    # ---------- UPDATE ----------

    def test_owner_can_update_own_lesson(self):
        """ Владелец может изменить свой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.owner_detail_url,
            data={"name": "Обновлённое название"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.owner_lesson.refresh_from_db()
        self.assertEqual(self.owner_lesson.name, "Обновлённое название")

    def test_owner_cannot_update_foreign_lesson(self):
        """ Владелец не может изменить чужой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.other_detail_url,
            data={"name": "Взломанный урок"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_moderator_can_update_any_lesson(self):
        """ Модератор может изменить любой урок """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(
            self.other_detail_url,
            data={"name": "Отредактировано модератором"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.other_lesson.refresh_from_db()
        self.assertEqual(self.other_lesson.name, "Отредактировано модератором")

    # ---------- DELETE ----------

    def test_owner_can_delete_own_lesson(self):
        """ Владелец может удалить свой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.owner_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Lesson.objects.filter(pk=self.owner_lesson.pk).exists()
        )

    def test_owner_cannot_delete_foreign_lesson(self):
        """ Владелец не может удалить чужой урок """
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(
            Lesson.objects.filter(pk=self.other_lesson.pk).exists()
        )

    def test_moderator_cannot_delete_lesson(self):
        """ Модератор не может удалять уроки """
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.owner_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Lesson.objects.filter(pk=self.owner_lesson.pk).exists()
        )


class SubscriptionTestCase(APITestCase):
    """ Тесты функционала подписки на обновления курса """

    def setUp(self):
        self.user = User.objects.create_user(
            username="subscriber",
            email="subscriber@test.com",
            password="testpass123",
        )
        self.course = Course.objects.create(
            owner=self.user, name="Курс для подписки"
        )
        self.url = reverse("materials:subscription")

    def test_unauthenticated_user_cannot_subscribe(self):
        """ Неавторизованный пользователь не может управлять подпиской """
        response = self.client.post(
            self.url, data={"course_id": self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user, course=self.course
            ).exists()
        )

    def test_subscribe_to_course(self):
        """ Пользователь может подписаться на обновления курса """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, data={"course_id": self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user, course=self.course
            ).exists()
        )

    def test_subscribe_twice_unsubscribes(self):
        """ Повторный POST удаляет существующую подписку """
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, data={"course_id": self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user, course=self.course
            ).exists()
        )

    def test_subscribe_to_nonexistent_course_returns_404(self):
        """ Подписка на несуществующий курс возвращает 404 """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url, data={"course_id": 999999}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)