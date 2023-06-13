from django.http import HttpResponseForbidden
from ...modules.config_provider import configProvider

class APIKeyMiddleware:
    
    def __init__(self, get_response):
        self.api_key = configProvider.api_key
        
        self.get_response = get_response

    def __call__(self, request):
        # API 키 확인 로직을 구현합니다.
        # print(request.META)
        api_key = request.META.get('HTTP_API_KEY')
        if not self.is_valid_api_key(api_key):
            return HttpResponseForbidden('Invalid API key')

        response = self.get_response(request)
        return response

    def is_valid_api_key(self, api_key):
        # 유효한 API 키인지 확인하는 로직을 구현합니다.
        # 예를 들어, 데이터베이스나 외부 서비스와의 검증 등을 수행할 수 있습니다.
        # 유효한 API 키라면 True를 반환하고, 그렇지 않다면 False를 반환합니다.
        return api_key == self.api_key
