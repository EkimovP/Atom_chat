from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from channels.auth import BaseMiddleware
from asgiref.sync import sync_to_async
from jwt import InvalidTokenError, DecodeError


User = get_user_model()


@sync_to_async
def get_user_from_jwt(validated_token):
    """
    Извлекает пользователя из валидного токена
    """
    try:
        user_id = validated_token.get("user_id")
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Для аутентификации пользователя по JWT-токену
    """
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = None

        # Извлечение токена из заголовка Authorization
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode()
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if token:
            try:
                # Валидация токена
                validated_token = UntypedToken(token)
                user = await get_user_from_jwt(validated_token)
                scope['user'] = user
            except (InvalidTokenError, DecodeError, KeyError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
