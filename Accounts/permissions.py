from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from decouple import config
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
            raise AuthenticationFailed('Missing Hash Key')
        try:
            API_KEY = request.META['HTTP_API_KEY']
        except:
            raise AuthenticationFailed('Missing API key ')
        try:
            request_ts = request.META['HTTP_REQUEST_TS']
        except:
            raise AuthenticationFailed('Missing Request Timestamp ')

        app_api_key = config('APP_API_KEY')
        app_secret_key = config('APP_SECRET_KEY')
        try:
            de_hash = app_api_key + app_secret_key + request_ts
        except:
            return False
        hash = hashlib.sha256(de_hash.encode('utf8')).hexdigest()

        # if hash != hash_key:
        #     return False
        return hash == hash_key
