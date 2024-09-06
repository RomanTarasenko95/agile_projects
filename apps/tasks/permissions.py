from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает доступ владельцу объекта и только для чтения другим пользователям.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ для чтения всем пользователям
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Проверяем, что пользователь является владельцем объекта
        return obj.owner == request.user
