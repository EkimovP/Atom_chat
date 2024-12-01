from django.contrib import admin


from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Настройка админки для модели CustomUser.
    """
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('id', 'username', 'email', 'is_moderator', 'is_blocked', 'date_joined')

    # Поля, по которым можно искать в админке
    search_fields = ('username', 'email')

    # Фильтры по полям
    list_filter = ('is_moderator', 'is_blocked')

    # Поля, которые можно редактировать прямо из списка
    list_editable = ('is_blocked', 'is_moderator')

    # Поля, отображаемые на форме редактирования пользователя
    fields = ('username', 'email', 'is_moderator', 'is_blocked', 'date_joined')

    # Поля, доступные только для чтения
    readonly_fields = ('id', 'date_joined')

    # Кастомные действия
    actions = ['make_moderator', 'remove_moderator', 'block_users', 'unblock_users']

    def make_moderator(self, request, queryset):
        """
        Назначить модераторами выбранных пользователей
        """
        updated = queryset.update(is_moderator=True)
        self.message_user(request, f"Назначено модераторами: {updated} пользователь(-я).")

    make_moderator.short_description = "Назначить модераторами"

    def remove_moderator(self, request, queryset):
        """
        Убрать роль модератора у выбранных пользователей
        """
        updated = queryset.update(is_moderator=False)
        self.message_user(request, f"Роль модератора убрана у: {updated} пользователя(-ей).")

    remove_moderator.short_description = "Убрать роль модератора"

    def block_users(self, request, queryset):
        """
        Заблокировать выбранных пользователей
        """
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f"Заблокировано пользователей: {updated}.")

    block_users.short_description = "Заблокировать пользователей"

    def unblock_users(self, request, queryset):
        """
        Разблокировать выбранных пользователей
        """
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f"Разблокировано пользователей: {updated}.")

    unblock_users.short_description = "Разблокировать пользователей"

    def get_queryset(self, request):
        """
        Ограничить доступ к пользователям для администраторов
        """
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.exclude(is_superuser=True)
        return queryset
