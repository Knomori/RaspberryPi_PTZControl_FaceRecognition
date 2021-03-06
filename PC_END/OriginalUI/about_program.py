# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_program.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_about_app(object):
    def setupUi(self, about_app):
        about_app.setObjectName("about_app")
        about_app.resize(850, 475)
        about_app.setMinimumSize(QtCore.QSize(850, 475))
        about_app.setMaximumSize(QtCore.QSize(850, 475))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/人脸识别.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        about_app.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(about_app)
        self.label.setGeometry(QtCore.QRect(30, 20, 141, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/人脸识别.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(about_app)
        self.label_2.setGeometry(QtCore.QRect(180, 20, 611, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(about_app)
        self.label_3.setGeometry(QtCore.QRect(280, 450, 291, 19))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(about_app)
        self.label_4.setGeometry(QtCore.QRect(270, 160, 541, 111))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(about_app)
        self.label_5.setGeometry(QtCore.QRect(180, 70, 661, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(about_app)
        self.label_7.setGeometry(QtCore.QRect(40, 190, 231, 191))
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(about_app)
        self.label_6.setGeometry(QtCore.QRect(40, 380, 20, 20))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/天平.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(about_app)
        self.label_8.setGeometry(QtCore.QRect(70, 380, 141, 19))
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(about_app)
        self.label_10.setGeometry(QtCore.QRect(270, 270, 541, 91))
        self.label_10.setAutoFillBackground(False)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")

        self.retranslateUi(about_app)
        QtCore.QMetaObject.connectSlotsByName(about_app)

    def retranslateUi(self, about_app):
        _translate = QtCore.QCoreApplication.translate
        about_app.setWindowTitle(_translate("about_app", "关于本程序"))
        self.label_2.setText(_translate("about_app", "Beluga 2.1"))
        self.label_3.setText(_translate("about_app", "2022     作者：Knomori"))
        self.label_4.setText(_translate("about_app", "       Beluga最开始诞生于一个实习项目，也不将止于实习项目。整体的程序使用以树莓派作为人脸图像采集的主要入口，进行人脸的追踪与识别。由服务端（本程序）进行人脸数据的录入、数据管理等功能的程序，两程序互相配合以发挥最大的效能。本程序的构建全部在Linux下完成，同时可以运行于Windows和MacOS.目前本程序目前由Knomori进行维护与开发。"))
        self.label_5.setText(_translate("about_app", "Beluga——基于树莓派的人脸追踪与识别的打卡系统（总控制与识别端）"))
        self.label_7.setText(_translate("about_app", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">构建测试信息：</span></p><p>               测试平台：ArchLinux</p><p> KDE Plasma 版本：5.24</p><p>KDE程序框架版本：5.92</p><p>                 QT版本： 5.15</p><p>              图形平台：X11</p></body></html>"))
        self.label_8.setText(_translate("about_app", "GPL-3.0 License "))
        self.label_10.setText(_translate("about_app", "       本程序使用GPL-3.O开源协议。同时希望可以对这方面感兴趣的同学一些微不足道的参考。也希望同学们通过社区分享你的发现，同样地分享你遇到的问题。欢迎大家去搜索、做出努力、提出反馈、帮助他人、参与其中并为此做出贡献。"))
