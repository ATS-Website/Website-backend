from .permissions import IsValidRequestAPIKey, IsAdmin


class IsAdminOrReadOnlyMixin:
    permission_classes = (IsValidRequestAPIKey, IsAdmin)
