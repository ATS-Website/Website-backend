from .permissions import IsAdminOrReadOnly

from accounts.permissions import IsValidRequestAPIKey


class AdminOrContentManagerOrReadOnlyMixin:
    permission_classes = (IsValidRequestAPIKey, IsAdminOrReadOnly,)
