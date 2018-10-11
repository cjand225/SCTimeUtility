from PyQt5.QtWidgets import QWidget, QGridLayout, QStyle, QApplication, QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import queue
import cv2

from video.ImageCanvas import ImageCanvas
from video.CaptureThread import CaptureThread

frameQueue = queue.Queue()

class VisionWidget(QWidget):

    def __init__(self):
        super().__init__()
        #video part
        self.image = None

        # default sizing for Widget
        self.width = self.frameSize().width()
        self.height = self.frameSize().height()
        self.layout = QGridLayout()  # Defines Layout - grid

        #thread related - default
        self.resolution = [None] * 2
        self.fps = None
        self.deviceCam = None
        self.captureThread = None

        #adding list of threads before they are instanced
        #self.threadList = [None] * 4

        #Image queue for capture thread
        self.imageQueue = queue.Queue()

        #images from capture thread, aviable for processing
        self.processQueue = queue.Queue()

        #gives context to capture thread
        self.setDevice(0)
        self.setResolution(1920,1080)
        self.setFps(60)


        #initalizers
        self.initUI()
        self.initButton()
        self.initVisionWidget()



    #initalizes Vision Widget Qwidget
    def initUI(self):
        self.ui = loadUi('./../resources/Video.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))

    #initializes Canvas for Qimage to be put onto
    def initVisionWidget(self):
        self.imageWidget = ImageCanvas()
        self.windowWidth = self.imageWidget.frameSize().width()
        self.windowHeight = self.imageWidget.frameSize().height()
        self.imageLayout.addWidget(self.imageWidget)

    #initalizes button that toggles thread
    def initButton(self):
        self.startButton.clicked.connect(self.startThread)
        self.stopButton.clicked.connect(self.stopThread)

    #initalizes thread for grabbing data from capture cam
    def initCaptureThread(self):
        self.captureThread = CaptureThread(self.imageQueue, self.deviceCam, self.resolution[0], self.resolution[1], self.fps)

    def setResolution(self, height, width):
        self.resolution[0] = height
        self.resolution[1] = width

    def setFps(self, frames):
        self.fps = frames

    def setDevice(self, deviceNum):
        self.deviceCam = deviceNum

    #used for binding thread to a button
    def startThread(self):
        self.initCaptureThread()
        self.initTimer()
        self.captureThread.start()

    def stopThread(self):
        if(self.captureThread.isRunning()):
            self.captureThread.stop()
            self.captureThread.join()
            if(self.captureThread.isAlive()):
                print("Thread is still Alive.")
            else:
                print("Thread has Quit.")

    #makes sure thread stops before widget/program is closed
    def closeEvent(self, a0: QCloseEvent):
        if(self.captureThread != None and self.captureThread.isRunning()):
            self.stopThread()
        a0.ignore()
        self.hide()


    #grabs frames from queue that is managed by CaptureThread Class
    def updateFrame(self):
        if not self.imageQueue.empty():
            frame = self.imageQueue.get()
            currentImage = frame["img"]

            imageHeight, imageWidth, imageColors = currentImage.shape
            scaleWidth = float(self.windowWidth) / float(imageWidth)
            scaleHeight = float(self.windowHeight) / float(imageHeight)
            scale = min([scaleWidth, scaleHeight])

            if scale == 0:
                scale = 1

            currentImage = cv2.resize(currentImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            currentImage = cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB)
            height, width, bpc = currentImage.shape
            bpl = bpc * width

            finalImage = QImage(currentImage.data, width, height, bpl, QImage.Format_RGB888)

            self.imageWidget.setImage(finalImage)


    #initalizes a timer to call for repeatedly updating frames
    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1)

