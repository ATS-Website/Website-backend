from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .permissions import IsAdminOrMembershipManagerOrReadOnly
from .utils import write_log_csv


class AdminOrMembershipManagerOrReadOnlyMixin:
    permission_classes = (IsAdminOrMembershipManagerOrReadOnly, )


class CustomListCreateAPIView(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        write_log_csv(f"Created {self.get_serializer().Meta.model.__name__}", request.user.username, "test")
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CustomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        write_log_csv(f"Updated {self.get_serializer().Meta.model.__name__}", request.user.username, "test")
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        write_log_csv(f"Deleted {self.get_serializer().Meta.model.__name__}", request.user.username, "test")
        return Response(status=HTTP_204_NO_CONTENT)


class CustomCreateAPIView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        write_log_csv(f"Created {self.get_serializer().Meta.model.__name__}", request.user.username, "test")
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CustomRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        write_log_csv(f"Updated {self.get_serializer().Meta.model.__name__}", request.user.username, "test")
        return Response(serializer.data, status=HTTP_201_CREATED)
