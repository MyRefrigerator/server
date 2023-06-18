from typing import List

import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

class ReceiptLine():
    
    def __init__(self, line: int):
        print('ReceiptLine is generated')
        self.line = line
        self.word = ''
        self.wordNpdarr = np.zeros((0, 1))
        self.wordBoundary = np.zeros((0, 4), dtype=np.int64)
    
    def add_word(self, word: str, boundary: np.ndarray) -> None:
        self.word = self.word + word
        self.wordNpdarr = np.append(self.wordNpdarr, [np.array([word])], axis=0)
        self.wordBoundary = np.append(self.wordBoundary, [boundary.astype(np.int64)], axis=0)
    
    def get_line_boundary(self) -> np.ndarray:
        x = int(self.wordBoundary[:, 0].min())   # 0열 최솟값
        y = int(self.wordBoundary[:, 1].min())   # 1열 최솟값
        width = int((self.wordBoundary[:, 0] + self.wordBoundary[:, 2]).max())   # 0열 + 2열 합의 최댓값
        height = int((self.wordBoundary[:, 3]).max())   # 1열 + 3열 합의 최댓값
        
        # 안정값 조정
        x = x - 20
        
        return np.array([x, y, width, height])

    def get_line(self) -> str:
        
        return self.line
    
    def get_line_word(self) -> str:
        
        return self.word
    
    def get_word(self) -> np.ndarray:
        
        return self.wordNpdarr
    
    def get_word_boundary(self) -> np.ndarray:
        
        return self.wordBoundary  

class Receipt():
    
    def __init__(self, receipt_img: np.ndarray):
        print('Receipt is generated')
        
        self.bodyKeys = []
        self.body = {}
        self.originLines = np.zeros((0, 12), dtype=int)
        self.convertedLines = None
        
        document = pytesseract.image_to_data(receipt_img, lang='kor', output_type=pytesseract.Output.STRING)
        document_lines = document.splitlines()[1:-1]
        
        for document_line in document_lines:
            document_line_parts = document_line.split('\t')
            
            if document_line_parts[11] != '':
                height = int(document_line_parts[9])
                min_height = 10
                max_height = 40
                
                is_valid_height = height > min_height and height < max_height
                
                if is_valid_height:    
                    self.add_line(document_line_parts)

    def add_line(self, line: list):
        self.originLines = np.append(self.originLines, [line], axis=0)
    
    def classify_line(self):
        # [STEP 1] 박스들의 높이 평균값 계산
        height_nparr = self.originLines[:, 9]
        mean_height = np.nanmean(height_nparr.astype(np.float64), axis=0)

        # [STEP 2] 개별 박스들의 중앙값 계산 (top + height / 2)
        boundary = self.originLines[:, [7, 9]]
        
        median_of_boundary = boundary.astype(np.float64)[:, 0] + boundary.astype(np.float64)[:, 1] / 2
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
                
                # print(median_case, min_median, median, max_median)
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

    def classify_data(self):
        print(self.convertedLines)

    def get_receipt_dict(self):
        
        receipt_dict = {}
        for idx, convertedLine in enumerate(self.convertedLines):
            line = convertedLine[12]
            text = convertedLine[11]
            boundary = convertedLine[6:10]
            
            if line in receipt_dict:
                receipt_dict[line].add_word(text, boundary)
            else:
                receipt_dict[line] = ReceiptLine(line)
                receipt_dict[line].add_word(text, boundary)
            
        return receipt_dict
    
    def get_receipt_string(self):
        
        receipt_content = '' # 유효성 검사된 문자열
        
        prev_group = 0
        for lines in self.convertedLines:
            text = lines[11]
            now_group = lines[12]
            if prev_group != now_group:
                receipt_content = receipt_content + '\n' + text
                
            else:
                receipt_content = receipt_content + ' ' + text
            
            prev_group = now_group
            
        return receipt_content
    
    def get_receipt_without_line(self):
        
        receipt_content = '' # 그냥 원본 문자열
            
        for lines in self.originLines:
            text = lines[11]
            receipt_content = receipt_content + text
            
        return receipt_content