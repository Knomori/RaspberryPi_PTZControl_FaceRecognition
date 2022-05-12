from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox

from Logic import database_access_object
from OriginalUI import check_in_details


class Show_CheckedPage(QDialog, check_in_details.Ui_Dialog):  # 关于程序窗口
    def __init__(self):
        QDialog.__init__(self)
        check_in_details.Ui_Dialog.__init__(self)
        self.setupUi(self)

        self.timer_fresh_statusBar = QtCore.QTimer()
        self.timer_fresh_statusBar.timeout.connect(self.reset_refresh_button)  # 刷新数据 调用

        self.timer_search_statusBar = QtCore.QTimer()
        self.timer_search_statusBar.timeout.connect(self.reset_search_button)  # 搜索 调用

        self.timer_modify_statusBar = QtCore.QTimer()
        self.timer_modify_statusBar.timeout.connect(self.reset_modify_button)  # 修改 调用

        # 关联一下控件
        self.button_refresh.clicked.connect(self.click_refresh)
        self.button_close_page.clicked.connect(self.click_close_page)
        self.button_search.clicked.connect(self.click_search)
        self.button_modify_data.clicked.connect(self.click_modify_daya)

        # 刚开始就开始运行
        self.fill_all_data()

    def fill_all_data(self):  # 填充数据
        all_data = database_access_object.DAO.get_all_data(self)
        self.show_data(all_data)

    def click_refresh(self):
        self.lineEdit.setText("")
        self.fill_all_data()

        icon = QtGui.QIcon()  # 重新设置按钮icon
        icon.addPixmap(QtGui.QPixmap("OriginalUI/正确.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_refresh.setIcon(icon)
        self.timer_fresh_statusBar.start(3000)

    def click_search(self):
        name_to_search = self.lineEdit.text()
        all_data = database_access_object.DAO.get_data_use_name(self, name_to_search)
        self.show_data(all_data)

        icon = QtGui.QIcon()  # 重新设置按钮icon
        icon.addPixmap(QtGui.QPixmap("OriginalUI/正确.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_search.setIcon(icon)
        self.timer_search_statusBar.start(3000)

    def click_modify_daya(self):
        msg = QMessageBox.warning(self, "注意！", "您确认要写入修改的数据吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:  # 确认进行数据修改
            # 修改图标为正在进行修改中
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("OriginalUI/等待.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button_modify_data.setIcon(icon)

            # 先获取所有数据
            all_data_modify = []
            n = 0
            print(self.tableWidget.item(1, 1).text())

            for _ in range(self.tableWidget.rowCount()):
                one_row = [self.tableWidget.item(n, 0).text(), self.tableWidget.item(n, 1).text(),
                           self.tableWidget.item(n, 2).text(), self.tableWidget.item(n, 3).text(),
                           self.tableWidget.item(n, 4).text()]
                all_data_modify.append(one_row)
                n = n + 1
            database_access_object.DAO.modify_new_data(self, all_data_modify)# 通知数据库进行写入操作

            # 修改图标为已完成
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("OriginalUI/正确.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.button_modify_data.setIcon(icon)

            # 刷新当前页面
            self.fill_all_data()
            self.timer_modify_statusBar.start(3000)

    def reset_refresh_button(self):  # 重新设置刷新按钮的图标
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("OriginalUI/刷新.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_refresh.setIcon(icon)
        self.timer_fresh_statusBar.stop()

    def reset_search_button(self):  # 重新设置搜索按钮
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("OriginalUI/搜索.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_search.setIcon(icon)
        self.timer_search_statusBar.stop()

    def reset_modify_button(self):  # 重新设置修改图标按钮
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("OriginalUI/编辑.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_modify_data.setIcon(icon)
        self.timer_modify_statusBar.stop()

    def show_data(self, all_data):
        if all_data:  # 有数据情况
            n = len(all_data)
            self.tableWidget.setRowCount(n)

            # 向列表中填充数据
            n = 0
            for data in all_data:
                self.tableWidget.setItem(n, 0, QtWidgets.QTableWidgetItem(str(data[0])))
                self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem(str(data[1])))
                self.tableWidget.setItem(n, 2, QtWidgets.QTableWidgetItem(str(data[2])))

                if str(data[3]) == "0":
                    self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem("-"))
                elif str(data[3]) == "1":
                    self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem("是"))
                else:
                    self.tableWidget.setItem(n, 3, QtWidgets.QTableWidgetItem("数据有误"))

                self.tableWidget.setItem(n, 4, QtWidgets.QTableWidgetItem(str(data[4])))
                n = n + 1
        else:  # 无数据情况
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("无结果"))
            self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("无结果"))
            self.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("无结果"))
            self.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem("无结果"))
            self.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem("无结果"))

    def click_close_page(self):
        self.close()
