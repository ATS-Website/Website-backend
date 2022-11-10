from django.utils.deprecation import MiddlewareMixin
import json

from .enc_dec.encryption_decryption import aes_encrypt
from .utils import write_server_logs


class EncryptionAndDecryptionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        # for the_key in response.data:
        #     response.data[the_key] = aes_encrypt(response.data.get(the_key))
        # print(type(response.data) == 'rest_framework.utils.serializer_helpers.ReturnList')
        # print(type(str(type(response.data))))
        # print(json.dumps(response.data))
        # for items in json.dumps(response.data):
        #     print(items)
        #     break

        # print(aes_encrypt(json.dumps(response.data)))
        # print(vars(response))
        # print(vars(request))
        try:
            url = str(vars(response).get("renderer_context").get("request"))[33:-1]
            status_code = str(vars(response).get("renderer_context").get("response"))[22:25]
            write_server_logs(url, status_code)
        except:
            pass
        return response
