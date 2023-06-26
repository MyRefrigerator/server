import pymysql
from json import dumps
from datetime import datetime

# Layer
from src.routes.base_service import BaseService
from src.models.exception.custom_exception import CustomException

# Modules
from src.modules.provider.jwt_provider import JwtProvider
from src.modules.provider.uuid_provider import UuidProvider

# Models
from src.routes.ingredients.ingredients_repository import IngredientsRepository

class AlarmService(BaseService):
    
    def __init__(self):
        super().__init__()
        
        self.ingredientsRepository = IngredientsRepository()
        
    def getExpiredIngredientList(
        self,
        deviceUniqueKey: str
    ):
        print('getExpiredIngredientList')
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            
            nowUtcDatetime = datetime.utcnow()
            nowUtcStr = nowUtcDatetime.strftime("%y.%m.%d")
            
            expiredIngredientList = self.ingredientsRepository.selectExpiredIngredientRow(cursor, deviceUniqueKey, nowUtcStr)
            
            return expiredIngredientList