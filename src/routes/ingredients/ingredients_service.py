import pymysql

# Layer
from src.routes.base_service import BaseService
from src.routes.ingredients.ingredients_repository import IngredientsRepository

# Modules
from src.modules.provider.jwt_provider import JwtProvider
from src.modules.provider.uuid_provider import UuidProvider

# Models
from src.models.dtos.ingredient.post_ingredient_manual_input_dto import PostIngredientManualInputDto

class IngredientsService(BaseService):
    
    def __init__(self):
        super().__init__()
        
        self.ingredientsRepository = IngredientsRepository()
        
    def postIngredientManualInput(self, dto: PostIngredientManualInputDto):
        print('postDeviceRegistration', dto)
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            self.ingredientsRepository.insertIngredientsRow(cursor, 'sample', [dto])
            
            conn.commit()