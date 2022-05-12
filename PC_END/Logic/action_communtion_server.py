import time
import sqlite3
from PyQt5.QtCore import QThread, pyqtSignal
import os
import socketserver

from PyQt5.QtWidgets import QMessageBox

from Logic import face_recognition, client_parameter


class thread_communion_server(QThread):  # 线程1————网络连接与文件的接收
    signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        #################用于通信的服务器的服务器
        print(" 文件接收服务器")

        HOST, PORT = "",  client_parameter.COMMUNICATION_PORT

        try:
            client_parameter.COMM_STATUS = "正常"
            server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
            with server:
                server.serve_forever()
        except:
            client_parameter.COMM_STATUS = "错误"
            icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
            cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "通信服务器开启失败，请查看相关信息并等待一段时间后尝试手动开启。", icon)
            os.system(cmd)

            print("#######通信服务器出现错误#######")



#继承StreamRequestHandler类，并重写其中的handle方法，该方法是在每个请求到来之后都会调用
class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        #这里是将传进的数据加上Hello 之后再返回，继承自StreamRequestHandler可以使用wfile这个类文件（file-like）对象
        data = str(self.request.recv(1024), 'utf-8')
        print(data)

        if data == "1":
            data = bytes(data, "utf-8")
            self.wfile.write(data)  # write()方法只能写入bytes类型

        if data == "2":
            name, id = face_recognition.face_rec()  # 已经拿到了识别完成后的name与id

            client_parameter.recongitioned_name = name
            client_parameter.recongitioned_id = id
            client_parameter.is_recongition = True

            data = name + " " + str(id)
            data = bytes(data, "utf-8")
            self.wfile.write(data)  # write()方法只能写入bytes类型

            # 对数据库进行修改
            clocked_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

            client_parameter.mutex_modify_db.lock()  #
            try:
                # 将识别到的人的是否打卡字段的INTEGER值设置为1,同时记录打卡时间（0是未打卡，1是已打卡）
                conn = sqlite3.connect(client_parameter.face_sqlite_path)
                cursor = conn.cursor()
                sql = "update user_data set is_clocked=?,clock_time=? where identity_codes=?"
                changed_data = (1, clocked_time, id)
                cursor.execute(sql, changed_data)
                conn.commit()

                cursor.close()
                conn.close()
            except:
                print("daemon_thread线程数据库修改连接失败")
            client_parameter.mutex_modify_db.unlock()


#该类是实现多请求并发处理，只需要继承socketserver.ThreadingMixIn即可，内部无需多加处理，采用默认方法。
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
