from django.http import JsonResponse
from django.conf import settings

class SimpleApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') and request.method != 'OPTIONS':
            expected_key = getattr(settings, 'API_KEY_HEADER', None)
            if expected_key and request.headers.get('X-API-Key') != expected_key:
                return JsonResponse(
                    {"detail": "Invalid or missing API key"},
                    status=403
                )
        return self.get_response(request)
