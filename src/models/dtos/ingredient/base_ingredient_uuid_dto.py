from pydantic import BaseModel, validator
from uuid import UUID

class BaseIngredientUuidDto(BaseModel):
    
    ingredientUuid: str
    
    @validator('ingredientUuid')
    def validate_ingredient_uuid(cls, value):
        try:
            UUID(value, version=4)
        except ValueError:
            raise ValueError('ingredientUuid must be a valid UUID4')
        return value