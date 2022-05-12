from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog
from OriginalUI import server_status
from Logic import client_parameter

class Show_ServerStatus(QDialog, server_status.Ui_server_status_dlg):
    def __init__(self):
        QDialog.__init__(self)
        server_status.Ui_server_status_dlg.__init__(self)
        self.setupUi(self)

        # 关联控件
        self.button_close.clicked.connect(self.click_cancle)
        self.button_refresh.clicked.connect(self.click_refresh)

        # 一上来就开始运行
        self.show_default()


    def show_default(self):
        self.label_show_img_status.setText(client_parameter.IMG_STATUS)
        self.label_show_img_port.setText(str(client_parameter.IMG_PORT))
        self.label_show_comm_status.setText(client_parameter.COMM_STATUS)
        self.label_show_comm_port.setText(str(client_parameter.COMMUNICATION_PORT))

    def click_refresh(self):
        self.show_default()

    def click_cancle(self):
        self.closeEvent(self)

    # 最终的关闭事件
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()
