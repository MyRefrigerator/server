from ..base_controller import BaseController
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Layer
from src.routes.device.device_service import DeviceService

# Modules
from src.modules.factory.dto_factory import DtoFactory

# Models
from src.models.dtos.device.post_device_registration_dto import PostDeviceRegistrationDto
from src.models.dtos.device.patch_device_registration_dto import PatchDeviceRegistrationDto

@method_decorator(csrf_exempt, name='dispatch')
class DeviceRegistrationController(BaseController):
    
    def __init__(self):
        # self.rdsProvider = RdsProvider()
        self.dtoFactory = DtoFactory()
        self.deviceService = DeviceService()
    
    def post(self, request):
        
        bodyDict = self._getRequestBody(request.body)
        targetDto = self.dtoFactory.getDtoInstance(PostDeviceRegistrationDto, bodyDict)
        self.deviceService.postDeviceRegistration(targetDto)
        
        return self._getJsonResponse({
            'isSuccess': True
        })
        
    def patch(self, request):
        
        bodyDict = self._getRequestBody(request.body)
        targetDto = self.dtoFactory.getDtoInstance(PatchDeviceRegistrationDto, bodyDict)
        deviceToken = self.deviceService.patchDeviceRegistration(targetDto)
                
        return self._getJsonResponse({
            'isSuccess': True,
            'deviceToken': deviceToken
        })