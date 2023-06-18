from django.views import View
from django.http import HttpResponse, JsonResponse

# Models
from src.models.enums.e_status_code import EStatusCode

# Modules
from src.modules.provider.config_provider import configProvider

class BaseController(View):
    
    def __init__(self):
        self.configProvider = configProvider
        
    def get_chunked_image(
        self,
        Files, # django.core.files.uploadedfile.InMemoryUploadedFile
        KEY: str
    ):
        file = self.get_chunked_file(Files, KEY)
        
        return file if file.name.endswith('.png') or file.name.endswith('.jpg') else None
    
    def get_chunked_file(
        self,
        Files, # django.core.files.uploadedfile.InMemoryUploadedFile
        KEY: str
    ):
        try:
            return Files[KEY]
        
        except Exception as e:
            return None
        
    def _getJsonResponse(
        self,
        params: dict,
        statusCode: EStatusCode = EStatusCode.CREATED
    ):
        return JsonResponse(
            params,
            status = statusCode.value,
            json_dumps_params={ 'ensure_ascii': False }
        )