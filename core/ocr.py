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
        self.originLines = np.zeros((0, 12), dtype=int)
        self.convertedLines = None
        
    # arr = np.array([[1,2,3,4]])
    # arr = np.append(arr, [[4,5,6,7]], axis=0)
    # arr = np.append(arr, [[4,5,6,7]], axis=0)
    # arr = np.append(arr, [[4,5,6,7]], axis=0)
    def add_line(self, line: list):
        self.originLines = np.append(self.originLines, [line], axis=0)

def get_receipt_object(normalized_img) -> Receipt:
    
    document = pytesseract.image_to_data(normalized_img, lang='kor', output_type=pytesseract.Output.STRING)
    document_lines = document.splitlines()[1:-1]
    
    receipt = Receipt()
    for document_line in document_lines:
        document_line_parts = document_line.split('\t')
        
        if document_line_parts[11] != '':
            
            height = int(document_line_parts[9])
            min_height = 10
            max_height = 40
            
            is_valid_height = height > min_height and height < max_height
            
            if is_valid_height:    
                receipt.add_line(document_line_parts)
    
    # for b in receipt.body:
    #     print(b, ' : ', receipt.body[b])
    
    return receipt

def analysis_receipt_object(receipt: Receipt):

    # recipet.originLiens의 길이는 (N, 12)
    
    # [STEP 1] 박스들의 높이 평균값 계산
    height_nparr = receipt.originLines[:, 9]
    mean_height = np.nanmean(height_nparr.astype(np.float32), axis=0)

    # [STEP 2] 개별 박스들의 중앙값 계산 (top + height / 2)
    boundary = receipt.originLines[:, [7, 9]]
    
    median_of_boundary = boundary.astype(np.float32)[:, 0] + boundary.astype(np.float32)[:, 1] / 2
    median_of_boundary = median_of_boundary.reshape(-1, 1)
    
    # [STEP 3] 개별 박스들의 그룹화
    prev_median = 0
    group_index = -1
    
    len_originLines = int(receipt.originLines.size / receipt.originLines[0].size)
    group_index_np = np.zeros((int(len_originLines), 1), dtype=int)
    for idx in range(len_originLines):
        
        median = median_of_boundary[idx]
        text = receipt.originLines[idx][11]
        
        median_gap = abs(median - prev_median)
        prev_median = median
        if median_gap > mean_height:
            group_index = group_index + 1
            group_index_np[idx] = group_index
            # print(f'다른 그룹 {group_index}', median_gap, median, text)
            
        else:
            group_index_np[idx] = group_index
            # print(f'같은 그룹 {group_index}', median_gap, median, text)
            
    receipt.convertedLines = np.concatenate((receipt.originLines, group_index_np), axis=1)
    
            
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
    
    
    ReceiptString = '' # 유효성 검사된 문자열
    OriginString = '' # 그냥 원본 문자열
    prev_group = 0
    for lines in ReceiptObject.convertedLines:
        text = lines[11]
        now_group = lines[12]
        if prev_group != now_group:
            ReceiptString = ReceiptString + '\n' + text
            
        else:
            ReceiptString = ReceiptString + text
        
        prev_group = now_group
    for lines in ReceiptObject.originLines:
        text = lines[11]
        OriginString = OriginString + text
    print(ReceiptString)
    print(OriginString)
    
    # [DRAWING]
    count = 0
    single_color = 50
    for lines in ReceiptObject.convertedLines:
        # print([int(l) for l in lines[6:10]], lines[11])
        # [MAIN]
        color = (0, single_color, 0)
        single_color = min(single_color + 1, 255)
        draw_rectangle(boxed_img, [int(l) for l in lines[6:10]], color)
        
        # [TEMP]
        # count = count + 1
        # temp_img = normalized_img.copy()
        # draw_rectangle(temp_img, [int(l) for l in lines[6:10]], color)
        # save_path = f'{base_path}/assets/receipt/{target_path}_drawed_{count}.png'
        # is_saved = save_img(temp_img, save_path)
        # print(is_saved)
    
    # # [OUTPUT]
    save_path = f'{base_path}/assets/receipt/{target_path}_oirigin.png'
    is_saved = save_img(normalized_img, save_path)
    print(is_saved)
    
    save_path = f'{base_path}/assets/receipt/{target_path}_drawed_9999.png'
    is_saved = save_img(boxed_img, save_path)
    print(is_saved)