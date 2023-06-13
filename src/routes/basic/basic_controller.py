from django.views import View
from django.http import HttpResponse

class BasicView(View):
    def get(self, request):
        # GET 요청 처리
        return HttpResponse('This is a GET request.')

    def post(self, request):
        # POST 요청 처리
        return HttpResponse('This is a POST request.')
