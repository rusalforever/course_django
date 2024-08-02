from rest_framework import permissions

class HasPositionPermission(permissions.BasePermission):
    message = 'Accessing the Employee data requires an Employee Position.'

    def has_permission(self, request, view):
        # Check if the user is authenticated and has an employee_position attribute
        return request.user.is_authenticated and hasattr(request.user, 'employee_position')