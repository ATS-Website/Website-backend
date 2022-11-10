from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from decouple import config
from time import time
import hashlib
from .models import Account
from rest_framework.permissions import (
    DjangoModelPermissions, IsAdminUser, BasePermission, SAFE_METHODS)


class IsAdmin(IsAdminUser):
    message = "You can't access this resource because you are'nt an Admin"

    def has_permission(self, request, view):
        admin_perm = bool(request.user and request.user.is_staff)
        return admin_perm


class IsValidRequestAPIKey(BasePermission):

    def has_permission(self, request, view):
        try:
            hash_key = request.META['HTTP_HASH_KEY']
        except:
            raise PermissionDenied('Missing Hash Key')
        try:
            APP_API_KEY = request.META['HTTP_API_KEY']
            print(APP_API_KEY)
        except:
            raise PermissionDenied('Missing API key ')
        try:
            request_ts = request.META['HTTP_REQUEST_TS']
            print(request_ts)
        except:
            raise PermissionDenied('Missing Request Timestamp ')

        app_api_key = config('APP_API_KEY')
        app_secret_key = config('APP_SECRET_KEY')
        print(app_api_key)
        try:
            to_hash = app_api_key + app_secret_key + request_ts
        except:
            return False
        hash = hashlib.sha256(to_hash.encode('utf8')).hexdigest()
        print(hash, "Weldone")
        print(hash_key)

        return hash == hash_key
        # return True
