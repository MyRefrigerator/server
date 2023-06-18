import numpy as np
from config import get_config
from receipt import Receipt

class ReceiptFilter():
    
    def __init__(self, receipt: Receipt):
        print('ReceiptFilter is regerated')
        self.receipt = receipt
        
    def get_banned_line(self):
        config = get_config()
        
        banned_keyword_list = config['banned_keyword_list']
        banned_line_list = []
        
        receipt_lines = self.receipt.get_receipt_dict()
        for receipt in receipt_lines:
            line = receipt_lines[receipt].get_line()
            word = receipt_lines[receipt].get_line_word()
            boundary = receipt_lines[receipt].get_line_boundary()
            
            for banned_keyword in banned_keyword_list:
                
                if banned_keyword in word:
                    banned_line_list.append({
                        'line': line,
                        'boundary': boundary,
                        'word': word
                    })
                    break

        return banned_line_list
        
if __name__ == "__main__":
    from sys import argv
    from typing import List
    from config import get_config
    from detect import ReceiptDetector


    script_name = argv[0]
    
    config = get_config()

    base_path = config['path']
    target_path = 'full_sample_3'
    
    load_path = f'{base_path}/assets/receipt/sample/{target_path}.png'
    receiptDetector = ReceiptDetector()
    
    origin_img = receiptDetector.load_img(load_path)
    
    receipt_img= receiptDetector.resize_img(origin_img.copy())
    receipt_gray_img = receiptDetector.convert_gray_img(receipt_img)
    # receipt_blur_img = receiptDetector.convert_clean_img(receipt_gray_img)
    receipt_edge_img = receiptDetector.convert_edged_img(receipt_gray_img)
    
    receipt_area_point = receiptDetector.find_receipt_area_points(receipt_edge_img.copy())
    if receipt_area_point is None:
        raise Exception(("Could not find receipt outline. "
            "Try debugging your edge detection and contour steps."))
    
    receipt_img = receiptDetector.convert_receipt_img(origin_img, receipt_img, receipt_area_point)
    receipt_img = receiptDetector.convert_nomalize_img(receipt_img)
    
    receipt = Receipt(receipt_img)
    receipt.classify_line()
    receiptFilter = ReceiptFilter(receipt)
    banned_line_list = receiptFilter.get_banned_line()

    for banned_line in banned_line_list:
        receiptDetector.draw_filled_rectangle(receipt_img, banned_line['boundary'], color=(255, 255, 255))
    receiptDetector.save_img(receipt_img, f'./assets/receipt/sample/{target_path}_banned.png')
