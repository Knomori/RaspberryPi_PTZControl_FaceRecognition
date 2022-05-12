from PyQt5.QtCore import QMutex
import configparser

from PyQt5.QtWidgets import QMessageBox

# 舵机的 GPIO 输出口
rudder_gpioNUM_landscape = 27  # 水平
rudder_gpioNUM_portrait = 17  # 竖直

# 舵机的默认位置
rudder_angle_landscape = 55  # 范围 30-80
rudder_angle_portrait = 35  # 范围 10-50

# 舵机的极限位置
rudder_max_left = 30
rudder_max_right = 80
rudder_max_up = 10
rudder_max_down = 50

# 舵机的现在位置(初始位置仍然是默认位置)
rudder_angleNOW_landscape = rudder_angle_landscape
rudder_angleNOW_portrait = rudder_angle_portrait

# 是否已经连接
is_connect = False

mutex_ini = QMutex()  # ini文件读写互斥锁
mutex_ini.lock()
try:
    print("读取了默认的ini参数")

    # 读取配置文件
    config_ini = configparser.ConfigParser()
    config_ini.read("Logic/Config_Raspi.ini")

    HOST = config_ini.get("Address", "HOST")
    COMMUNICATION_PORT = config_ini.getint("Address", "COMM_PORT")
    IMG_PORT = config_ini.getint("Address", "IMG_PORT")
    NUMBER_TO_SAVE = config_ini.getint("CV", "FRAMES")  # 当连续识别到多少时进行保存
except:
    print("######## 配置文件读取错误 ########")
mutex_ini.unlock()

# 识别相关
is_identify = False  # 是否识别到人脸
is_identify_finish = True  # 是否处理完当前人脸（默认就是还没有识别到人脸，就是空载状态，也就是识别完成的状态）

# 图片文件读写的互斥锁
mutex_img = QMutex()
mutex_sending = QMutex()
