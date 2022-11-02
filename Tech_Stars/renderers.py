from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
                "success": True,
                "status_code": status_code,
                "data": data,
                "message": "Successfully Retrieved"
            }

        if not str(status_code).startswith("2"):
            response = {"success": False, "status_code": status_code}
            try:
                response["data"] = data
            except:
                pass
            response["message"] = "Error during retrieval"

        return super(CustomRenderer, self).render(data, accepted_media_type, renderer_context)
