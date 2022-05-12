from PyQt5.QtCore import QMutex
import configparser

# 服务器/识别相关
is_connect = False  # 服务器连接状态
is_training = True  # 是否在训练模型
is_received = False  # 是否已经获取到了图像
status_rec = 0  # 是否正确识别到人（0：默认等待中， 1：正确识别， 2：人脸不在现有数据库， 3：蓝色提示，dlib未识别到人脸， 4：错误）

# 人脸数据库训练和识别要读取人脸图像文件的路径
path_images_from_camera = "LocalData/Faces/"
path_featureDB = "LocalData/FaceFeatureDB/"
path_featureMean = "LocalData/"
resources_path = "LocalData/"
predictor_path = "LocalData/shape_predictor_68_face_landmarks.dat"
model_path = "LocalData/dlib_face_recognition_resnet_model_v1.dat"
faceDB_path = "LocalData/"
face_sqlite_path = "LocalData/user_database.db"
face_to_recognition = "face_to_recognition.jpg"

# 一些防止资源被占用的互斥锁
mutex_img = QMutex()  # 防止接收文件的时候被拿去读或者删除了（互斥锁）
mutex_modify_db = QMutex()  # 对数据库进行修改的时候的互斥锁

# 识别到了人脸相关
recongitioned_name = ""  # 识别到的人名称
recongitioned_id = 80387  # 识别到的人的id
is_recongition = False  # 是否识别了人

# 添加新人的相关资料
new_person_name = "none"
new_person_id = "404"
new_person_imgPath = "./LocalData/Temp_Face"
status_new_person_name = False  # 各个输入的状态
status_new_person_id = False
is_from_folder = False
is_photoed = False

COMM_STATUS = "错误"
IMG_STATUS = "正常"

mutex_ini = QMutex()  # ini文件读写互斥锁
mutex_ini.lock()
try:
    print("读取了默认的ini参数")

    # 读取配置文件
    config_ini = configparser.ConfigParser()
    config_ini.read("LocalData/Config_PC.ini")

    COMMUNICATION_PORT = config_ini.getint("Port", "COMMUNICATION_PORT")
    IMG_PORT = config_ini.getint("Port", "IMG_PORT")
    PORT_OCCUPY = config_ini.getint("System", "PORT_OCCUPY")    # 端口占用处理方法：0是不自动切换  1是自动切换
    REFRESH_RATE = config_ini.getint("System", "REFRESH_RATE")   # 刷新频率：0是高  1是中等
except:
    print("######## 配置文件读取错误 ########")
mutex_ini.unlock()