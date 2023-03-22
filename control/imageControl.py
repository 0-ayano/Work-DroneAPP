import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
import numpy as np
import pygame

"""
関数名 : convertImg
引数　 : opencvの画像
返り値 : pygameの画像
OpenCVの画像をPygame用に変換する
- [opencvで作った画像をpygameで描画する。](https://blanktar.jp/blog/2016/01/pygame-draw-opencv-image.html)
"""
def convertImg(opencvImage: np.ndarray) -> pygame.Surface:
    opencvImage = opencvImage[:, :, ::-1]  # OpenCVはBGR、pygameはRGBなので変換してやる必要がある。
    shape = opencvImage.shape[1::-1]  # OpenCVは(高さ, 幅, 色数)、pygameは(幅, 高さ)なのでこれも変換。
    pygameImage = pygame.image.frombuffer(opencvImage.tobytes(), shape, 'RGB')

    return pygameImage


"""
関数名 : findColor
引数　 : 
返り値 : 抽出した色をマークした画像情報, [中点, 半径, 座標]
特定色の抽出処理
"""
def findColor(img, rgb):
    # 任意色の閾（H）の設定
    rgb =  np.uint8([[[rgb[0], rgb[1], rgb[2]]]])
    hsv = cv2.cvtColor(rgb,cv2.COLOR_BGR2HSV)
    h1 = hsv[0][0][0] - 10
    h2 = hsv[0][0][0] + 10

    if(h1 >= 179):
        h1 = 179
    if(h2 <= 0):
        h2 = 0
    
    hsv_min = np.array([h1, 100, 100])
    hsv_max = np.array([h2,255,255])

    # 任意色を黒、それ以外を白にマスキング
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    label = cv2.connectedComponentsWithStats(mask)
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # 取得した色の位置情報の取得
    maxArea = 0
    maxCoodinateX = 0
    maxCoodinateY = 0
    for i in range(n):
        if data[i][4] / (data[i][2] * data[i][3]) >= 0.6 and data[i][4] >= 1000:
            x, y = map(int, center[i])
            if maxArea < data[i][4]:
                maxArea = data[i][4]
                maxCoodinateX = x
                maxCoodinateY = y
            cv2.circle(img, (x, y), 5, (0, 205, 255), 3)
            # cv2.rectangle(img, (x0, y0), (x1, y1), (0, 205, 255))
            # cv2.putText(img, "ID: " + str(i + 1), (x - 20, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
            # cv2.putText(img, "S: " + str(data[i][4]), (x - 20, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
            # cv2.putText(img, "Bounds: " + str(int(data[i][2] * int(data[i][3]))), (x - 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
            # cv2.putText(img, "X: " + str(int(center[i][0])), (x - 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
            # cv2.putText(img, "Y: " + str(int(center[i][1])), (x - 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
    return [[maxCoodinateX, maxCoodinateY], maxArea]