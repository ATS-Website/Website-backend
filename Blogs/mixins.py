from .permissions import IsAdminOrReadOnly

from Accounts.permissions import IsValidRequestAPIKey


class AdminOrContentManagerOrReadOnlyMixin:
    # permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (IsValidRequestAPIKey, IsAdminOrReadOnly,)
