from rest_framework.permissions import IsAuthenticatedOrReadOnly


from Accounts.permissions import IsValidRequestAPIKey


class AdminOrReadOnlyMixin:
    permission_classes = (IsValidRequestAPIKey, IsAuthenticatedOrReadOnly, )
