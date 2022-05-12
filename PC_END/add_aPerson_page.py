import glob
import os
import time

import cv2

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox

import cap_from_camera_page
from Logic import client_parameter
from OriginalUI import add_new_person


class Add_aPerson(QDialog, add_new_person.Ui_Dialog):  # 关于程序窗口
    def __init__(self):
        QDialog.__init__(self)
        add_new_person.Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.timer_fresh_statusBar = QtCore.QTimer()
        self.timer_fresh_statusBar.timeout.connect(self.show_status)  # 若定时器结束，则调用
        self.timer_fresh_statusBar.start(5000)

        # 恢复参数的默认值
        client_parameter.new_person_name = "none"
        client_parameter.new_person_id = "404"
        client_parameter.new_person_imgPath = "./LocalData/Temp_Face"
        client_parameter.status_new_person_name = False  # 各个输入的状态
        client_parameter.status_new_person_id = False
        client_parameter.is_from_folder = False
        client_parameter.is_photoed = False

        # 关联一下控件
        self.edit_Name.textEdited[str].connect(lambda: self.onChange_person_name())  # 实时更改调用
        self.edit_IdentityCodes.textEdited[str].connect(lambda: self.onChange_person_id())
        self.button_FromCamera.clicked.connect(self.click_from_camera)
        self.button_FromFile.clicked.connect(self.click_from_folder)
        self.button_Abandon.clicked.connect(self.click_abandon)
        self.button_Continue.clicked.connect(self.click_continue)

    def onChange_person_name(self):
        new_persion_name = self.edit_Name.text()

        if len(new_persion_name) > 1:
            self.label_showName_icon.setPixmap(QPixmap("OriginalUI/正确.png"))
            client_parameter.new_person_name = new_persion_name
            client_parameter.status_new_person_name = True
        else:
            self.label_showName_icon.setPixmap(QPixmap("OriginalUI/错误.png"))
            client_parameter.status_new_person_name = False

    def onChange_person_id(self):
        new_persion_id = self.edit_IdentityCodes.text()

        if new_persion_id.isdigit():
            self.label_showID_icon.setPixmap(QPixmap("OriginalUI/正确.png"))
            client_parameter.new_person_id = new_persion_id
            client_parameter.status_new_person_id = True
        else:
            self.label_showID_icon.setPixmap(QPixmap("OriginalUI/错误.png"))
            client_parameter.status_new_person_id = False

    def click_from_camera(self):
        self.label_show_status.setText("正在拉起摄像机...")
        capture_from_camera_module = cap_from_camera_page.Cap_FromCamera()
        capture_from_camera_module.exec_()

        if client_parameter.is_photoed:
            self.label_showImg_icon.setPixmap(QPixmap("OriginalUI/正确.png"))
        else:
            self.label_showImg_icon.setPixmap(QPixmap("OriginalUI/错误.png"))

    def click_from_folder(self):
        print("点击从文件夹导入")
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        if directory:
            client_parameter.new_person_imgPath = directory
            client_parameter.is_from_folder = True
            self.label_showImg_icon.setPixmap(QPixmap("OriginalUI/正确.png"))
        else:
            print("未选择")
            self.label_showImg_icon.setPixmap(QPixmap("OriginalUI/错误.png"))
            client_parameter.is_from_folder = False

    def click_abandon(self):
        self.label_show_status.setText("已放弃，正在清理残留照片文件...")
        # 先删除旧的csv文件
        fileNames = glob.glob("./LocalData/Temp_Face" + r'/*')
        for fileName in fileNames:
            try:
                os.remove(fileName)
                print("已删除:%s" % fileName)
            except:
                print("删除旧数据出错")
        self.close()

    def click_continue(self):
        self.label_show_status.setText("正在检查")

        if client_parameter.status_new_person_id & client_parameter.status_new_person_name:
            if client_parameter.is_from_folder | client_parameter.is_photoed:
                try:
                    self.label_show_status.setText("请稍候，正在进行数据导入...")
                    new_dir_path = "./LocalData/Faces/" + client_parameter.new_person_name + " " + client_parameter.new_person_id
                    os.makedirs(new_dir_path)

                    fileNames = glob.glob(client_parameter.new_person_imgPath + r'/*')

                    n = 1
                    for fileName in fileNames:
                        pic_to_write_name = new_dir_path + "/" + str(n) + ".jpg"
                        pic_read = cv2.imread(fileName)
                        cv2.imwrite(pic_to_write_name, pic_read)
                        n = n + 1

                    QMessageBox.information(self, "提示", "导入成功，您还需要更新数据库以应用最新的数据。", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.Yes)
                    self.click_abandon()

                except:
                    QMessageBox.warning(self, u"注意！", u"我们未能正确导入这些文件",
                                        buttons=QMessageBox.Ok,
                                        defaultButton=QMessageBox.Ok)

            else:
                self.label_show_status.setText("您还没有导入图像文件")
                QMessageBox.warning(self, u"注意！", u"您还没有导入图像文件",
                                    buttons=QMessageBox.Ok,
                                    defaultButton=QMessageBox.Ok)
        else:
            self.label_show_status.setText("姓名或身份识别码不正确")
            QMessageBox.warning(self, u"注意！", u"姓名或身份识别码不正确",
                                buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.click_abandon()
        print("窗口关闭事件")

    # 自动刷新显示statusbar（伪）
    def show_status(self):
        self.label_show_status.setText("完成上面的信息，然后点击导入.")
