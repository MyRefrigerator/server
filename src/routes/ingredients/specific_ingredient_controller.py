from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layer
from ..base_controller import BaseController
from src.routes.ingredients.ingredients_service import IngredientsService

# Middleware
from src.common.middlewares.jwt_middleware import JwtMiddleware

# Modules
from ..base_controller import BaseController
from src.modules.factory.dto_factory import DtoFactory

# Models
from src.models.dtos.ingredient.base_ingredient_uuid_dto import BaseIngredientUuidDto
from src.models.dtos.ingredient.put_ingredient_dto import PutIngredientDto  

@method_decorator(csrf_exempt, name='dispatch')
class SpecificIngredientsController(BaseController):
    
    
    def __init__(self):
        self.dtoFactory = DtoFactory()
        self.ingredientsService = IngredientsService()
    
    @method_decorator(JwtMiddleware)
    def get(self, request, ingredientUuid=None):
        
        try:
            
            bodyDict = self._getRequestBody(request.body)
            targetDto = self.dtoFactory.getDtoInstance(BaseIngredientUuidDto, { 'ingredientUuid': ingredientUuid })
            deviceUniqueKey = request.token['deviceUniqueKey']
            ingredient = self.ingredientsService.getIngredient(deviceUniqueKey, targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True,
                'ingredient': ingredient
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })
            
    def put(self, request, ingredientUuid=None):
        
        try:
            
            bodyDict = self._getRequestBody(request.body)
            targetDto = self.dtoFactory.getDtoInstance(PutIngredientDto, {
                'ingredientUuid': ingredientUuid,
                **bodyDict
            })
            deviceUniqueKey = request.token['deviceUniqueKey']
            
            ingredient = self.ingredientsService.putIngredient(deviceUniqueKey, targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True,
                'ingredient': ingredient
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })
            
    def delete(self, request, ingredientUuid=None):
        
        try:
            
            targetDto = self.dtoFactory.getDtoInstance(BaseIngredientUuidDto, { 'ingredientUuid': ingredientUuid })
            deviceUniqueKey = request.token['deviceUniqueKey']
            
            ingredient = self.ingredientsService.delIngredient(deviceUniqueKey, targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True,
                'ingredient': ingredient
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })
        