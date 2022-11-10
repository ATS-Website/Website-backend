from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    message = "You do not have the permission to perform this action"

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or ((request.user.is_superadmin or request.user.is_membership_manager) and
                                                       request.user.is_authenticated))


class OnlyAdminDelete(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in ["POST", "PUT", "GET", "PATCH"] or ((request.user.is_superadmin or request.user.is_membership_manager) and
                                                                          request.user.is_authenticated))
