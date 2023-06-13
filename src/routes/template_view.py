from django.views import View
from django.http import HttpResponse
from src.modules.config_provider import configProvider

class TemplateView(View):
    
    def __init__(self):
        self.configProvider = configProvider
        
    def get_chunked_image(
        self,
        Files, # django.core.files.uploadedfile.InMemoryUploadedFile
        KEY: str
    ):
        file = self.get_chunked_file(Files, KEY)
        
        return file if file.name.endswith('.png') else None
    
    def get_chunked_file(
        self,
        Files, # django.core.files.uploadedfile.InMemoryUploadedFile
        KEY: str
    ):
        try:
            return Files[KEY]
        
        except Exception as e:
            return None