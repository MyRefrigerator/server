from ..base_controller import BaseController

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class IngredientsController(BaseController):
    
    def get(self, request):
        
        return self._getJsonResponse({
            'isSuccess': True
        })