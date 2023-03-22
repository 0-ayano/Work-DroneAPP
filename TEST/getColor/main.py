import cv2
import numpy as np

# 赤色の検出
def detect_color(img, h):
    h1 = int(h) - 10
    h2 = int(h) + 10

    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域1
    hsv_min = np.array([h1, 100, 100])
    hsv_max = np.array([h2,255,255])

    # 緑色領域のマスク（255：赤色、0：赤色以外）    
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    
    # マスキング処理
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return mask, masked_img


# 入力画像の読み込み
img = cv2.imread("./test1.png")

# 色検出
mask, masked_img = detect_color(img, 90)

# 結果を出力
cv2.imwrite("./mask.png", mask)
cv2.imwrite("./masked_img.png", masked_img)