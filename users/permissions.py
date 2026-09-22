from rest_framework.permissions import BasePermission

MODERATOR_GROUP_NAME = 'Модераторы'


class IsModerator(BasePermission):
    """ Разрешает доступ только пользователям из Модераторы """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
        )


class IsNotModerator(BasePermission):
    """ Разрешает доступ авторизованным пользователям, кроме модераторов """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and not request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()
        )

class IsOwner(BasePermission):
    """Разрешает доступ только владельцу объекта """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user