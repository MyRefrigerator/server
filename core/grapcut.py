import cv2
import numpy as np

def remove_background(image_path):
    # 이미지 파일을 불러옵니다.
    
    print('웍')
    image = cv2.imread(image_path)

    print('웍2')
    # 이미지 사이즈를 얻습니다.
    height, width = image.shape[:2]

    print('웍3')
    # 그랩컷 알고리즘에 필요 변수를 설정합니다.
    mask = np.zeros(image.shape[:2], np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)
    rect = (1,1, width-1, height-1)
    print('웍4')

    # 그랩컷 알고리즘을 적용합니다.
    cv2.grabCut(image, mask, rect, bg_model, fg_model, 5, cv2.GC_INIT_WITH_RECT)
    print('웍5')
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype(np.float64)
    print('웍6')
    result = image * mask2[:, :, np.newaxis]
    print('웍7')

    return result

# 종이가 놓인 책상 이미지의 경로를 지정.
image_path = "/home/ubuntu/server/assets/receipt/full_sample.png"


print('야옹')
# 배경을 제거합니다.
no_background = remove_background(image_path)


print('야옹2')
# 결과를 저장합니다.
cv2.imwrite("./no_background.png", no_background)


print('야옹3')