import os
import os.path

dir = './'  # 文件所在的路径


# 找出路径下所有的.ui文件
def listUiFile():
    list = []
    files = os.listdir(dir)
    for filename in files:
        # print(filename)
        if os.path.splitext(filename)[1] == '.ui':
            list.append(filename)

    return list


# 把扩展名未.ui的转换成.py的文件
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


# 通过命令把.ui文件转换成.py文件
def runMain():
    list = listUiFile()
    for uifile in list:
        pyfile = transPyFile(uifile)
        cmd = 'pyuic5 -o {pyfile} {uifile}'.format(pyfile=pyfile, uifile=uifile)
        os.system(cmd)

    # cmd = 'pyuic5 -o pyqt_resorce_file_rc.py pyqt_resorce_file.qrc'  # 这个是图像资源文件，也要转换的
    # os.system(cmd)


if __name__ == "__main__":
    runMain()
