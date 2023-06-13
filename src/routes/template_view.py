from django.views import View
from django.http import HttpResponse
from src.modules.config_provider import configProvider

class TemplateView(View):
    
    def __init__(self):
        self.configProvider = configProvider