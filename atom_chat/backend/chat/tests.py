from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Channel, Message


User = get_user_model()


class ChatAPITestCase(APITestCase):

    def setUp(self):
        """
        Создаем начальные данные
        """
        # Создаем модератора
        self.moderator = User.objects.create_user(username="moderator", email="moderator@test.com", password="password",
                                                  is_moderator=True)
        self.user = User.objects.create_user(username="admin", email="admin@test.com", password="password")
        self.user_2 = User.objects.create_user(username="user2", email="user2@test.com", password="password2")

        # Создаем клиент для работы с API
        self.client = APIClient()

    def test_user_registration(self):
        """
        Тестирование регистрации нового пользователя.
        """
        data = {
            "username": "new_user",
            "email": "new_user@test.com",
            "password": "password123"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Уведомление", response.data)

    def test_user_login(self):
        """
        Тестирование получения JWT токена.
        """
        data = {"username": "user2", "password": "password2"}
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_channel_creation(self):
        """
        Тестирование создания канала модератором.
        """
        self.client.force_authenticate(user=self.moderator)

        data = {"name": "Test_Channel", "description": "This is a test channel"}
        response = self.client.post("/api/channels/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test_Channel")

    def test_channel_update(self):
        """
        Тестирование обновления канала модератором.
        """
        # Создаем канал
        channel = Channel.objects.create(name="Old_Channel", description="Old_description")

        # Авторизация модератора
        self.client.force_authenticate(user=self.moderator)

        data = {"name": "Updated_Channel", "description": "Updated_description"}
        response = self.client.patch(f"/api/channels/update/{channel.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated_Channel")

    def test_channel_delete(self):
        """
        Тестирование удаления канала модератором.
        """
        # Создаем канал
        channel = Channel.objects.create(name="Channel_to_Delete", description="To_be_deleted")

        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(f"/api/channels/delete-by-id/{channel.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Уведомление", response.data)

    def test_get_users_list(self):
        """
        Тестирование просмотра списка пользователей модератором.
        """
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Должно быть минимум 1 пользователь (созданный в setUp)

    def test_message_history(self):
        """
        Тестирование получения истории сообщений в канале.
        """
        # Создаем канал
        channel = Channel.objects.create(name="Message_History_Test")

        # Создаем сообщения
        Message.objects.create(channel=channel, user=self.user, content="Test message 1")
        Message.objects.create(channel=channel, user=self.user, content="Test message 2")

        # Авторизация обычного пользователя
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/channels/{channel.id}/history/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def tearDown(self):
        """
        Очистка данных после каждого теста.
        """
        User.objects.all().delete()
        Channel.objects.all().delete()
        Message.objects.all().delete()
