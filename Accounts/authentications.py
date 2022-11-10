from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from decouple import config
from datetime import datetime
import hashlib


class RequestAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # try:
        #     hash_key = request.META['HTTP_HASH_KEY']
        # except:
        #     raise PermissionDenied('Missing Hash Key')
        try:
            APP_API_KEY = request.META['HTTP_API_KEY']
            print(APP_API_KEY)
        except:
            raise AuthenticationFailed('Missing API key ')
        # try:
            # request_ts = request.META['HTTP_REQUEST_TS']
            request_ts = time.now()
        # except:
        #     raise AuthenticationFailed('Missing Request Timestamp ')
        request_ts = (datetime.now()).split(' ')[0]
        print(request_ts)
        app_api_key = config('APP_API_KEY')
        app_secret_key = config('APP_SECRET_KEY')
        try:
            to_hash = app_api_key + app_secret_key + request_ts
            print(to_hash, "rr")
        except:
            return False
        hash = hashlib.sha256(to_hash.encode('utf8')).hexdigest()
        print(hash, "Weldone")
        # print(hash_key)

        # return hash == hash_key
        return True

    def authenticate_header(self, request):
        return 'Bearer'
