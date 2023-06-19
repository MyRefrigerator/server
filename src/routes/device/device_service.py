import pymysql

# Layer
from src.routes.base_service import BaseService
from src.routes.device.device_repository import DeviceRepository

# Modules
from src.modules.provider.jwt_provider import JwtProvider

# Models
from src.models.dtos.device.post_device_registration_dto import PostDeviceRegistrationDto
from src.models.dtos.device.patch_device_registration_dto import PatchDeviceRegistrationDto

class DeviceService(BaseService):
    
    def __init__(self):
        super().__init__()
        
        self.deviceRepository = DeviceRepository()
        self.jwtProvider = JwtProvider()
    
    def postDeviceRegistration(self, dto: PostDeviceRegistrationDto):
        print('postDeviceRegistration', dto)
        
        with self.rdsProvider.get_auto_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            deviceData = self.deviceRepository.getDeviceRowByUniqueKey(cursor, dto.deviceUniqueKey)
            if deviceData != None:
                raise '이미 등록된 기기입니다.'
            
            self.deviceRepository.insertDeviceRow(cursor, dto)
            conn.commit()
    
    def patchDeviceRegistration(self, dto: PatchDeviceRegistrationDto):
        print('patchDeviceRegistration', dto)
        
        with self.rdsProvider.get_auto_connection() as conn:
            
            cursor = conn.cursor(dictionary=True)
            deviceData = self.deviceRepository.getDeviceRowByUniqueKey(cursor, dto.deviceUniqueKey)
            if deviceData == None:
                raise '등록되지 않은 기기입니다.'

            return self.jwtProvider.encode(deviceData)
            