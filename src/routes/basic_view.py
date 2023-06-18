from django.views import View
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .template_view import TemplateView
from ..modules.receipt.receipt_provider import ReceiptProvider
from ..modules.factory.dto_factory import DtoFactory

# Computer Vision
import cv2
import numpy as np
from ..models.dtos.sample_dto import UserDto

@method_decorator(csrf_exempt, name='dispatch')
class BasicView(TemplateView):
    
    def __init__(self):
        super().__init__()
        self.receiptProvider = ReceiptProvider()
        
    # @csrf_exempt # NOT WORKING
    def get(self, request):
        
        user = DtoFactory().getDto(
            UserDto,
            {
                # 'id': 13,
                'signup_ts': '2017-06-01 12:22',
                'friends': [1, '2', b'3']
            }
        )
        
        # GET 요청 처리
        # print(self.configProvider.ocrConfig.analysis_keyword_list)
        return HttpResponse('Hello World')
    
    # @csrf_exempt # NOT WORKING
    def post(self, request):
        # POST 요청 처리
        file = self.get_chunked_image(request.FILES, 'file')
        if file is None:
            return HttpResponse('No images')
        
        # s3 다운로드
        receipt = self.receiptProvider.get_receipt(file.read())
        this.receiptDetector.getReceipt(imageBuffer)

        response = JsonResponse({
            'isSuccess': True,
            'receipt': receipt.originLines
        }, json_dumps_params={ 'ensure_ascii': False })
        return response