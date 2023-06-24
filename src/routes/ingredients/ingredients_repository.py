import pymysql
from typing import List
from mysql.connector.cursor import MySQLCursor


# Layer
from src.routes.base_service import BaseService

# Models
from src.models.dtos.ingredient.post_ingredient_manual_input_dto import PostIngredientManualInputDto

class IngredientsRepository(BaseService):
    
    def __init__(self):
        super().__init__()
    
    def insertIngredientsRow(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str,
        dtoList: List[PostIngredientManualInputDto]
    ) -> None:
        
        query = '''
            INSERT ingredient
            (
                device_unique_key,
                ingredient_uuid,
                name, count,
                created_date, expired_date,
                first_category, second_category, third_category
            ) VALUES
        '''
        for dto in dtoList:
            
            query = query + f'''
            (
                '{deviceUniqueKey}',
                '{dto.ingredientUuid}',
                '{dto.name}', {dto.count},
                '{dto.createdDate}', '{dto.expiredDate}',
                '{dto.category}', null, null
            ),'''
        query = query.rstrip(',') + ';'
        
        cursor.execute(query)