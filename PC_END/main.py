import sys
import os
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

import add_aPerson_page
import show_checked_page
from Logic import client_parameter, face_getdb, daemon_thread, output_file, action_communtion_server,action_receive_img
from OriginalUI import MainClient
from OriginalUI.about_program import Ui_about_app
import setting_page
import show_server_status_page

class Main(QMainWindow, MainClient.Ui_MainWindow):
    def __init__(self):
        # 初始化
        QMainWindow.__init__(self)
        MainClient.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 关联动作
        self.action_train_face.triggered.connect(self.train_facedb)
        self.action_about.triggered.connect(self.show_about_app)
        self.action_server.triggered.connect(self.click_server)
        self.action_exit_app.triggered.connect(self.exit_prog)
        self.action_addPesion.triggered.connect(self.add_aPersion)
        self.action_show_check.triggered.connect(self.show_clocked_status)
        self.action_output_SQLite.triggered.connect(self.click_output_sqlite)
        self.action_output_Excel.triggered.connect(self.click_output_excel)
        self.action_main_settings.triggered.connect(self.click_setting)
        self.action_restar_comm.triggered.connect(self.resrart_comm_server)
        self.action_restart_img.triggered.connect(self.resrart_img_server)

        # 程序运行就执行的动作
        self.communion_server()
        self.img_server()
        self.daemon_thread()

    # 以下是显示控制 ##############################
    def statusBar_ToShow_15(self, textToShow):  # 仅显示 statusbBar信息 15秒
        self.statusbar.showMessage(textToShow, 15000)

    def statusBar_ShowAllTime(self, textToShow):  # 一直显示 statusBar
        self.statusbar.showMessage(textToShow)

    # 以下是逻辑动作控制 ##############################
    def communion_server(self):
        self.thread_connect_server = action_communtion_server.thread_communion_server()
        self.thread_connect_server.start()

    def img_server(self):
        self.thread_img_server = action_receive_img.thread_img_server()
        self.thread_img_server.start()

    def daemon_thread(self):
        self.thread_daemon = daemon_thread.daemon_thread()
        self.thread_daemon.signal.connect(self.show_result)
        self.thread_daemon.start()

    def resrart_img_server(self):
        print("点击重新启动图像服务器")
        if client_parameter.IMG_STATUS == "正常":
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "图像服务器正在正常工作，无需重启。")
            msg_box.exec_()
        else:
            # 推送通知
            icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
            cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "已经尝试重新启动图像服务器。", icon)
            os.system(cmd)

            self.img_server()

    def resrart_comm_server(self):
        print("点击重新启动通信服务器")
        if client_parameter.COMM_STATUS == "正常":
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "通信服务器正在正常工作，无需重启。")
            msg_box.exec_()
        else:
            # 推送通知
            icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
            cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "已经尝试重新启动通信服务器。", icon)
            os.system(cmd)

            self.communion_server()



    # def callback_statusBar_show(self, show_text):  # 用于statusBar的显示回调
    #     if not client_parameter.is_connect:
    #         msg_box = QMessageBox(QMessageBox.Warning, '注意', '无法正确连接到服务器，程序可能无法正常运行。')
    #         msg_box.exec_()
    #     self.statusBar_ShowAllTime(show_text)

    def train_facedb(self):  # 点击菜单中的训练模型
        self.thread_train_face = face_getdb.thread_train_face()
        self.thread_train_face.signal.connect(self.statusBar_ToShow_15)
        self.thread_train_face.start()

    def click_server(self):    # 点击服务器状态
        print("点击服务器状态")
        show_server = show_server_status_page.Show_ServerStatus()
        show_server.exec_()

    def add_aPersion(self):
        print("点击添加一个新人")
        addPerson_dlg = add_aPerson_page.Add_aPerson()
        addPerson_dlg.exec_()

    def show_clocked_status(self):
        print("点击展示所有数据")
        check_in_page = show_checked_page.Show_CheckedPage()
        check_in_page.exec_()

    def click_output_sqlite(self):
        output_file.Output_Files.output_as_sqlite(self)

    def click_output_excel(self):
        output_file.Output_Files.output_as_excel(self)

    def click_setting(self):
        print("点击设定")
        setting_dlg = setting_page.Setting_Dlg()
        setting_dlg.exec_()

    def show_result(self, NAME, ID, IMG, ICON):
        if client_parameter.status_rec is 0:
            self.label_showPic_shendBack.setText("正在等待服务端送入图片")
            self.label_showName.setText("等待中...")
            self.label_showNumber.setText(str(204))
            self.label_showResult_Img.setPixmap(QtGui.QPixmap("OriginalUI/等待.png"))
        else:
            self.label_showPic_shendBack.setPixmap(QPixmap.fromImage(IMG))
            self.label_showName.setText(NAME)
            self.label_showNumber.setText(str(ID))
            self.label_showResult_Img.setPixmap(ICON)



    def show_about_app(self):  # 点击关于此程序
        about_dlg = AboutUI()
        about_dlg.exec()

    def exit_prog(self):
        sys.exit(app.exec_())


class AboutUI(QDialog, Ui_about_app):  # 关于程序窗口
    def __init__(self):
        QDialog.__init__(self)
        self.about_ui = Ui_about_app()
        self.about_ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
