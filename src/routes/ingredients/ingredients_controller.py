from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layer
from ..base_controller import BaseController
from src.routes.ingredients.ingredients_service import IngredientsService

# Modules
from ..base_controller import BaseController
from src.modules.factory.dto_factory import DtoFactory

@method_decorator(csrf_exempt, name='dispatch')
class IngredientsController(BaseController):
    
    
    def __init__(self):
        self.dtoFactory = DtoFactory()
        self.ingredientsService = IngredientsService()
    
    def get(self, request):
        
        try:
            
            bodyDict = self._getRequestBody(request.body)
            ingredientList = self.ingredientsService.getIngredientList()
            
            return self._getJsonResponse({
                'isSuccess': True,
                'ingredientList': ingredientList
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })