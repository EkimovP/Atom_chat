import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from chat import models

User = get_user_model()

class Command(BaseCommand):
    help = "Создание тестовых данных для приложения Chat"

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_channels()
        self.create_messages()
        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы."))

    # Создание пользователей
    def create_users(self):
        self.stdout.write("Создаём тестовых пользователей...")
        user_data = [
            {"username": "user11", "email": "user11@example.com", "password": "password11", "is_moderator": False},
            {"username": "user12", "email": "user12@example.com", "password": "password12", "is_blocked": True},
            {"username": "user13", "email": "user13@example.com", "password": "password13"},
            {"username": "user14", "email": "user14@example.com", "password": "password14", "is_moderator": False,
             "is_blocked": True},
            {"username": "moderator11", "email": "moderator11@example.com", "password": "moderatorpassword11",
             "is_moderator": True, "is_staff": True},
            {"username": "moderator12", "email": "moderator12@example.com", "password": "moderatorpassword12",
             "is_moderator": True, "is_staff": True},
        ]
        for data in user_data:
            user, created = User.objects.get_or_create(username=data['username'], defaults=data)
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f"Пользователь {data['username']} создан.")
            else:
                self.stdout.write(f"Пользователь {data['username']} уже существует.")

    # Создание каналов
    def create_channels(self):
        self.stdout.write("Создаём тестовые каналы...")
        channel_data = [
            {"name": "general", "description": "Общий канал для общения."},
            {"name": "random", "description": "Случайные обсуждения."},
            {"name": "tech", "description": "Технический канал."},
        ]
        for data in channel_data:
            channel, created = models.Channel.objects.get_or_create(name=data['name'], defaults=data)
            if created:
                self.stdout.write(f"Канал {data['name']} создан.")
            else:
                self.stdout.write(f"Канал {data['name']} уже существует.")

    # Создание сообщений
    def create_messages(self):
        self.stdout.write("Создаём тестовые сообщения...")
        users = User.objects.all()
        channels = models.Channel.objects.all()
        if not users.exists() or not channels.exists():
            self.stdout.write("Недостаточно данных для создания сообщений.")
            return

        for channel in channels:
            for _ in range(10):  # Создаём 10 сообщений на канал
                user = random.choice(users)
                message_content = f"Сообщение от {user.username} в {channel.name}"
                models.Message.objects.create(user=user, channel=channel, content=message_content)
                self.stdout.write(f"Сообщение создано: {message_content}")
