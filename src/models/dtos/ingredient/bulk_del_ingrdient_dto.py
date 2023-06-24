from uuid import UUID
from json import dumps
from pydantic import BaseModel, validator

# Models
from src.models.exception.custom_exception import CustomException

class BulkDelIngredientDto(BaseModel):
    
    ingredientUuidSet: set
    
    @validator('ingredientUuidSet')
    def validate_ingredient_uuid(cls, value):
        try:
            
            for v in value:
                UUID(v, version=4)
 
        except ValueError:
            
            raise CustomException(dumps([
                'ingredientUuidSet must be a valid List using valid UUID4'
            ]))
            
        return value
