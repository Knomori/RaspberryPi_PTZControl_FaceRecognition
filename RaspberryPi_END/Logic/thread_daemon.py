import os
import socket
import struct
import sys
from time import sleep

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap

from Logic import raspi_parameter


class daemon(QThread):  # 守护进程
    signal = pyqtSignal(object, object, object, object)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                response = self.client(raspi_parameter.HOST, raspi_parameter.COMMUNICATION_PORT, "1")
                raspi_parameter.is_connect = True
                if response == "1":
                    self.signal.emit("准备就绪", "Ready", QPixmap("OriginalUI/想法.png"), "主控端已成功连接，目前可以正常提供服务。")  # 初始状态

                if raspi_parameter.is_identify_finish == False:  # 如果正在处理这个人
                    self.signal.emit("正在识别", "Identifying", QPixmap("OriginalUI/查询.png"), "识别中")
                    self.sock_client_image()  # 发送图片

                    # os.remove("face_to_recognition.jpg")

                    response = self.client(raspi_parameter.HOST, raspi_parameter.COMMUNICATION_PORT, "2")  # 表示图像已经发送

                    name_and_id = response.split(" ")
                    name = name_and_id[0]
                    id = name_and_id[1]

                    print("识别到的人是：" + name + " " + id)

                    if id == "404":  # 不再数据库中的情况
                        self.signal.emit("不在现有数据库中", "Not in the database.", QPixmap("OriginalUI/错误.png"), " ")  # 初始状态
                        sleep(2)
                        raspi_parameter.is_identify_finish = True
                    elif id == "400":  # 识别错误
                        self.signal.emit("识别错误", "Identify Errors", QPixmap("OriginalUI/错误.png"), " ")  # 初始状态
                        sleep(2)
                        raspi_parameter.is_identify_finish = True
                    elif id == "415":  # 数据文件不完整
                        self.signal.emit("数据文件不完整", "Incomplete data file", QPixmap("OriginalUI/错误.png"), " ")  # 初始状态
                        sleep(2)
                        raspi_parameter.is_identify_finish = True
                    else:#正确识别到人的情况
                        raspi_parameter.is_identify_finish = True
                        self.signal.emit(name, id, QPixmap("OriginalUI/成功.png"), " ")  # 初始状态

                        print("5秒内不再识别其他人")
                        sleep(5)
                        raspi_parameter.is_identify_finish = True
            except:
                self.signal.emit("正在等待主控端", "Loading", QPixmap("OriginalUI/在线查找.png"), "正在等待主控端连接，目前无法提供服务！")  # 初始状态
                raspi_parameter.is_connect = False
            sleep(0.5)

    def client(self, ip, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall(bytes(message, 'utf-8'))
            response = str(sock.recv(1024), 'utf-8')
            return response

    def sock_client_image(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((raspi_parameter.HOST, raspi_parameter.IMG_PORT))  # 服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
            except socket.error as msg:
                print(msg)
                print(sys.exit(1))
            filepath = "face_to_recognition.jpg"  # 输入当前目录下的图片名 xxx.jpg
            fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                                os.stat(filepath).st_size)  # 将xxx.jpg以128sq的格式打包
            s.send(fhead)

            fp = open(filepath, 'rb')  # 打开要传输的图片
            while True:
                data = fp.read(1024)  # 读入图片数据
                if not data:
                    print('{0} send over...'.format(filepath))
                    break
                s.send(data)  # 以二进制格式发送图片数据
            s.close()
            break  # bu循环发送

    # def img_send(self):
    #     sk = socket.socket()
    #     # 定义连接的ip和port
    #     ip_port = ('127.0.0.1', 9999)
    #     # 服务器连接
    #     sk.connect(ip_port)
    #
    #     with open('face_to_recognition.jpg', 'rb') as f:
    #         # 按每一段分割文件上传
    #         for i in f:
    #             sk.send(i)
    #             # 等待接收完成标志
    #             data = sk.recv(1024)
    #             # 判断是否真正接收完成
    #             if data != b'success':
    #                 break
    #     # 给服务端发送结束信号
    #     sk.send('quit'.encode())
