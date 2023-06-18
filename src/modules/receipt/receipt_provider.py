import cv2
import numpy as np

from ...models.receipt import Receipt
from .receipt_detector import ReceiptDetector

class ReceiptProvider():
    
    def __init__(self):
        
        self.receiptDetector = ReceiptDetector()
        
        pass
        
    def get_receipt(self, img_bytes: bytes):
        origin_img = cv2.imdecode(
            np.frombuffer(img_bytes, np.uint8),
            cv2.IMREAD_COLOR
            # cv2.IMREAD_GRAYSCALE
        )
        
        receipt_img= self.receiptDetector.resize_img(origin_img.copy())
        receipt_gray_img = self.receiptDetector.convert_gray_img(receipt_img)
        # receipt_blur_img = self.receiptDetector.convert_clean_img(receipt_gray_img)
        receipt_edge_img = self.receiptDetector.convert_edged_img(receipt_gray_img)
        
        receipt_area_point = self.receiptDetector.find_receipt_area_points(receipt_edge_img.copy())
        if receipt_area_point is None:
            raise Exception(("Could not find receipt outline."))
        
        receipt_img = self.receiptDetector.convert_receipt_img(origin_img, receipt_img, receipt_area_point)
        receipt_img = self.receiptDetector.convert_nomalize_img(receipt_img)

        return Receipt(origin_img)