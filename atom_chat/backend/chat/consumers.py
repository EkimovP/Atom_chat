import json
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Channel


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Устанавливаем WebSocket-соединение
        """
        # Извлекаем название канала из URL
        self.channel_name = self.scope['url_route']['kwargs']['channel_name']
        # Название группы для канала
        self.room_group_name = f'chat_{self.channel_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Закрытие WebSocket-соединения
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
       Получение сообщения
       """
        # Преобразуем текстовые данные в JSON
        data = json.loads(text_data)
        message = data['message']
        # Получаем имя пользователя
        username = self.scope['user'].username
        channel_name = self.channel_name
        # Сохраняем сообщение в базе данных
        await self.save_message(username, channel_name, message)

        # Отправляем сообщение всем пользователям, подключенным к каналу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        """
        Обработка отправки сообщения
        """
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))

    @database_sync_to_async
    def save_message(self, username, channel_name, message):
        """
        Сохраняем сообщение в базе данных
        """
        user = User.objects.get(username=username)
        channel = Channel.objects.get(name=channel_name)

        return Message.objects.create(user=user, channel=channel, content=message)
