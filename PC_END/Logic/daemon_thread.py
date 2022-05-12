import time
from time import sleep

import cv2
import sqlite3

from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

from Logic import face_recognition, client_parameter


class daemon_thread(QThread):  # 线程3————守护进程 用于如果有新的图片发回第一时间进行人脸识别与通知显示
    signal = pyqtSignal(object, object, object, object)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            print("证实到守护进程")

            if client_parameter.is_recongition == True:
                client_parameter.is_recongition = False

                # 处理图片到合适的控件大小
                img = cv2.imread(client_parameter.face_to_recognition)
                img_new = cv2.resize(img, (590, 440))  # 缩放至合适大小
                qt_img = cv2.cvtColor(img_new, cv2.COLOR_BGR2BGRA)  # 转换图片为qt图片
                h, w = qt_img.shape[0:2]
                qt_img = QImage(qt_img.data, w, h, QImage.Format_RGB32)

                # 处理合适的图片缩放大小
                if client_parameter.status_rec is 1:
                    qt_icon = QtGui.QPixmap("OriginalUI/正确.png")
                elif client_parameter.status_rec is 2:
                    qt_icon = QtGui.QPixmap("OriginalUI/提示.png")
                elif client_parameter.status_rec is 3:
                    qt_icon = QtGui.QPixmap("OriginalUI/警告.png")
                else:
                    qt_icon = QtGui.QPixmap("OriginalUI/错误.png")

                self.signal.emit(client_parameter.recongitioned_name, client_parameter.recongitioned_id, qt_img, qt_icon)

                sleep(5)
            else:
                if client_parameter.REFRESH_RATE == 0:
                    sleep(1)
                else:
                    sleep(2)

    def show_default(self):
        print("显示默认")
