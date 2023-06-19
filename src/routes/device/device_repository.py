from mysql.connector.cursor import MySQLCursor

# Models
from src.models.dtos.device.post_device_registration_dto import PostDeviceRegistrationDto
from src.models.dtos.device.patch_device_registration_dto import PatchDeviceRegistrationDto

class DeviceRepository():
    
    # def __init__(self):
    #     pass
    
    def insertDeviceRow(
        self,
        cursor: MySQLCursor,
        dto: PostDeviceRegistrationDto
    ):

        query = '''
            INSERT INTO device
            (device_unique_key, device_os_system, device_os_version)
            VALUES (%s, %s, %s);
        '''
        
        result = cursor.execute(query, (
            dto.deviceUniqueKey,
            dto.deviceOsSystem,
            dto.deviceOsVersion,
        ))
        print(result)
        print(type(result))
    
    def getDeviceRowByUniqueKey(
        self,
        cursor: MySQLCursor,
        deviceUniqueKey: str
    ) -> dict or None:
        
        query = '''
            SELECT
                device_unique_key as deviceUniqueKey,
                device_os_system as deviceOsSystem,
                device_os_version as deviceOsVersion
            FROM device
            WHERE device_unique_key = %s;
        '''
        
        cursor.execute(query, ( deviceUniqueKey, ))
        result = cursor.fetchall()
        if len(result) == 1:
            return result[0]
        
        else:
            return None
        
    