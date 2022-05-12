from time import sleep
import configparser
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox

from OriginalUI import setting
from Logic import raspi_parameter

class Settings_UI(QDialog, setting.Ui_setting_UI):
    def __init__(self):
        QDialog.__init__(self)
        setting.Ui_setting_UI.__init__(self)
        self.setupUi(self)

        # 设置相关按钮仅支持数字
        self.lineEdit_commPort.setValidator(QtGui.QIntValidator())  # 设置只能输入int类型的数据
        self.lineEdit_commPort.setValidator(QtGui.QIntValidator())
        self.lineEdit_imgFrames.setValidator(QtGui.QIntValidator())

        # 连接相关按钮
        self.button_yes.clicked.connect(self.click_modify)
        self.button_cancle.clicked.connect(self.click_cancle)

        # 显示默认的参数（上来就运行）
        self.show_default()

    def click_modify(self):
        host_ip = self.lineEdit_ip.text()
        comm_port = self.lineEdit_commPort.text()
        img_port = self.lineEdit_imgPort.text()
        img_frame = self.lineEdit_imgFrames.text()

        if self.isIpVsAddrLegal(host_ip):#如果ip合法
            reply = QMessageBox.question(self, "最后确认", "    确定要进行修改吗？   ",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:#最终进行修改地方
                raspi_parameter.mutex_ini.lock()
                try:
                    # 读取配置文件
                    config_ini = configparser.ConfigParser()
                    config_ini.read("Logic/Config_Raspi.ini")

                    config_ini.set("Address", "HOST", str(host_ip))
                    config_ini.set("Address", "COMM_PORT", str(comm_port))
                    config_ini.set("Address", "IMG_PORT", str(img_port))
                    config_ini.set("CV", "FRAMES", str(img_frame))

                    config_ini.write(open("Logic/Config_Raspi.ini", "w"))

                    reply = QMessageBox.information(self, "提示", "修改配置成功，请重新启动本程序以应用最新的配置～",
                                                    QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.Yes)
                    print(reply)
                    self.closeEvent(self)

                except:
                    msg_box = QMessageBox(QMessageBox.Warning, "警告", "修改配置出现异常，请稍候再试！")
                    msg_box.exec_()
                raspi_parameter.mutex_ini.unlock()
            else:
                print("放弃修改")
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "服务器地址不合法！\n请输入正确的ip地址！")
            msg_box.exec_()

    def show_default(self):
        print("显示默认值")
        self.lineEdit_ip.setText(raspi_parameter.HOST)
        self.lineEdit_commPort.setText(str(raspi_parameter.COMMUNICATION_PORT))
        self.lineEdit_imgPort.setText(str(raspi_parameter.IMG_PORT))
        self.lineEdit_imgFrames.setText(str(raspi_parameter.NUMBER_TO_SAVE))

    def click_cancle(self):
        self.closeEvent(self)

    # 最终的关闭事件
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()

    # 判断是否是合法的IP地址
    def isIpVsAddrLegal(self,ipStr):
        if '.' not in ipStr:  # 判断字符串里面有没有.
            return False

        # 用.切割ip地址为一个列表
        ip_split_list = ipStr.strip().split('.')
        if len(ip_split_list) != 4:  # 切割后列表必须要有四个元素
            return False

        for i in range(4):
            try:
                ip_split_list[i] = int(ip_split_list[i])
            except:
                print("IP invalid for not number: " + ipStr)  # 每个参数必须为数字，否则校验失败
                exit()  # 退出，不再判断后续的字符串

            if ip_split_list[i] <= 255 and ip_split_list[i] >= 0:  # 每个参数值必须在0-255之间
                pass
            else:
                print("IP invalid: " + ipStr)
                return False

        if int(ip_split_list[0] == 0):  # first 参数 is not 0
            print("ip format wrong")
            exit()  # 退出，不再判断后续的字符串

        return True

