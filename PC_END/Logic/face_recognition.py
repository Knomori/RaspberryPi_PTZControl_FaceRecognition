import dlib, os, glob, time
import cv2
import numpy as np
import csv
import pandas as pd
import sqlite3

from Logic import client_parameter


def face_rec():
    try:
        # 声明各个资源路径
        global name, identity_codes
        client_parameter.status_rec = 0  # 识别标志 ，等待中
        predictor_path = client_parameter.predictor_path
        model_path = client_parameter.model_path
        faceDB_path = client_parameter.faceDB_path
        face_sqlite_path = client_parameter.face_sqlite_path
        test_image = client_parameter.face_to_recognition

        # 计算128D描述符的欧式距离
        def compute_dst(feature_1, feature_2):
            feature_1 = np.array(feature_1)
            feature_2 = np.array(feature_2)
            dist = np.linalg.norm(feature_1 - feature_2)
            return dist

        # 加载模型
        detector = dlib.get_frontal_face_detector()  # 人脸特征提取器
        predictor = dlib.shape_predictor(predictor_path)  # 人脸关键点标记
        facerec = dlib.face_recognition_model_v1(model_path)  # 生成面部识别器

        # 读取本地人脸库
        head = []
        for i in range(128):
            fe = "feature_" + str(i + 1)
            head.append(fe)
        face_path = faceDB_path + "feature_all.csv"
        face_feature = pd.read_csv(face_path, names=head)
        face_feature_array = np.array(face_feature)

        # 连接数据读取相关信息
        conn = sqlite3.connect(face_sqlite_path)
        c = conn.cursor()
        cursor = c.execute("SELECT max(recongition_sequence) FROM user_data")
        for row in cursor:
            faces_number = int(str(row[0])) + 1

        frame = cv2.imread(test_image)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detector(gray, 1)  # 检测帧图像中的人脸

        if len(dets) > 0:
            for index, value in enumerate(dets):
                # 获取面部关键点
                shape = predictor(gray, value)

                # 标记人脸
                cv2.rectangle(frame, (value.left(), value.top()), (value.right(), value.bottom()), (0, 255, 0), 2)
                # 提取特征-图像中的68个关键点转换为128D面部描述符，其中同一人的图片被映射到彼此附近，并且不同人的图片被远离地映射。
                face_descriptor = facerec.compute_face_descriptor(frame, shape)  # 进行人脸识别并打上姓名标签
                v = np.array(face_descriptor)

                flag = 0
                for j in range(faces_number):
                    if (compute_dst(v, face_feature_array[j]) < 0.4):  # 人脸匹配，距离小于阈值，表示识别成功，打上标签
                        cursor = c.execute("SELECT name,identity_codes FROM user_data WHERE recongition_sequence = {}".format(j))

                        for row in cursor:
                            name = str(row[0])
                            identity_codes = int(row[1])
                        flag = 1
                        client_parameter.status_rec = 1
                        break
                if (flag == 0):
                    name = "不在数据库中"
                    identity_codes = 404
                    client_parameter.status_rec = 2
        else:
            name = "无法识别到人脸"
            identity_codes = 400
            client_parameter.status_rec = 3

        cursor.close()  # 关闭数据库
        conn.close()
        return name, identity_codes

    except:
        name = "数据文件不完整"
        identity_codes = 415
        client_parameter.status_rec = 4
    return name, identity_codes
