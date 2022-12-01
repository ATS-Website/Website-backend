from rest_framework.permissions import IsAuthenticatedOrReadOnly


from accounts.permissions import IsValidRequestAPIKey


class AdminOrReadOnlyMixin:
    pass
    # permission_classes = (IsValidRequestAPIKey, IsAuthenticatedOrReadOnly, )
