from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atom_chat.settings')

from chat import routing, middleware


application = ProtocolTypeRouter({
    # Для HTTP-запросов используем стандартное ASGI-приложение
    'http': get_asgi_application(),
    # Для WebSocket используем middleware для аутентификации по JWT
    'websocket': middleware.JWTAuthMiddleware(
        URLRouter(routing.websocket_urlpatterns)
    )
})
