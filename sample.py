import cv2
import numpy as np
import pytesseract


# 이미지 파일 불러오기
image_file = 'sample.jpg'
image = cv2.imread(image_file)

# OpenCV를 사용하여 이미지 기울기 보정
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.bitwise_not(gray)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# TesseractOCR 설정
config = '--psm 11'

# 이미지에서 텍스트 추출
text = pytesseract.image_to_string(image, lang='kor')
print(text)