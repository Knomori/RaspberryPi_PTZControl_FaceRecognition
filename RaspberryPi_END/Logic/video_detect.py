from time import sleep

import cv2
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from Logic import rudder_control
from Logic import raspi_parameter


class thread_video_detect(QThread):  # 线程——————网络等待连接与文件发送
    signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)  # 视频流

    def run(self):
        have_rec_fram = 0

        while True:
            ret, img = self.cap.read()
            img = cv2.flip(img, 1)  # 水平反转画面

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cap = cv2.CascadeClassifier(
                "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/RaspberryPi_END/Logic/haircare_frontage_default.xml"
            )

            faceRects = cap.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=3, minSize=(50, 50))

            if len(faceRects):
                for faceRect in faceRects:
                    x, y, w, h = faceRect

                    have_rec_fram = have_rec_fram + 1
                    if have_rec_fram == raspi_parameter.NUMBER_TO_SAVE:  # 识别到特定张后
                        have_rec_fram = 0

                        if raspi_parameter.is_connect == True:
                            if raspi_parameter.is_identify_finish == True:  # 如果是空载的情况
                                print("已经写入这个图片")
                                cv2.imwrite("face_to_recognition.jpg", img)
                                raspi_parameter.is_identify_finish = False  # 正在处理这个人

                    cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0), 2)  # 框出人脸

                    # self.judge_rudder_move_positon((x + x + h) / 2, (y + y + w) / 2)
            else:
                have_rec_fram = 0
                # print("未检测到")

            self.signal.emit(img)
            # sleep(0.05)

    # def judge_rudder_move_positon(self, position_X, position_Y):
    #     """
    #     图像的预设触发边界范围是（上下左右）：130 340 160 490
    #     图像的整个最左和最右边界是（上下左右）：70 400 100 550
    #     以上数据全部取图像和框选图像的中值
    #     """
    #     if (position_X < 160):
    #         rudder_control.rudder_move_left()
    #         print("向左")
    #     elif (position_X > 490):
    #         rudder_control.rudder_move_right()
    #         print("向右")
    #
    #     if (position_Y < 130):
    #         rudder_control.rudder_move_up()
    #         print("向上")
    #     elif (position_Y > 340):
    #         rudder_control.rudder_move_down()
    #         print("向下")
