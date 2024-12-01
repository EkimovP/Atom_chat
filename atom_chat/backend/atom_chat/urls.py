from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Маршрут для панели администрирования
    path('admin/', admin.site.urls),
    # Все API маршруты будут направляться в chat.urls
    path('api/', include('chat.urls')),
]
