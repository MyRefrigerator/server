from ..base_controller import BaseController

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Middleware
from src.common.middlewares.jwt_middleware import JwtMiddleware


@method_decorator(csrf_exempt, name='dispatch')
class IngredientsAutoInputController(BaseController):
    
    @method_decorator(JwtMiddleware)
    def get(self, request):
        
        return self._getJsonResponse({
            'isSuccess': True
        })