from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layers
from ..base_controller import BaseController
from src.routes.alarm.alarm_service import AlarmService

# Modules
from src.modules.factory.dto_factory import DtoFactory

@method_decorator(csrf_exempt, name='dispatch')
class ExpiredIngredientAlarmController(BaseController):
    
    def __init__(self):
        super().__init__()
        
        self.dtoFactory = DtoFactory()
        self.alarmService = AlarmService()
    
    def get(self, request):
        
        try:
            
            expiredIngredientList = self.alarmService.getExpiredIngredientList()
            
            return self._getJsonResponse({
                'isSuccess': True,
                'expiredIngredientList': expiredIngredientList,
                'expiredIngredientCount': len(expiredIngredientList)
            })
        
        except Exception as e:
            
            print('Exception : ', e)
            
            return self._getJsonResponse({
                'isSuccess': False
            })
            