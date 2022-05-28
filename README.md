# Raspberry Pi PTZControl Face Tracking and Recognition
## 项目简介

该项目是基于树莓派使用CSI相机和云台的人脸追踪和识别的打卡系统项目。该项目是毕设的一个组成部分，该项目还有很多地方设计可能并不是很完善，因此期待您的加入，也欢迎您不断完善它。如果您是想学习该项目是如何实现的，也非常欢迎您来下载并且尝试运行它，它非常容易在您的设备上运行起来。

该项目的原理是在树莓派端实现使用CSI摄像头对人脸视频流的捕获，根据人脸所在的位置来控制云台上的舵机将舵机上的摄像机位置始终朝向人脸的方向。在等待到画面稳定之后，树莓派端将会保存该图像，随后发送给电脑端的程序进行人脸身份的识别，最后将识别结果发送回树莓派端并进行显示。由于本身是一个打卡系统，所以PC端还有相关的打卡功能。PC端的主要工作是承担对新导入人脸数据的训练以及数据集的生成、人脸识别以及相关的打卡功能。

## 如何运行本项目

本项目分为树莓派端和PC端，分别在两个文件夹内。在建立工程文件夹的时候请直接分别将两个项目建立在这两个文件夹之下！

由于本项目设计较多的数据文件，并且在上传GitHub已经将相关的数据集做了脱敏处理，因此您可能需要自行将这些文件以及文件夹补充齐全。下面是您需要自行在项目中补充的文件。

- **新建`user_database.db`数据库文件：**

  你需要自己新建一个名为`user_database.db`的SQLite数据库文件，它的路径在`RaspberryPi_PTZControl_FaceRecognition/PC_END/LocalData/`下，你需要按照下面的信息来创建这个SQLite数据库文件，你可以使用DB-Browser For SQLite这个软件来进行创建。

  ![数据库创建信息](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/数据库表定义.png)

或者您也可以使用上面给出的SQL语言来快速创建。

- **新建三个文件夹：**

  在`RaspberryPi_PTZControl_FaceRecognition/PC_END/LocalData/`下，你需要自行创建两个文件夹，名称分别为`Faces`、`FaceFeatureDB`和`Temp_Face`，你不需要向文件夹里面填充数据，程序会根据你到时候导入的人脸以及身份信息自行生成文件夹里的内容信息。

在创建完所需要的环境之后，这个文件夹下的文件看起来像下面这样：

![](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/路径内留存的文件.png)

- **配置软件运行环境：**

在完成了新建上述文件夹与数据库文件之后，你还需要创建软件的运行环境。

在树莓派上，你只需要用pip安装`opencv-python`这个包即可。

在PC端上，你可以用anaconda来管理Python的虚拟环境，首先新建一个用来存放虚拟环境的文件夹，接着创建Python3.7的虚拟环境，所需要的包已经在`requirements.txt`有所说明，安装即可。如果你使用的是Arch Linux，有**可能**会遇到导入了所有包但是还是部分报错，这些错误包括但不限于：无法找到pyqt的xcb；无法像文本框中输入文字。如果遇到了上述两错误可以直接在系统中找到相应的包，然后复制到你新建本工程时使用的虚拟环境文家家下的相关库应该存放的地方。如果还是不行的话建议使用Windows或其他Linux发行版。

- [x] 树莓派的系统：

![树莓派端环境](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/树莓派环境.png)

- **配置硬件环境**

创建完运行环境后下面来看这线怎么连。

用树莓派的GPIO口连接到舵机，GPIO17控制线控制垂直方向转动的舵机、GPIO27号控制水平方向转动的舵机。连接线路是这样的：（注意GPIO编号和引脚顺序编号是不一样的）

![连接方式](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/树莓派与舵机的连接画面.png)

![GPIO对照](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/GPIO对照表.png)

连接完成之后大概是这个样子：

![连接好线路的实物图](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/连接线路实物.png)

在你创建完成好了上述文件之后，并且配置了运行环境后，就可以运行它了。在PC端，您可以直接运行`main.py`文件，或者是用PyCharm直接执行这个文件，如果你配置好了本地运行环境和所需要的依赖包的话，不出意外应该可以正常运行。树莓派端的软件也是同样的道理，同样也是main.稍后会对环境配置方面进行一些提示。

## 运行截图

### PC端部分截图：

![主界面（已打码）](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/主界面.png)

![菜单](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/菜单.png)

![](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/数据导入页面.png)

![关于本程序画面](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/关于本程序.png)

### 树莓派端部分截图：

![树莓派端主画面](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/树莓派端.png)

![树莓派端设置画面](/home/knomori/Desktop/RaspberryPi_PTZControl_FaceRecognition/README-PIC/树莓派端设置画面.png)









