from uuid import UUID
from json import dumps
from pydantic import BaseModel, validator

# Models
from src.models.exception.custom_exception import CustomException

class BaseIngredientUuidDto(BaseModel):
    
    ingredientUuid: str
    
    @validator('ingredientUuid')
    def validate_ingredient_uuid(cls, value):
        try:
            
            UUID(value, version=4)
            
        except ValueError:
            raise CustomException(dumps([
                'ingredientUuid must be a valid UUID4'
            ]))
        return value