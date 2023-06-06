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
    
    def classify_line(self):
        # [STEP 1] 박스들의 높이 평균값 계산
        height_nparr = self.originLines[:, 9]
        mean_height = np.nanmean(height_nparr.astype(np.int), axis=0)

        # [STEP 2] 개별 박스들의 중앙값 계산 (top + height / 2)
        boundary = self.originLines[:, [7, 9]]
        
        median_of_boundary = boundary.astype(np.int)[:, 0] + boundary.astype(np.int)[:, 1] / 2
        median_of_boundary = median_of_boundary.reshape(-1, 1)
        
        # [STEP 3] 개별 박스들의 그룹화
        prev_median = 0
        min_median, max_median = 999999999, 0
        group_index = 0
        
        len_originLines = int(self.originLines.size / self.originLines[0].size)
        group_index_np = np.zeros((int(len_originLines), 1), dtype=int)
        for idx in range(len_originLines):
            median: int = median_of_boundary[idx][0]
            text = self.originLines[idx][11]
            
            median_gap = abs(median - prev_median)
            # print('prev : ', prev_median, '/ median : ', median, '/ text : ', text)
            prev_median = median 
            min_median = 0
            
            is_diff_group = median_gap > mean_height
            if is_diff_group:
                group_index = group_index + 1
                group_index_np[idx] = group_index
                
                min_median, max_median = median, median
            else:
                group_index_np[idx] = group_index
                
                is_min_median = median < min_median
                is_max_median = median > max_median
                
                median_case = 'min_value' if is_min_median else 'max_value' if is_max_median == True else 'none'
                
                print(median_case, min_median, median, max_median)
                if median_case == 'min_value':
                    total_group_indexes = np.where(group_index_np == group_index)[0]
                    total_group = median_of_boundary[total_group_indexes]
                    
                    target_group = total_group[total_group[:, 0] < median + median_gap]
                    target_group = target_group.flatten()
                    
                    # print('👿 경고 👿 예외 케이스 처리 발견시 처리 필요함')
                    
                    min_median = median
                    
                elif median_case == 'max_value':
                    total_group_indexes = np.where(group_index_np == group_index)[0]
                    total_group = median_of_boundary[total_group_indexes]
                    
                    target_group = total_group[total_group[:, 0] > median + median_gap]
                    target_group = target_group.flatten()
                    
                    # print('👿 경고 👿 예외 케이스 처리 발견시 처리 필요함')
                    
                    max_median = median
                
        self.convertedLines = np.concatenate((self.originLines, group_index_np), axis=1)

    def get_receipt(self):
        
        receipt_content = '' # 유효성 검사된 문자열

        prev_group = 0

        for lines in self.convertedLines:
            text = lines[11]
            now_group = lines[12]
            if prev_group != now_group:
                receipt_content = receipt_content + '\n' + text
                
            else:
                receipt_content = receipt_content + text
            
            prev_group = now_group
            
        return receipt_content
    
    def get_receipt_without_line(self):
        
        receipt_content = '' # 그냥 원본 문자열
            
        for lines in self.originLines:
            text = lines[11]
            receipt_content = receipt_content + text
            
        return receipt_content

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
    ReceiptObject.classify_line()
    receipt = ReceiptObject.get_receipt()
    receipt2 = ReceiptObject.get_receipt_without_line()
    
    # [DRAWING]
    count = 0
    single_color = 50
    for lines in ReceiptObject.convertedLines:
        # print([int(l) for l in lines[6:10]], lines[11])
        # [MAIN]
        color = (0, single_color, 0)
        single_color = min(single_color + 1, 255)
        draw_rectangle(boxed_img, [int(l) for l in lines[6:10]], color)
    
    # # [OUTPUT]
    save_path = f'{base_path}/assets/receipt/{target_path}_oirigin.png'
    is_saved = save_img(normalized_img, save_path)
    print(is_saved)
    
    save_path = f'{base_path}/assets/receipt/{target_path}_drawed_9999.png'
    is_saved = save_img(boxed_img, save_path)
    print(is_saved)