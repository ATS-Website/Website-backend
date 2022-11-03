from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsAdminOrReadOnly


class AdminOrReadOnlyMixin:
   permission_classes = (IsAuthenticatedOrReadOnly,)
