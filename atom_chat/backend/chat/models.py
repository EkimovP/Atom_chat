from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_moderator = models.BooleanField(default=False,
                                       help_text="Указывает, является ли пользователь модератором")
    is_blocked = models.BooleanField(default=False,
                                     help_text="Указывает, является ли пользователь заблокированным")

    class Meta:
        swappable = 'AUTH_USER_MODEL'


User = get_user_model()


class Channel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    channel = models.ForeignKey(Channel, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message by {self.user.username} in {self.channel.name}"
