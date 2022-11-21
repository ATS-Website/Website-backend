import json

from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin

from Tech_Stars.renderers import CustomRenderer
from .enc_dec.encryption_decryption import aes_encrypt
from .utils import write_server_logs
# from .tasks import write_server_logs


class EncryptionAndDecryptionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print(request._request__data)
        # print(request.user)
        # print(request.method)
        # print(json.loads(request.body))
        pass

    def process_response(self, request, response):
        try:
            url = str(vars(response).get(
                "renderer_context").get("request"))[33:-1]
            print(url)
            status_code = str(vars(response).get(
                "renderer_context").get("response"))[22:25]
            if request.method == "POST" or request.method == "PUT":
                write_server_logs.delay(url, status_code, request.body)
            else:
                write_server_logs.delay(url, status_code)
        except:
            pass

        # context = vars(response).get("renderer_context")
        # encrypted = aes_encrypt(json.dumps(response.data))
        # response = Response({encrypted})
        # response.accepted_renderer = CustomRenderer()
        # response.accepted_media_type = "application/json"
        # response.renderer_context = context
        # response.render()
        return response
