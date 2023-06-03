from detect import load_img, convert_gray_img, nomalize_img, draw_rectangle, save_img
from typing import List

import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

class Receipt():
    
    def __init__(self):
        print('OcrReceipt is generated')
        
        self.bodyKeys = []
        self.body = {}
        self.originLines = []
        sel;f
        
    def add_line(self, line: list):
        # print(
        #     f'level : {line[0]}\n',
        #     f'page_num : {line[1]}\n',
        #     f'block_num : {line[2]}\n',
        #     f'par_num : {line[3]}\n',
        #     f'line_num : {line[4]}\n',
        #     f'word_num : {line[5]}\n',
        #     f'text : {line[11]}\n===================='
        # )
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
                
        # word_line = line[4]
        # if word_line in self.bodyKeys:
        #     # print(line[11])
            
        #     self.body[word_line] += line[11]
        # else:
        #     # print(line[11])
            
        #     self.bodyKeys.append(word_line)
        #     self.body[word_line] = line[11]
        # print(line)
        
        height = int(line[9])
        min_height = 10
        max_height = 40
        is_valid_height = height > min_height and height < max_height
        if is_valid_height:
            self.originLines.append(line)

def get_receipt_object(normalized_img) -> Receipt:
    
    document = pytesseract.image_to_data(normalized_img, lang='kor', output_type=pytesseract.Output.STRING)
    document_lines = document.splitlines()[1:-1]
    
    receipt = Receipt()
    for document_line in document_lines:
        document_line_parts = document_line.split('\t')
        
        if document_line_parts[11] != '':
            receipt.add_line(document_line_parts)
    
    # for b in receipt.body:
    #     print(b, ' : ', receipt.body[b])
    return receipt

def analysis_receipt_object(receipt: Receipt):

    arr = []
    for line in receipt.originLines:
        height = int(line[9])
        arr.append(height)

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
    ReceiptObject = get_receipt_object(normalized_img)
    analysis_receipt_object(ReceiptObject)
    
    # [DRAWING]
    for lines in ReceiptObject.originLines:
        # print([int(l) for l in lines[6:10]], lines[11])
        draw_rectangle(boxed_img, [int(l) for l in lines[6:10]])
    
    
    # [OUTPUT]
    save_path = f'{base_path}/assets/receipt/{target_path}_oirigin.png'
    is_saved = save_img(normalized_img, save_path)
    print(is_saved)
    
    save_path = f'{base_path}/assets/receipt/{target_path}_drawed.png'
    is_saved = save_img(boxed_img, save_path)
    print(is_saved)