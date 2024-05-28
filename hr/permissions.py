from rest_framework import permissions


class IsNotRussianEmail(permissions.BasePermission):
    """
    Allows access only to users whose email does not end with .ru
    """

    def has_permission(self, request, view):
        if request.user and request.user.email:
            return not request.user.email.endswith('.ru')
        return False


class EmployeeHawPosition(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.position:
            return True
        return False
