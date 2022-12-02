from rest_framework.permissions import IsAuthenticatedOrReadOnly

from accounts.permissions import IsValidRequestAPIKey


class AdminOrReadOnlyMixin:
    permission_classes = (IsValidRequestAPIKey, IsAuthenticatedOrReadOnly, )
