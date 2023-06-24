import pymysql
from json import dumps

# Layer
from src.routes.base_service import BaseService
from src.routes.ingredients.ingredients_repository import IngredientsRepository

# Modules
from src.modules.provider.jwt_provider import JwtProvider
from src.modules.provider.uuid_provider import UuidProvider

# Models
from src.models.exception.custom_exception import CustomException
from src.models.dtos.ingredient.put_ingredient_dto import PutIngredientDto
from src.models.dtos.ingredient.bulk_del_ingrdient_dto import BulkDelIngredientDto
from src.models.dtos.ingredient.base_ingredient_uuid_dto import BaseIngredientUuidDto
from src.models.dtos.ingredient.post_ingredient_manual_input_dto import PostIngredientManualInputDto

class IngredientsService(BaseService):
    
    def __init__(self):
        super().__init__()
        
        self.ingredientsRepository = IngredientsRepository()
        
    # GET
        
    def getIngredientList(self):
        print('getIngredientList')
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            ingredientList = self.ingredientsRepository.selectIngredientRows(cursor, 'sample')
            
            return ingredientList
        
    def getIngredient(self, dto: BaseIngredientUuidDto):
        print('getIngredient : ', dto)
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            ingredient = self.ingredientsRepository.selectIngredientRow(
                cursor,
                'sample',
                dto.ingredientUuid
            )
            if ingredient == None:
                raise CustomException(dumps([
                'ingredient is not exsists more'
                ]))
            
            return ingredient
    
    # POST
    
    def postIngredientManualInput(self, dto: PostIngredientManualInputDto):
        print('postDeviceRegistration', dto)
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            self.ingredientsRepository.insertIngredientRows(cursor, 'sample', [dto])
            
            conn.commit()
    
    # PUT
    
    def putIngredient(self, dto: PutIngredientDto):
        print('postDeviceRegistration', dto)
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            ingredient = self.ingredientsRepository.selectIngredientRow(cursor, 'sample', dto.ingredientUuid)
            if ingredient == None:
                raise CustomException(dumps([
                    'ingredient is not exsists more'
                ]))
            
            self.ingredientsRepository.updateIngredientRow(cursor, 'sample', dto)
            
            puttedIngredient = {
                'ingredientUuid': ingredient['ingredientUuid'],
                'name': ingredient['name'],
                'count': dto.count,
                'category': ingredient['category'],
                'expiredDate': ingredient['expiredDate'],
                'createdDate': ingredient['createdDate']
            }
            
            conn.commit()
            
            return puttedIngredient
            
    # DEL
    
    def delIngredientList(self, dto: BulkDelIngredientDto):
        
        print('delIngredientList', dto)
                
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            ingredientList = self.ingredientsRepository.selectIngredientRowByOptions(cursor, 'sample', dto.ingredientUuidSet)
            if len(ingredientList) == 0:
                return []
            
            self.ingredientsRepository.deleteIngredientRowByOptions(cursor, 'sample', dto.ingredientUuidSet)
            conn.commit()
            
            return ingredientList
            
    def delIngredient(self, dto: BaseIngredientUuidDto):
        
        print('delIngredient : ', dto)
                
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            ingredient = self.ingredientsRepository.selectIngredientRow(cursor, 'sample', dto.ingredientUuid)
            if ingredient == None:
                raise CustomException(dumps([
                    'ingredient is not exsists more'
                ]))
            
            self.ingredientsRepository.deleteIngredientRow(cursor, 'sample', dto.ingredientUuid)
            
            deletedIngredient = {
                'ingredientUuid': ingredient['ingredientUuid'],
                'name': ingredient['name'],
                'count': ingredient['count'],
                'category': ingredient['category'],
                'expiredDate': ingredient['expiredDate'],
                'createdDate': ingredient['createdDate']
            }
            
            conn.commit()
            
            return deletedIngredient