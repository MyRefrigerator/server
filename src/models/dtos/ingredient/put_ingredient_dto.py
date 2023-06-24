from uuid import UUID
from json import dumps
from pydantic import BaseModel, validator

# Models
from src.models.exception.custom_exception import CustomException

class PutIngredientDto(BaseModel):
    
    ingredientUuid: str
    
    count: int
    
    @validator('ingredientUuid')
    def validate_ingredient_uuid(cls, value):
        try:
            
            UUID(value, version=4)

        except ValueError:
            
            raise CustomException([
                'ingredientUuid must be a valid UUID4'
            ])
            
        return value
    
    @validator('count')
    def count_positive(cls, value):
        
        if value <= 0:
            
            raise CustomException(dumps([
                'count must be a positive integer'
            ]))
            
        return value