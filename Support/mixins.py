from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AdminOrReadOnlyMixin:
    permission_classes = (IsAuthenticatedOrReadOnly, )
