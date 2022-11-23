from .permissions import IsValidRequestAPIKey, IsAdmin


class IsAdminOrReadOnlyMixin:
    pass
    # permission_classes = (IsValidRequestAPIKey, IsAdmin)
