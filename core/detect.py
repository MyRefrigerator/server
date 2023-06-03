import cv2
import numpy as np

def load_img(load_path: str) -> np.ndarray:
    return cv2.imread(load_path)

def convert_gray_img(color_img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

def nomalize_img(gray_img: np.ndarray) -> np.ndarray:
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

def draw_rectangle(
    img_ndarray: np.ndarray,
    boundary: list,
    color = (0, 255, 0)
):
    
    boundary_len = len(boundary)
    is_valid_boundary = boundary_len == 4
    if is_valid_boundary:
        
        start_point = (boundary[0], boundary[1])
        end_point = (boundary[0] + boundary[2], boundary[1] + boundary[3])
                
        cv2.rectangle(img_ndarray, start_point, end_point, color, 2)
        
        return img_ndarray
    else:
        raise ValueError('boundary 길이는 4여야 합니다.')
    

def save_img(img_ndarray: np.ndarray, save_path: str) -> bool:
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

    script_name = argv[0]
    print(f'\n[{script_name}] __name__ / {__name__}\n')
        
    config = get_config()
    
    base_path = config['path']
    target_path = 'sample'
    
    load_path = f'{base_path}/assets/receipt/{target_path}.png'
    img = load_img(load_path)
    
    gray_img = convert_gray_img(img)
    normalized_img = nomalize_img(gray_img)
    
    save_path = f'{base_path}/assets/receipt/{target_path}_output.png'
    is_saved = save_img(normalized_img, save_path)
    
    save_path = f'{base_path}/assets/receipt/{target_path}_output_2.png'
    is_saved = save_img(gray_img, save_path)