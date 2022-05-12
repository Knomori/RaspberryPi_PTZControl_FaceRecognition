from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox
from OriginalUI import setting
from Logic import client_parameter
import configparser


class Setting_Dlg(QDialog, setting.Ui_main_setting):
    def __init__(self):
        QDialog.__init__(self)
        setting.Ui_main_setting.__init__(self)
        self.setupUi(self)

        # 设置相关输入框只支持输入数字
        self.lineEdit_commPort.setValidator(QtGui.QIntValidator())
        self.lineEdit_imgPort.setValidator(QtGui.QIntValidator())

        # 关联按钮
        self.pushButton_modify.clicked.connect(self.click_modify)
        self.pushButton_cancle.clicked.connect(self.click_cancle)

        # 上来就运行
        self.show_default()

    def click_modify(self):
        # 先获取输入的信息
        comm_port = self.lineEdit_commPort.text()
        img_port = self.lineEdit_imgPort.text()
        if self.comboBox_port.currentText() == "不自动切换端口":
            port_occupy = "0"
        else:
            port_occupy = "1"

        if self.comboBox_frequence.currentText() == "高":
            frequence = "0"
        else:
            frequence = "1"

        # 对相关数据进行验证合法性 并继续或者提示
        if self.check_number_validity(comm_port, img_port):
            reply = QMessageBox.question(self, "最后确认", "    确定要进行修改吗？   ",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:  # 最终进行修改地方
                client_parameter.mutex_ini.lock()

                try:
                    # 读取配置文件
                    config_ini = configparser.ConfigParser()
                    config_ini.read("LocalData/Config_PC.ini")

                    config_ini.set("Port","COMMUNICATION_PORT", str(comm_port))
                    config_ini.set("Port","IMG_PORT", str(img_port))
                    config_ini.set("System","PORT_OCCUPY", str(port_occupy))
                    config_ini.set("System","REFRESH_RATE", str(frequence))

                    config_ini.write(open("LocalData/Config_PC.ini", "w"))

                    QMessageBox.information(self, "提示", "修改配置成功，请重关闭程序 1分钟 后再重新启动本程序以应用最新的配置～",
                                                    QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.Yes)
                    # print(reply)
                    self.closeEvent(self)

                except:
                    msg_box = QMessageBox(QMessageBox.Warning, "警告", "修改配置出现异常，请稍候再试！")
                    msg_box.exec_()
                client_parameter.mutex_ini.unlock()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "注意！", "  端口号必须大于1024,且必须小于65535！  ")
            msg_box.exec_()

    # 校验两个端口号是否正确
    def check_number_validity(self, port_number, img_port):
        if port_number == "":
            return False
        if img_port == "":
            return False

        number_1 = int(port_number)
        number_2 = int(img_port)

        if (number_1 > 1024) & (number_1 < 65535):
            if (number_2 > 1024) & (number_2 < 65535):
                return True
            else:
                return False
        else:
            return False

    def show_default(self):
        self.lineEdit_commPort.setText(str(client_parameter.COMMUNICATION_PORT))
        self.lineEdit_imgPort.setText(str(client_parameter.IMG_PORT))
        if client_parameter.PORT_OCCUPY == 0:
            self.comboBox_port.setCurrentIndex(0)
        else:
            self.comboBox_port.setCurrentIndex(1)

        if client_parameter.REFRESH_RATE == 0:
            self.comboBox_frequence.setCurrentIndex(0)
        else:
            self.comboBox_frequence.setCurrentIndex(1)

    def click_cancle(self):
        self.closeEvent(self)

    # 最终的关闭事件
    def closeEvent(self, a0: QtGui.QCloseEvent):
        print("取消加关闭窗口")
        self.close()
