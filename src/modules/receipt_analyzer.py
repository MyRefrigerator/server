import numpy as np
from config import get_config
from receipt import Receipt

class ReceiptAnalyzer():
    
    def __init__(self, receipt: Receipt):
        print('ReceiptAnalyzer is regerated')
        self.receipt = receipt
        
    def get_analysis_line(self):
        config = get_config()
        
        analysis_keyword_list = config['analysis_keyword_list']
        analysis_line_list = []
        
        receipt_lines = self.receipt.get_receipt_dict()
        
        for receipt in receipt_lines:
            line = receipt_lines[receipt].get_line()
            word = receipt_lines[receipt].get_line_word()
            boundary = receipt_lines[receipt].get_line_boundary()
                
            for analysis_keyword in analysis_keyword_list:
                if analysis_keyword in word:
                    analysis_line_list.append({
                        'line': line,
                        'boundary': boundary,
                        'word': word
                    });
                    break
                    
        
        return analysis_line_list
    
    def get_menu_line(self):
        
        taget_line_group = self.get_analysis_line()
        target_line = taget_line_group[0]['line']
        
        menu_line_nparr = np.zeros((0,4), dtype=int)
        
        receipt_lines = self.receipt.get_receipt_dict()
        for receipt in receipt_lines:
            line = receipt_lines[receipt].get_line()
            line_word = receipt_lines[receipt].get_line_word()
            
            words = receipt_lines[receipt].get_word()
            word_boundaries = receipt_lines[receipt].get_word_boundary()
        
            if line.astype(int) > target_line.astype(int):
                # [STEP 1] 박스들의 가로 평균값 계산 
                mean_width = np.nanmean(word_boundaries[:,2].astype(np.float32), axis=0)
                
                # [STEP 2] 개별 박스들의 가로 중앙값 계산 (left + width / 2)
                x_boundary = word_boundaries[:, [0, 2]]
                median_of_x_boundary = x_boundary.astype(np.float32)[:, 0] + x_boundary.astype(np.float32)[:, 1] / 2
                median_of_x_boundary = median_of_x_boundary.reshape(-1, 1)

                # [STEP 3] 개별 박스들의 그룹화
                prev_median_x = 0
                min_median_x, max_median_x = 999999999, 0
                group_index = 0
                
                menu_group = []
                temp_menu_group = ''
                for idx in range(len(median_of_x_boundary)):
                    median_x: int = median_of_x_boundary[idx][0]
                    
                    median_x_gap = abs(median_x - prev_median_x) - 5
                    prev_median_x = median_x
                    
                    # 👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿 #
                    # 👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿 #
                    # 👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿👿 #
                    # 지금 여기값이 이상함 #
                    
                    
                    is_diff_group = median_x_gap > mean_width
                    if is_diff_group:
                        group_index = group_index + 1
                        if temp_menu_group == '':
                            menu_group.append(words[idx][0])
                        else:
                            menu_group.append(temp_menu_group)
                        temp_menu_group = ''
                    else:
                        temp_menu_group = temp_menu_group + words[idx][0]
                
                if len(menu_group) != 4:
                    break
                
                menu_line_nparr = np.vstack([menu_line_nparr, np.array(menu_group)])
                
            else:
                continue
        print(menu_line_nparr)
        
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
    
    ReceiptAnalyzer(receipt)
    receiptAnalyzer = ReceiptAnalyzer(receipt)
    analysis_line_list = receiptAnalyzer.get_analysis_line()
    menu_line_list = receiptAnalyzer.get_menu_line()

    for analysis_line in analysis_line_list:
        receiptDetector.draw_rectangle(receipt_img, analysis_line['boundary'], color=(0, 0, 0))
        
    for analysis_line in menu_line_list:
        for boundary in analysis_line['boundary']:
            receiptDetector.draw_rectangle(receipt_img, boundary, color=(0, 0, 0))
        
    receiptDetector.save_img(receipt_img, f'./assets/receipt/sample/{target_path}_analysis.png')