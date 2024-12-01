from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView

from .serializers import (UserRegistrationSerializer, UserListSerializer, UserManageSerializer,
                          UserManageSerializerForModerator, ChannelSerializer, MessageSerializer)
from .permissions import IsModeratorOrSuperUser, IsModerator, IsSuperUser
from .models import Channel, Message


User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Уведомление": "Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    permission_classes = [IsModeratorOrSuperUser]
    serializer_class = UserListSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_moderator=False, is_staff=False, is_superuser=False)


class UserDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsSuperUser]
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserManageSerializer

    def perform_update(self, serializer):
        serializer.save()


class UserDetailViewModerator(RetrieveUpdateAPIView):
    permission_classes = [IsModerator]
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserManageSerializerForModerator

    def perform_update(self, serializer):
        user = self.get_object()

        if user.is_moderator or user.is_staff or user.is_superuser:
            raise PermissionDenied("Модераторы не могут изменять данные других модераторов или администраторов")

        serializer.save()


class ChannelListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelListCreateView(CreateAPIView):
    permission_classes = [IsModeratorOrSuperUser]
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ChannelUpdateView(UpdateAPIView):
    permission_classes = [IsModeratorOrSuperUser]
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    def patch(self, request, *args, **kwargs):
        channel = self.get_object()

        # Обновляем только те поля, которые были переданы
        # Если имя не указано, сохраняем текущее
        name = request.data.get('name', channel.name)
        # Если описание не указано, сохраняем текущее
        description = request.data.get('description', channel.description)

        # Обновляем объект и сохраняем изменения
        channel.name = name
        channel.description = description
        channel.save()

        # Возвращаем обновленные данные
        serializer = self.get_serializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChannelDeleteView(APIView):
    permission_classes = [IsModeratorOrSuperUser]

    def delete(self, request, *args, **kwargs):
        channel_id = kwargs.get('id', None)
        channel_name = kwargs.get('name', None)

        if channel_id:
            channel = get_object_or_404(Channel, id=channel_id)
        elif channel_name:
            channel = get_object_or_404(Channel, name=channel_name)
        else:
            return Response(
                {"Ошибка": "Необходимо указать id или name канала"},
                status=status.HTTP_400_BAD_REQUEST
            )

        channel.delete()
        return Response(
            {"Уведомление": f"Канал '{channel.name}' успешно удален"},
            status=status.HTTP_200_OK
        )


class MessageHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        channel_identifier = self.kwargs['channel_identifier']
        if channel_identifier.isdigit():
            channel = get_object_or_404(Channel, id=int(channel_identifier))
        else:
            channel = get_object_or_404(Channel, name=channel_identifier)
        return Message.objects.filter(channel=channel)

class DeleteMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, channel_identifier, message_id):
        try:
            if channel_identifier.isdigit():
                channel = Channel.objects.get(id=int(channel_identifier))
            else:
                channel = Channel.objects.get(name=channel_identifier)
        except Channel.DoesNotExist:
            return Response({"Ошибка": "Канал не найден"}, status=status.HTTP_404_NOT_FOUND)

        message = get_object_or_404(Message, id=message_id, channel=channel)

        if not (request.user.is_superuser or request.user.is_moderator):
            raise PermissionDenied("У вас нет прав на удаление этого сообщения")

        # Удаляем сообщение
        message.delete()
        return Response({"Уведомление": "Сообщение успешно удалено"}, status=status.HTTP_204_NO_CONTENT)
