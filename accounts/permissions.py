from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import  AuthenticationFailed
from decouple import config
from time import time
import hashlib
from .models import Account
from rest_framework.permissions import (
    DjangoModelPermissions, IsAdminUser, BasePermission, SAFE_METHODS)


class IsAdmin(IsAdminUser):
    message = "You can't access this resource because you are'nt an Admin"

    def has_permission(self, request, view):
        return bool(request.user.is_superadmin and request.user.is_authenticated)


class IsValidRequestAPIKey(BasePermission):

    def has_permission(self, request, view):
        try:
            hash_key = request.META['HTTP_HASH_KEY']
        except:
            raise AuthenticationFailed('Missing Hash Key')
        try:
            APP_API_KEY = request.META['HTTP_API_KEY']
        except:
            raise AuthenticationFailed('Missing API key ')
        try:
            request_ts = request.META['HTTP_REQUEST_TS']
        except:
            raise AuthenticationFailed('Missing Request Timestamp ')

        app_api_key = config('APP_API_KEY')
        app_secret_key = config('APP_SECRET_KEY')
        try:
            to_hash = app_api_key + app_secret_key + request_ts
        except:
            return False
        hash = hashlib.sha256(to_hash.encode('utf8')).hexdigest()
        # print(hash)

        return hash == hash_key
