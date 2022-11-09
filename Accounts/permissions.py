from .models import Account
from rest_framework.permissions import (
    DjangoModelPermissions, IsAdminUser, BasePermission, SAFE_METHODS)


class IsAdmin(IsAdminUser):
    message = "You can't access this resource because you are'nt an Admin"

    def has_permission(self, request, view):
        admin_perm = bool(request.user and request.user.is_staff)
        return admin_perm
