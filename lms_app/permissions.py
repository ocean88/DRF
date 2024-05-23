from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'Недостаточно прав для выполнения данного действия'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moder').exists()


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Разрешение позволяет доступ только владельцу объекта или персоналу (staff).
    """

    def has_object_permission(self, request, view, obj):
        # Разрешение на чтение (GET, HEAD или OPTIONS) доступно всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешение на запись доступно только владельцу или персоналу
        return obj.owner == request.user or request.user.is_staff


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем этой записи.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow 'moder' group members to edit an object.
    """

    def has_permission(self, request, view):
        # Allow read-only permissions (GET, HEAD, OPTIONS) for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow editing if user is in 'moder' group and has the change permission
        if request.user.is_authenticated:
            if request.user.groups.filter(name='moder').exists():
                return request.user.has_perm('lms_app.change_lesson')
            # Allow full access to authenticated users not in 'moder' group
            return True
        # Deny if request is not safe and user is not authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions (GET, HEAD, OPTIONS) for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow editing if user is in 'moder' group and has the change permission
        if request.user.is_authenticated:
            if request.user.groups.filter(name='moder').exists():
                return request.user.has_perm('lms_app.change_lesson')
            # Allow full access to authenticated users not in 'moder' group
            return True
        # Deny if request is not safe and user is not authenticated
        return False