from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)