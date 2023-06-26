from django.http import HttpRequest
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
from src.models.dtos.ingredient.bulk_del_ingrdient_dto import BulkDelIngredientDto

@method_decorator(csrf_exempt, name='dispatch')
class IngredientsController(BaseController):
    
    
    def __init__(self):
        self.dtoFactory = DtoFactory()
        self.ingredientsService = IngredientsService()
    
    @method_decorator(JwtMiddleware)
    def get(self, request: HttpRequest):
        
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
    
    @method_decorator(JwtMiddleware)
    def delete(self, request: HttpRequest):
        
        try:
            
            print("set(request.GET.get('ingredientUuid').split(',') : ", set(request.GET.get('ingredientUuid').split(',')))
            print("set(request.GET.get('ingredientUuid').split(',') : ", type(set(request.GET.get('ingredientUuid').split(','))))
                  
            targetDto = self.dtoFactory.getDtoInstance(BulkDelIngredientDto, {
                'ingredientUuidSet': set(request.GET.get('ingredientUuid').split(','))
            })
            ingredientList = self.ingredientsService.delIngredientList(targetDto)
            
            return self._getJsonResponse({
                'isSuccess': True,
                'ingredientList': ingredientList
            })
            
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })