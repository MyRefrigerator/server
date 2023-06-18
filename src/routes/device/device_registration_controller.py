from ..base_controller import BaseController
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from src.modules.provider.rds_provider import RdsProvider

@method_decorator(csrf_exempt, name='dispatch')
class DeviceRegistrationController(BaseController):
    
    def __init__(self):
        self.rdsProvider = RdsProvider()
    
    def post(self, request):
        
        conn = self.rdsProvider.get_connection()
        conn_cursor = conn.cursor()
        conn_rows = conn_cursor.execute('''INSERT INTO device (
            deviceUniqueKey,
            deviceOsSystem,
            deviceOsVersion
        ) VALUES (
            '야옹1',
            '으앙',
            '으앙'
        )''')
        conn.commit()
        
        conn_cursor.execute('SELECT * FROM device')
        conn_rows = conn_cursor.fetchall()

        print(conn_rows)
        
        conn.close()
        
        return self._getJsonResponse({
            'isSuccess': True
        })
        
    def patch(self, request):
        
        return self._getJsonResponse({
            'isSuccess': True
        })