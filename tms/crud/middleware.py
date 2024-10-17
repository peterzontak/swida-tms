# myapp/middleware.py
import json
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class FetchErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # Check if the request is made by Fetch API
        # if 'fetch' in request.META.get('HTTP_USER_AGENT', '').lower():
        # Return a JSON response with error details
        response_data = {
            'error': str(exception),
            'status': 'error'
        }
        return JsonResponse(response_data, status=500)
        # Let Django handle other requests normally
        # return None
