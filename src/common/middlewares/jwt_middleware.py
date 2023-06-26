# from django.http import HttpResponseForbidden
from django.http import JsonResponse

# Modules
# from src.modules.provider.config_provider import configProvider
from src.modules.provider.jwt_provider import JwtProvider

class JwtMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        
        if 'Authorization' in request.headers:
            
            authorization = request.headers['Authorization']
            
            splited_authorization = authorization.split('Bearer ')
            
            if len(splited_authorization) != 2:
                return JsonResponse({
                    'isSuccess': False,
                    'tempMessage': 'Bearer Token 형식을 준수해주세요'
                }, status=400)
                
            else:   
                 
                try:
                    token = JwtProvider().verify(splited_authorization[1])
                    request.token = token
                    
                    response = self.get_response(request)
                    return response
                
                except Exception as e:
                    return JsonResponse({
                        'isSuccess': False,
                        'tempMessage': '[임시용] Token의 유효성 검증 실패했습니다'
                    }, status=400)
            
        else:
            return JsonResponse({
                'isSuccess': False,
                'tempMessage': '[임시용] Bearer Token 아 누락된 요청'
            }, status=400)
        