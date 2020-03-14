import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from single_video_UI import Ui_MainWindow

import copy
import msvcrt
import numpy
import cv2

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.VideoTimer = Video()  # videotimer是一个对象
        self.VideoTimer.show.connect(self.setImage)  # changePixmap信号，槽函数是setImage button  push
        self.pushButton.clicked.connect(self.VideoTimer.start) #可以理解为一个控件就是一个实例化的对象

    def setImage(self, frame):
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)#在这里可以对每帧图像进行处理，
        p = convertToQtFormat.scaled(900, 650) #Qt.KeepAspectRatio 保持图片的尺寸
        self.label.setPixmap(QPixmap.fromImage(p).scaled(self.label.width(), self.label.height()))

class Video(QThread):#图像视频流的获取和显示本身就是一个多线程
    show = pyqtSignal(numpy.ndarray)  # 一般来说最简单的信号有clicked pressed released  现在相当于是自定义 pyqtSignal是高级自定义信号

    def __init__(self):
        QThread.__init__(self)
        self.videorun = 0
    def run(self):#这个特殊的符号是不是代表主线程
        self.videorun = 0
        cap = cv2.VideoCapture("./test.mp4")

        while self.videorun == 0 and cap.isOpened():
            ret, image = cap.read()
            try:
                self.show.emit(image)#为何这里也使用self
            except:
                raise Exception("save file executed failed:%s" % e.args)#这个e的用法如何理解 .message 改为 e.args



#这个特殊的符号是不是代表主线程

if __name__=="__main__":
    app=QApplication(sys.argv)
    main=MainWindow()
    main.show()
    sys.exit(app.exec_())

