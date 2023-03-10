from rest_framework import permissions
from .models import User
from rest_framework.views import Request, View


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user_type == 'Vendedor'
        )


class IsAuthEmployee(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:

        if request.user.is_authenticated:
            if request.user.user_type == 'Vendedor' or obj == request.user:
                return True
        return False


class IsAdminOrAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return (
            request.user.is_authenticated
            and obj == request.user
            or request.user.is_staff
        )
