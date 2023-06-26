from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layers
from ..base_controller import BaseController
from src.routes.alarm.alarm_service import AlarmService

# Modules
from src.modules.factory.dto_factory import DtoFactory

# Middleware
from src.common.middlewares.jwt_middleware import JwtMiddleware

@method_decorator(csrf_exempt, name='dispatch')
class ExpiredIngredientAlarmController(BaseController):
    
    def __init__(self):
        super().__init__()
        
        self.dtoFactory = DtoFactory()
        self.alarmService = AlarmService()
    
    @method_decorator(JwtMiddleware)
    def get(self, request):
        
        try:
            
            deviceUniqueKey = request.token.deviceUniqueKey
            expiredIngredientList = self.alarmService.getExpiredIngredientList(deviceUniqueKey)

            
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
            