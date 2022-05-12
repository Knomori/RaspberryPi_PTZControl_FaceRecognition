import sys

import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

import setting_ui
from Logic import video_detect, thread_daemon
from OriginalUI import MainWindow


class Main(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        # 初始化
        QMainWindow.__init__(self)
        MainWindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 关联按钮
        self.button_setting.clicked.connect(self.click_setting)

        # 上来就开始执行
        self.thread_video_detect()
        self.thread_daemon()

    # 显示控制
    def statusBar_show15(self, text_to_show):  # 显示statusBar 15秒
        self.statusbar.showMessage(text_to_show, 15000)

    def statusBar_show(self, text_to_show):  # 一直显示statusBar
        self.statusbar.showMessage(text_to_show)

    def show_status(self, NAME, ID, ICON, STATUS_BAR):
        self.label_show_name.setText(NAME)
        self.label_show_id.setText(ID)
        self.label_show_status.setPixmap(ICON)
        self.statusbar.showMessage(STATUS_BAR)

    def show_img(self, img):
        show = cv2.resize(img, (800, 600))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                 QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.show_video.setPixmap(QPixmap.fromImage(showImage))

    def thread_video_detect(self):
        self.thread_show = video_detect.thread_video_detect()
        self.thread_show.signal.connect(self.show_img)
        self.thread_show.start()

    def thread_daemon(self):
        self.thread_daemon_raspi = thread_daemon.daemon()
        self.thread_daemon_raspi.signal.connect(self.show_status)
        self.thread_daemon_raspi.start()

    def click_setting(self):
        setting_dlg = setting_ui.Settings_UI()
        setting_dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
