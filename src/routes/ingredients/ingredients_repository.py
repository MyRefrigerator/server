import pymysql
from typing import List
from mysql.connector.cursor import MySQLCursor


# Layer
from src.routes.base_service import BaseService

# Models
from src.models.dtos.ingredient.put_ingredient_dto import PutIngredientDto
from src.models.dtos.ingredient.post_ingredient_manual_input_dto import PostIngredientManualInputDto

class IngredientsRepository(BaseService):
    
    def __init__(self):
        super().__init__()
    
    def selectIngredientRows(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str
    ) -> None:
        
        query = '''
            SELECT
                ingredient_uuid as ingredientUuid,
                name,
                count,
                created_date as createdDate,
                expired_date as expiredDate,
                first_category as category
            FROM ingredient
            WHERE device_unique_key = %s;
        '''
        cursor.execute(query, ( deviceUniqueKey, ))
        
        result = cursor.fetchall()
        return result
    
    def selectIngredientRowByOptions(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str,
        ingredientUuidSet: set
    ) -> dict or None:
        
        ingredientUuidStr = '(' + ', '.join(f"'{ingredientuuid}'" for ingredientuuid in ingredientUuidSet) + ')'
        query = f'''
            SELECT
                ingredient_uuid as ingredientUuid,
                name,
                count,
                created_date as createdDate,
                expired_date as expiredDate,
                first_category as category
            FROM ingredient
            WHERE   device_unique_key   =   %s
            AND     ingredient_uuid     IN  {ingredientUuidStr};
        '''
        
        cursor.execute(query, ( deviceUniqueKey, ))
        
        result = cursor.fetchall()
        if len(result) == 0:
            return []
        
        else:
            return result
        
    def selectIngredientRow(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str,
        ingredientUuid: str
    ) -> dict or None:
        
        query = '''
            SELECT
                ingredient_uuid as ingredientUuid,
                name,
                count,
                created_date as createdDate,
                expired_date as expiredDate,
                first_category as category
            FROM ingredient
            WHERE   device_unique_key = %s
            AND     ingredient_uuid = %s;
        '''
        cursor.execute(query, ( deviceUniqueKey, ingredientUuid, ))
        
        result = cursor.fetchall()
        if len(result) == 1:
            return result[0]
        
        else:
            return None
    
    # INSERT
    
    def insertIngredientRows(
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
        
    # PUT
    
    def updateIngredientRow(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str,
        dto: PutIngredientDto
    ) -> None:
        
        query = '''
            UPDATE  ingredient
            SET     count = %s
            WHERE   device_unique_key = %s
            AND     ingredient_uuid = %s;
        '''
        
        cursor.execute(query, (
            dto.count,
            deviceUniqueKey,
            dto.ingredientUuid,
        ))
        
    # DEL
    
    def deleteIngredientRow(
        self,
        cursor: MySQLCursor,
        devcieUniqueKey: str,
        ingredientUuid: str
    ) -> None:
        
        query = '''
            DELETE
            FROM    ingredient
            WHERE   device_unique_key = %s
            AND     ingredient_uuid = %s;
        '''
        
        cursor.execute(query, (
            devcieUniqueKey,
            ingredientUuid,
        ))
        
    def deleteIngredientRowByOptions(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str,
        ingredientUuidSet: set
    ) -> None:
        
        ingredientUuidStr = '(' + ', '.join(f"'{ingredientuuid}'" for ingredientuuid in ingredientUuidSet) + ')'
        query = f'''
            DELETE
            FROM ingredient
            WHERE   device_unique_key   =   %s
            AND     ingredient_uuid     IN  {ingredientUuidStr};
        '''
        
        cursor.execute(query, ( deviceUniqueKey, ))