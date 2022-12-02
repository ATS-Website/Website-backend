import json
from ast import literal_eval

from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin

from tech_stars.renderers import CustomRenderer
from .enc_dec.encryption_decryption import aes_encrypt
from .utils import write_server_logs


# from .tasks import write_server_logs


class EncryptionAndDecryptionMiddleware(MiddlewareMixin):

    body = ""

    def process_request(self, request):
        try:
            self.body = request.body.decode("utf8")
        except:
            self.body = {}
        pass

    def process_response(self, request, response):

        try:
            url = str(vars(response).get(
                "renderer_context").get("request"))[33:-1]
            status_code = str(vars(response).get(
                "renderer_context").get("response"))[22:25]

            if request.method == "POST" or request.method == "PUT":
                print("hello")
                write_server_logs(url, status_code, literal_eval(self.body))
            else:
                write_server_logs(url, status_code)
        except:
            status_code = ""
            pass

        return response
