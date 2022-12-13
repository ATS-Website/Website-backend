from rest_framework.renderers import JSONRenderer
from .enc_dec.encryption_decryption import aes_encrypt


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        if str(status_code).startswith("2"):
            response = {
                "success": True,
                "status_code": status_code,
                # "data": aes_encrypt(data)
                "data": data,
                "message": "Successfully"
            }

        else:
            response = {"success": False, "status_code": status_code}
            try:
                response["data"] = data
            except:
                pass
            response["message"] = "Error during retrieval"

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
