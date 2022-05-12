import time
from shutil import copyfile
import os
import xlwt
import sqlite3

from Logic import client_parameter


class Output_Files():
    def output_as_sqlite(self):
        # 拷贝文件到相关目录
        db_file_path = "LocalData/user_database.db"
        localtime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        destination_file = "截至" + localtime + "打卡情况.db"
        copyfile(db_file_path, destination_file)

        # 推送通知
        icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
        cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "已经导出该时段数据情况到SQLite文件", icon)
        os.system(cmd)

    def output_as_excel(self):
        # 新建工作簿然、写入标题和内容
        workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
        sheet1 = workbook.add_sheet("打卡情况")  # 新建sheet
        sheet1.write(0, 0, "数据库识别序号")
        sheet1.write(0, 1, "姓名")
        sheet1.write(0, 2, "身份识别码")
        sheet1.write(0, 3, "是否打卡(0为未打卡，1为已打卡)")
        sheet1.write(0, 4, "打卡时间")

        # 先获取数据，然后进行填充
        try:
            conn = sqlite3.connect(client_parameter.face_sqlite_path)
            c = conn.cursor()
            all_data = c.execute("SELECT recongition_sequence,name,identity_codes,is_clocked,clock_time FROM user_data")

            n = 1
            for data in all_data:
                sheet1.write(n, 0, str(data[0]))
                sheet1.write(n, 1, str(data[1]))
                sheet1.write(n, 2, str(data[2]))
                sheet1.write(n, 3, str(data[3]))
                sheet1.write(n, 4, str(data[4]))

                n = n + 1
            conn.commit()
            c.close()
            conn.close()

            # 写入数据句
            localtime = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
            destination_file = "截至" + localtime + "打卡情况.xlsx"
            workbook.save(destination_file)  # 保存

            # 推送成功通知
            icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
            cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "已经导出该时段数据情况到Excel文件", icon)
            os.system(cmd)

        except:
            # 推送失败通知
            icon = "/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/PC_END/OriginalUI/通知.png"
            cmd = "notify-send  '%s' '%s' --icon '%s'" % ("通知", "数据库访问失败！", icon)
            os.system(cmd)
