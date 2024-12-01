from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (UserRegistrationView, UserListView, UserDetailView, UserDetailViewModerator,
                    ChannelListView, ChannelListCreateView, ChannelUpdateView, ChannelDeleteView,
                    MessageHistoryView, DeleteMessageView)


urlpatterns = [
    # Регистрация пользователя
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Обновление токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Просмотр пользователей
    path('users/', UserListView.as_view(), name='user_list'),
    # Изменение данных пользователей
    path('admin/users/<int:pk>/', UserDetailView.as_view(), name='user_detail_for_admin'),
    path('moderator/users/<int:pk>/', UserDetailViewModerator.as_view(), name='user_detail_for_moderator'),
    # Создание канала
    path('channels/create/', ChannelListCreateView.as_view(), name='channel_list_create'),
    # Получение списка каналов
    path('channels/', ChannelListView.as_view(), name='channel_list_create'),
    # Обновление канала
    path('channels/update/<int:pk>/', ChannelUpdateView.as_view(), name='channel_update'),
    # Удаление канала (по id или имени)
    path('channels/delete-by-id/<int:id>/', ChannelDeleteView.as_view(), name='channel_delete_by_id'),
    path('channels/delete-by-name/<str:name>/', ChannelDeleteView.as_view(), name='channel_delete_by_name'),
    path('channels/<str:channel_identifier>/history/', MessageHistoryView.as_view(), name='message_history'),
    path('channels/<str:channel_identifier>/history/<int:message_id>/delete/', DeleteMessageView.as_view(),
         name='delete_message'),
]
