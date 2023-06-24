from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layer
from ..base_controller import BaseController
from src.routes.ingredients.ingredients_service import IngredientsService

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
    
    def get(self, request, ingredientUuid=None):
        
        try:
            
            bodyDict = self._getRequestBody(request.body)
            targetDto = self.dtoFactory.getDtoInstance(BaseIngredientUuidDto, { 'ingredientUuid': ingredientUuid })
            
            ingredient = self.ingredientsService.getIngredient(targetDto)
            
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
            ingredient = self.ingredientsService.putIngredient(targetDto)
            
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
            ingredient = self.ingredientsService.putIngrediedelIngredientnt(targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True,
                'ingredient': ingredient
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })
        