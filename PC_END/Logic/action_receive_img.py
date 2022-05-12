import socket
from time import sleep
from PyQt5.Qt import (QThread, QMutex, pyqtSignal)
import os
from Logic import client_parameter, face_recognition
import struct


class thread_img_server(QThread):  # 线程1————网络连接与文件的接收
    # signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        #################文件接收的服务器
        print(" 图像接收服务器")

        try:
            client_parameter.IMG_STATUS = "正常"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.bind(('', client_parameter.IMG_PORT))
            s.listen(10)
        except:
            client_parameter.IMG_STATUS = "错误"
            icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
            cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "图像服务器开启失败，请查看相关信息并等待一段时间后尝试手动开启。", icon)
            os.system(cmd)

            print("#######图像服务器出现错误#######")

        while True:
            sock, addr = s.accept()  # addr是一个元组(ip,port)
            self.deal_image(sock, addr)

    def deal_image(self, sock, addr):
        print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口

        while True:
            fileinfo_size = struct.calcsize('128sq')
            buf = sock.recv(fileinfo_size)  # 接收图片名
            if buf:
                filename, filesize = struct.unpack('128sq', buf)
                fn = filename.decode().strip('\x00')
                new_filename = os.path.join('./',
                                            fn)  # 在服务器端新建图片名（可以不用新建的，直接用原来的也行，只要客户端和服务器不是同一个系统或接收到的图片和原图片不在一个文件夹下）

                recvd_size = 0
                fp = open(new_filename, 'wb')

                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = sock.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = sock.recv(1024)
                        recvd_size = filesize
                    fp.write(data)  # 写入图片数据
                fp.close()
            sock.close()
            break

        # sk = socket.socket()
        # # 定义连接的ip和port
        # ip_port = ("", 11123)
        # # 绑定端口
        # sk.bind(ip_port)
        # # 最大连接数
        # sk.listen(5)
        #
        # while True:
        #     # 进入循环接收数据
        #     print("开始循环")
        #     conn, address = sk.accept()
        #
        #     try:
        #         os.remove("face_to_recognition.jpg")
        #         print("原图像已经删除")
        #     except:
        #         print("之前可能没有图片")
        #
        #     print("文件接收开始")
        #
        #     try:
        #         while True:
        #             with open('face_to_recognition.jpg', 'ab') as f:
        #                 # 接收数据
        #                 data = conn.recv(1024)
        #                 if data == b'quit':
        #                     break
        #                 # 写入文件
        #                 f.write(data)
        #                 # 接受完成标志
        #                 conn.send('success'.encode())
        #     except:
        #         print("发送错误")
        #
        #     print("文件接收完成")
        #
        #     sleep(2)
