from django.views import View
from django.http import HttpResponse
from .template_view import TemplateView

class BasicView(TemplateView):
    
    def get(self, request):
        # GET 요청 처리
        print(self.configProvider.ocrConfig.analysis_keyword_list)
        return HttpResponse('Hello World')

    # def post(self, request):
    #     # POST 요청 처리
    #     return HttpResponse('This is a POST request.')
