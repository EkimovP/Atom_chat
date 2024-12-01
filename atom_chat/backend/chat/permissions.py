from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Разрешение, позволяющее доступ только суперпользователям
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsModerator(BasePermission):
    """
    Разрешение, позволяющее доступ только модераторам
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsModeratorOrSuperUser(BasePermission):
    """
    Разрешение, позволяющее доступ модераторам и суперпользователям
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_moderator or request.user.is_superuser)
