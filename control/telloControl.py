import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

from djitellopy import Tello
import numpy as np
import time
import cv2
import pygame

class telloControl:
    drone    = None
    widht    = 0
    height   = 0
    pid      = [0.5, 0.5, 0]
    pidUD    = [0.9, 0.9, 0]
    pError   = 0
    pErrorUD = 0

    """
    関数名 : __init__
    引数　 :  
    返り値 : 
    Telloの初期化
    """
    def __init__(self, WIDTH, HEIGHT) -> None:
        self.widht = WIDTH
        self.height = HEIGHT

        self.drone = Tello()
        self.drone.connect()
        self.drone.for_back_velowwcity =0
        self.drone.left_right_velocity =0
        self.drone.up_down_velocity =0
        self.drone.yaw_velocity =0
        self.drone.speed= 0
        self.drone.streamoff()
        self.drone.streamon()


    """
    関数名 : getTelloFrame
    引数　 : フレームの縦と横の長さ
    返り値 : 
    Telloについているカメラ映像の取得
    """
    def getTelloFrame(self):
        frame = self.drone.get_frame_read()
        frame = frame.frame
        frame = cv2.resize(frame, (self.widht, self.height))
        return frame


    """
    関数名 : controlTelloByKey
    引数　 : pygame仕様の文字列
    返り値 : 
    Telloの基本操作
    """
    def controlTelloByKey(self, pressedKey):
        SPEED = 100
        DisSPEED = -100
        speedFB = 0
        speedLR = 0
        speedAngle = 0
        speedUD = 0

        if pressedKey[pygame.K_w]:      # 前進
            speedFB = SPEED
        elif pressedKey[pygame.K_s]:    # 後進
            speedFB = DisSPEED

        if pressedKey[pygame.K_a]:      # 左
            speedLR = DisSPEED
        elif pressedKey[pygame.K_d]:    # 右
            speedLR = SPEED
        
        if pressedKey[pygame.K_q]:      # 左回転
            speedAngle = DisSPEED
        elif pressedKey[pygame.K_e]:    # 右回転
            speedAngle = SPEED

        if pressedKey[pygame.K_UP]:     # 上昇
            speedUD = SPEED
        elif pressedKey[pygame.K_DOWN]: # 下降
            speedUD = DisSPEED

        if(speedFB != 0 or speedLR != 0 or speedAngle != 0 or speedUD != 0):
            self.drone.send_rc_control(speedLR, speedFB, speedUD, speedAngle)    # 実行


    """
    関数名 : commonTello
    引数　 : プログラムの動作フラグ
    返り値 : プログラムの動作フラグ
    Telloの基本操作
    """
    def commonTello(self, mode):
        runFlag = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:            # Xを押したらプログラム終了
                    runFlag = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    # ESCキーならプログラム終了
                    runFlag = False

            if event.type == pygame.KEYUP:  
                if event.key == pygame.K_l:         # 離陸
                    time.sleep(1)
                    self.drone.land()    
                    time.sleep(1)
                    
                elif event.key == pygame.K_t:         # 着陸
                    time.sleep(1)
                    self.drone.takeoff()
                    time.sleep(1)

                if event.key == pygame.K_1:
                    mode = 0

                elif event.key == pygame.K_2:
                    mode = 1
        return runFlag, mode

    """
    関数名 : getBattery
    引数　 : 
    返り値 : バッテリ残量
    画面に出力する情報の取得
    """
    def getBattery(self):
        return  self.drone.get_battery() 

    """
    関数名 : getTime
    引数　 : 
    返り値 : 飛行時間
    画面に出力する情報の取得
    """
    def getTime(self):
        return self.drone.get_flight_time()

    
    def trackPerson(self, info):
        speedFB = 0
        if int(info[1]) > 150000:
            speedFB = 0

        elif int(info[1]) <= 150000:
            speedFB = 30

        errorUD = info[0][1] - self.height // 2
        speedUD = self.pidUD[0] * errorUD + self.pidUD[1] * (errorUD - self.pErrorUD)
        speedUD = int(np.clip(speedUD, -60, 60))

        ## PID
        error = info[0][0] - self.widht // 2
        speed = self.pid[0]*error + self.pid[1]*(error-self.pError)
        speed = int(np.clip(speed, -30, 30))

        if info[1] != 0:
            self.drone.yaw_velocity = speed
            self.drone.for_back_velocity = speedFB
            self.drone.up_down_velocity = -speedUD
        else:
            self.drone.for_back_velocity = 0
            self.drone.left_right_velocity = 0
            self.drone.up_down_velocity = 0
            self.drone.yaw_velocity = 0
            error = 0

        if self.drone.send_rc_control:
            self.drone.send_rc_control(self.drone.left_right_velocity,
                                self.drone.for_back_velocity,
                                self.drone.up_down_velocity,
                                self.drone.yaw_velocity)

        self.pError   = error
        self.pErrorUD = errorUD
        return 0