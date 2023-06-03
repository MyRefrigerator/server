from detect import load_img, convert_gray_img, nomalize_img, draw_rectangle, save_img
from typing import List

import numpy as np
import pytesseract

class Receipt():
    
    def __init__(self):
        print('OcrReceipt is generated')
        
        self.bodyKeys = []
        self.body = {}
        
    def add_line(self, line: list):
        # self.level = line[0]
        # self.page_num = line[1]
        # self.block_num = line[2]
        # self.par_num = line[3]
        # self.line_num = line[4]
        # self.word_num = line[5]
        # self.left = line[6]
        # self.top = line[7]
        # self.width = line[8]
        # self.height = line[9]
        # self.conf = line[10]
        # self.text = line[11]
                
        word_line = line[4]
        if word_line in self.bodyKeys:
            # print(line[11])
            
            self.body[word_line] += line[11]
        else:
            # print(line[11])
            
            self.bodyKeys.append(word_line)
            self.body[word_line] = line[11]

def get_receipt_object(normalized_img):
    print('미구현')
    # document: str = pytesseract.image_to_data(normalized_img, lang='kor')
    # document_lines = document.splitlines()
    
    # receipt = Receipt()
    # for document_line in document_lines:
    #     document_line_parts = document_line.split('\t')
        
    #     receipt.add_line(document_line_parts)
    
    # for b in receipt.body:
    #     print(b, ' : ', receipt.body[b])

def get_receipt_string(normalized_img):
    document: str = pytesseract.image_to_string(normalized_img, lang='kor')
    
    return document

if __name__ == "__main__":
    from sys import argv
    from config import get_config
        
    script_name = argv[0]
    
    config = get_config()

    base_path = config['path']
    target_path = 'sample'
    
    load_path = f'{base_path}/assets/receipt/{target_path}.png'
    img = load_img(load_path)
    
    gray_img = convert_gray_img(img)
    normalized_img = nomalize_img(gray_img)
    boxed_img = normalized_img.copy()
    
    # get_ImageBoxes(normalized_img)
    ReceiptString = get_receipt_string(normalized_img)
    print(ReceiptString)