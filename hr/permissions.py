from rest_framework import permissions
from hr.models import Employee

class HasPositionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            return obj.position is not None
        return False