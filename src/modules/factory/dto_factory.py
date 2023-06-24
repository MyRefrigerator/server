
from ...models.dtos.sample_dto import UserDto
from json import dumps
from pydantic.error_wrappers import ValidationError

# Models
from ...models.exception.custom_exception import CustomException

class DtoFactory():
    
    def getDtoInstance(self, className, paramDict):
        try:
            
            return className(**paramDict)
        
        except ValidationError as exception:
            # print('ValidationError : ', exception)
            
            errorMessage =[]
            for e in exception.errors():
                
                if len(e['loc']) == 1:
                    errorMessage.append(f'key "{e["loc"][0]}" {e["msg"]} ({e["type"]})')
                    
                else:
                    errorMessage.append(f'keys "{e["loc"]}" {e["msg"]} ({e["type"]})')
            
            raise CustomException(dumps(errorMessage))
        
        # except Exception as e:
        #     print('Exception : ', e)