
from ...models.dtos.sample_dto import UserDto
from ...models.exception.custom_exception import CustomException
from pydantic.error_wrappers import ValidationError
from json import dumps

class DtoFactory():
    
    def getDto(self, className, paramDict):
        try:
            
            return className(**paramDict)
        
        except ValidationError as exception:
            errorMessage =[]
            for e in exception.errors():
                
                if len(e['loc']) == 1:
                    errorMessage.append(f'{e["loc"][0]} {e["msg"]} ({e["type"]})')
                else:
                    errorMessage.append(f'{e["loc"]} {e["msg"]} ({e["type"]})')
            
            raise CustomException(dumps(errorMessage))