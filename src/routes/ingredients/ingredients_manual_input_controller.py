from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layer
from ..base_controller import BaseController
from src.routes.ingredients.ingredients_service import IngredientsService

# Middleware
from src.common.middlewares.jwt_middleware import JwtMiddleware

# Modules
from src.modules.factory.dto_factory import DtoFactory

# Models
from src.models.dtos.ingredient.post_ingredient_manual_input_dto import PostIngredientManualInputDto

@method_decorator(csrf_exempt, name='dispatch')
class IngredientsManualInputController(BaseController):
    
    def __init__(self):
        self.dtoFactory = DtoFactory()
        self.ingredientsService = IngredientsService()
    
    @method_decorator(JwtMiddleware)
    def post(self, request):
        
        try:
            
            bodyDict = self._getRequestBody(request.body)
            targetDto = self.dtoFactory.getDtoInstance(PostIngredientManualInputDto, bodyDict)
            deviceUniqueKey = request.token['deviceUniqueKey']
            
            self.ingredientsService.postIngredientManualInput(deviceUniqueKey, targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })