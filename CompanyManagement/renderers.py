import re
import json
from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        all_list = re.findall("[3-5]..$", str(status_code))
        formatted_data = {
            "data": data,
            "message": None,
            "status_code": status_code,
        }
        if all_list.__len__() > 0:
            formatted_data["data"] = None
            formatted_data["error"] = data
            formatted_data["message"] = data
        return super().render(formatted_data, accepted_media_type, renderer_context)