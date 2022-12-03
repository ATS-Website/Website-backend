from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
            "status": "success",
            "status_code": status_code,
            "data": data,
            "message": "Successfully Retrieved"
        }

        if not str(status_code).startswith("2"):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data
            except KeyError:
                response["data"] = data
                response["message"] = "An Error ocurred"

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
