from .permissions import IsAdminOrReadOnly

from accounts.permissions import IsValidRequestAPIKey


class AdminOrContentManagerOrReadOnlyMixin:
    pass
    # permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (IsValidRequestAPIKey, IsAdminOrReadOnly,)
