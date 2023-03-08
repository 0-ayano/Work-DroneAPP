from control.telloControl import telloControl
import control.pygameControl as pygameControl
import control.imageControl as imageControl

import pygame
from pygame.locals import *
import sys

def test():
    # TelloとPygameの初期化
    WIDTH  = 720
    HEIGHT = 480
    screen = pygameControl.initPygame(WIDTH, HEIGHT)
    drone  = telloControl(WIDTH, HEIGHT)

    # Telloの操作
    runFlag = True
    mode    = 0
    while(runFlag):
        # キーボード入力とフレームの取得
        pressedKey = pygameControl.getKey()
        frame = drone.getTelloFrame()

    # Modeの分岐点（デフォルト）
        if mode == 0:
            # Telloの基本操作とTelloのカメラ映像の出力
            drone.controlTelloByKey(pressedKey)
            pygameImage  = imageControl.convertImg(frame)

        elif mode == 1:
            pass
        
        # 画面の生成
        battery_text = pygameControl.setText( "Battery : " + str( drone.getBattery() ) + "%" )
        time_text    = pygameControl.setText( " time   : " + str( drone.getTime() ) + "s" )
        screen.blit(pygameImage, (0, 30))
        screen.blit(battery_text, [10, 60])
        screen.blit(time_text, [10, 80])
        pygameControl.updata()

        runFlag = drone.commonTello(runFlag)

    pygameControl.quit()
    sys.exit()

test()