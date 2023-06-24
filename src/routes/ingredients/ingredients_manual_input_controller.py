from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layer
from ..base_controller import BaseController
from src.routes.ingredients.ingredients_service import IngredientsService

# Modules
from src.modules.factory.dto_factory import DtoFactory

# Models
from src.models.dtos.ingredient.post_ingredient_manual_input_dto import PostIngredientManualInputDto

@method_decorator(csrf_exempt, name='dispatch')
class IngredientsManualInputController(BaseController):
    
    def __init__(self):
        self.dtoFactory = DtoFactory()
        self.ingredientsService = IngredientsService()
    
    def post(self, request):
        
        try:
            
            bodyDict = self._getRequestBody(request.body)
            targetDto = self.dtoFactory.getDtoInstance(PostIngredientManualInputDto, bodyDict)
            self.ingredientsService.postIngredientManualInput(targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })