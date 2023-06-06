import cv2
import imutils
from imutils.perspective import four_point_transform
import numpy as np

class ReceiptDetector():
    
    def __init__(self):
        print('ReceiptDetector is regerated')
        
    def load_img(salf, load_path: str) -> np.ndarray:
        return cv2.imread(load_path)

    def resize_img(self, target_img: np.ndarray) -> np.ndarray:
        return imutils.resize(target_img, width=len(target_img[0]))
        
    def convert_gray_img(salf, color_img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

    def convert_clean_img(self, dirty_img: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(dirty_img, (5, 5,), 0)
    
    def convert_edged_img(self, target_img: np.ndarray) -> np.ndarray:
        return cv2.Canny(target_img, 75, 200)
    
    def convert_nomalize_img(salf, gray_img: np.ndarray) -> np.ndarray:
        # 픽셀 값 추출
        pixels = gray_img.flatten()

        # 히스토그램 계산
        # hist, bins = np.histogram(pixels, bins=256, range=[0, 256])
        # print('히스토르그램 계산 : ', hist, bins)

        # 정규화
        # hist = hist / np.sum(hist)
        # print('정규화 : ', hist)

        # 평균, 표준편차 계산
        mean = np.mean(pixels)
        # std = np.std(pixels)
        # print('평균 : ', mean)
        # print('표준변차 : ', std)
        
        binary_img = np.where(gray_img > (mean - 25), 255, 0).astype(np.uint8)

        return binary_img

    def find_receipt_area_points(salf, gray_img: np.ndarray) -> np.ndarray:
        
        cnts = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        
        # initialize a contour that corresponds to the receipt outline
        receiptCnt = None
        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then we can
            # assume we have found the outline of the receipt
            if len(approx) == 4:
                receiptCnt = approx
                break

        return receiptCnt

    def convert_receipt_img(
        self,
        origin_image: np.ndarray,
        taget_image: np.ndarray,
        receipt_image_points: np.ndarray
    ) -> np.ndarray:
        
        target_image_ratio = origin_image.shape[1] / float(taget_image.shape[1])
        receipt_image = four_point_transform(origin_image, receipt_image_points.reshape(4, 2) * target_image_ratio)
        
        return receipt_image

    def draw_rectangle(salf, img_ndarray: np.ndarray, boundary: list, color = (0, 255, 0)):
        
        boundary_len = len(boundary)
        is_valid_boundary = boundary_len == 4
        if is_valid_boundary:
            
            start_point = (boundary[0], boundary[1])
            end_point = (boundary[0] + boundary[2], boundary[1] + boundary[3])
                    
            cv2.rectangle(img_ndarray, start_point, end_point, color, 2)
            
            return img_ndarray
        else:
            raise ValueError('boundary 길이는 4여야 합니다.')
        
    def save_img(salf, img_ndarray: np.ndarray, save_path: str) -> bool:
        try:
            result = cv2.imwrite(save_path, img_ndarray)
            
            if result == True: return True
            else: return False

        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":
    from sys import argv
    from config import get_config

    len_argv = len(argv)
    
    script_name = argv[0]
    if len_argv != 2:
        raise ValueError(f'''
            [{script_name} [purpose]가 누락되었습니다.]
            [purpose] nomalize 혹은 segmentation 이어야 합니다.
            __name__ / {__name__}\n
            ''')
    
    script_purpose = str(argv[1])
    if script_purpose == 'nomalize':
        config = get_config()
    
        receiptDetector = ReceiptDetector()

        target_path = 'sample'
        base_path = config['path']
        load_path = f'{base_path}/assets/receipt/sample/{target_path}.png'
        img = receiptDetector.load_img(load_path)
        
        gray_img = receiptDetector.convert_gray_img(img)
        normalized_img = receiptDetector.convert_nomalize_img(gray_img)
        
        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output.png'
        is_saved = receiptDetector.save_img(normalized_img, save_path)
        
        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output_2.png'
        is_saved = receiptDetector.save_iㅈmg(gray_img, save_path)
    
    elif script_purpose == 'segmentation':
        config = get_config()
        
        receiptDetector = ReceiptDetector()
        
        target_path = 'full_sample_3'
        base_path = config['path']
        load_path = f'{base_path}/assets/receipt/sample/{target_path}.png'
        
        receipt_image = receiptDetector.load_img(load_path)
        receipt_imutils_image = receiptDetector.resize_img(receipt_image.copy())
        receipt_image_ratio = receipt_image.shape[1] / float(receipt_imutils_image.shape[1])
        
        receipt_imutils_gray_image = receiptDetector.convert_gray_img(receipt_imutils_image)
        receipt_imutils_blurred_image = receiptDetector.convert_clean_img(receipt_imutils_gray_image)
        receipt_imutils_edged_image = receiptDetector.convert_edged_img(receipt_imutils_blurred_image)
        
        receiptCnt = receiptDetector.find_receipt_area_points(receipt_imutils_edged_image.copy())
        if receiptCnt is None:
            raise Exception(("Could not find receipt outline. "
                "Try debugging your edge detection and contour steps."))
            
        receipt = receiptDetector.convert_receipt_img(receipt_image, receipt_imutils_image, receiptCnt)

        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output_1.png'
        receiptDetector.save_img(receipt_image, save_path)
        
        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output_2.png'
        receiptDetector.save_img(receipt_imutils_gray_image, save_path)
        
        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output_3.png'
        receiptDetector.save_img(receipt_imutils_blurred_image, save_path)
        
        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output_4.png'
        receiptDetector.save_img(receipt_imutils_edged_image, save_path)
        
        save_path = f'{base_path}/assets/receipt/sample/{target_path}_output_5.png'
        receiptDetector.save_img(receipt, save_path)
        
    else:
        raise ValueError(f'''
            [{script_name} 잘못된 [purpose]가 입력되었습니다.]
            [purpose] nomalize 혹은 segmentation 이어야 합니다.
            __name__ / {__name__}\n
            ''')