from .permissions import IsAdminOrReadOnly


class AdminOrContentManagerOrReadOnlyMixin:
    permission_classes = (IsAdminOrReadOnly,)
