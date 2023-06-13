from django.views import View
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .template_view import TemplateView

# Computer Vision
import cv2
import numpy as np

@method_decorator(csrf_exempt, name='dispatch')
class BasicView(TemplateView):
    
    # @csrf_exempt # NOT WORKING
    def get(self, request):
        # GET 요청 처리
        print(self.configProvider.ocrConfig.analysis_keyword_list)
        return HttpResponse('Hello World')
    
    # @csrf_exempt # NOT WORKING
    def post(self, request):
        
        # POST 요청 처리\
        file = self.get_chunked_image(request.FILES, 'file')
        if file is None:
            return HttpResponse('No images')
        
        # file = request.FILES['file']
        file_bytes = file.read()
        image_np = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        # image_np = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(f'./color_{file}', image_np)

        return HttpResponse('This is a POST request.')
