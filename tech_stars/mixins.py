import json

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from accounts.permissions import IsValidRequestAPIKey

from .permissions import IsAdminOrMembershipManagerOrReadOnly
# from .utils import decrypt_request
from .utils import write_log_csv


class AdminOrMembershipManagerOrReadOnlyMixin:
    pass
    # permission_classes = (IsValidRequestAPIKey,
    #                       IsAdminOrMembershipManagerOrReadOnly, )


class CustomListCreateAPIView(ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        serializer = self.get_serializer(data=new_request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message_obj = serializer.data.get((list(serializer.data.keys())[1]))
        print(message_obj)
        print((list(serializer.data.keys())[1]))
        write_log_csv(f"Created {self.get_serializer().Meta.model.__name__}",
                      request.user.username, f"{message_obj} was Created")
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CustomRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    def put(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=new_request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message_obj = serializer.data.get((list(serializer.data.keys())[1]))
        print(message_obj)
        print((list(serializer.data.keys())[1]))
        write_log_csv.delay(f"Updated {self.get_serializer().Meta.model.__name__}",
                            request.user.username, f"{message_obj} was updated")
        return Response(serializer.data, status=HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        write_log_csv.delay(f"Deleted {self.get_serializer().Meta.model.__name__}",
                            request.user.username, f"{instance} was deleted")
        return Response(status=HTTP_204_NO_CONTENT)


class CustomCreateAPIView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        serializer = self.get_serializer(data=new_request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message_obj = serializer.data.get((list(serializer.data.keys())[1]))
        write_log_csv.delay(f"Created {self.get_serializer().Meta.model.__name__}",
                            request.user.username, f"{message_obj} was created")
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CustomRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    def put(self, request, *args, **kwargs):
        # new_request = decrypt_request(request.data)
        new_request = request.data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=new_request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message_obj = serializer.data.get((list(serializer.data.keys())[1]))
        write_log_csv.delay(f"Updated {self.get_serializer().Meta.model.__name__}",
                            request.user.username, f"{message_obj} was updated")
        return Response(serializer.data, status=HTTP_201_CREATED)


class CustomDestroyAPIView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        write_log_csv(f"Restored {self.get_serializer().Meta.model.__name__}",
                      request.user.username, f"{instance} was restored")
        return Response(status=HTTP_204_NO_CONTENT)

# class CustomThrashAPIView(APIView):
#     queryset = ""
#     serializer_class = ""


#     # def get_serializer(self, *args, **kwargs):
#     #     return self.serializer_class(*args, **kwargs)

#     def get_object(self, **kwargs):
#         return get_object_or_404(self.queryset, id=kwargs["pk"])

#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data, status=HTTP_200_OK)

#     def delete(self, **kwargs):
#         instance = self.get_object(**kwargs)
#         instance.is_active = True
#         instance.save()
#         return Response("Restored Successfully", status=HTTP_204_NO_CONTENT)
