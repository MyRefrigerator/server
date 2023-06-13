from django.views import View
from django.http import HttpResponse
from src.models.config_model import ConfigProvider

class TemplateView(View):
    
    def __init__(self):
        self.configProvider = ConfigProvider()