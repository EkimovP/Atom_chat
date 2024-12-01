from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Channel, Message


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        validated_data.pop('is_moderator', None)
        validated_data.pop('is_blocked', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_moderator', 'is_blocked']


class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_moderator', 'is_blocked']


class UserManageSerializerForModerator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_blocked']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'description', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'timestamp']
