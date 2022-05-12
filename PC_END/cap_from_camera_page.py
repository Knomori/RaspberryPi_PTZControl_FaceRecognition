import time

import cv2
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox
from OriginalUI import cap_from_camera
from Logic import client_parameter


class Cap_FromCamera(QDialog, cap_from_camera.Ui_Dialog):
    def __init__(self):
        QDialog.__init__(self)
        cap_from_camera.Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()  # 视频流
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.timer_camera.timeout.connect(self.show_camera)  # 若定时器结束，则调用show_camera()

        ## 关联拍照控件模组
        self.button_takePhoto.clicked.connect(self.click_takephoto_button)
        ## 自动执行的部分
        self.open_camera()

    # 点击拍照的实际动作(实际拍完照后的照片以时间为：当前时间.jpg)
    def click_takephoto_button(self):
        client_parameter.is_photoed = True
        localtime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        cv2.imwrite("./LocalData/Temp_Face/" + localtime + ".jpg", self.image)

    def open_camera(self):
        if self.timer_camera.isActive() == False:  # 若定时器未启动
            flag = self.cap.open(self.CAM_NUM)  # 参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频
            if flag == False:  # flag表示open()成不成功
                msg_box = QMessageBox(QMessageBox.Warning, '注意', '请检查相机于电脑是否连接正确!')
                msg_box.exec_()
            else:
                self.timer_camera.start(40)  # 定时器开始计时40ms，结果是每过30ms从摄像头中取一帧显示
        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label_show_camera.clear()  # 清空视频显示区域

    def show_camera(self):  # 在控件中显示现在的画面
        flag, self.image = self.cap.read()  # 从视频流中读取
        self.image = cv2.flip(self.image, 1)  # 水平反转画面

        show = cv2.resize(self.image, (900, 675))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label_showCamera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
