from rest_framework import permissions
from .models import User
from rest_framework.views import Request, View


# class IsAdminOrAccountOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view: View, obj: User) -> bool:
#         return (
#             request.user.is_authenticated
#             and obj == request.user
#             or request.user.is_staff
#         )


class IsAdminOrAccountOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.user.is_superuser and request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_superuser


class IsAuthEmployee(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:

        if request.user.is_authenticated:
            if request.user.user_type["Vendedor"] or obj == request.user:
                return True
        return False
