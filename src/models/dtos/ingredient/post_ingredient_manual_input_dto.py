from json import dumps
from pydantic import BaseModel, constr, validator

# Models
from src.models.exception.custom_exception import CustomException

class PostIngredientManualInputDto(BaseModel):
    
    name: constr(max_length=64)
    count: int
    category: str
    expiredDate: str
    createdDate: str
    
    @validator('count')
    def count_positive(cls, value):
        if value <= 0:
            raise CustomException(dumps([
                'count must be a positive integer'
            ]))
        return value