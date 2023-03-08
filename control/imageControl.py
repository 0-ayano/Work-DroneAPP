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
関数名 : findColorByShiroma
引数　 : 
返り値 : 抽出した色をマークした画像情報, [中点, 半径, 座標]
特定色の抽出処理
"""