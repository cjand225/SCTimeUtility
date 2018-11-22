'''
Module: ImageProcessThread.py
Purpose: Processes framedata passed from CaptureThread for further processing before being
         sent to the OCR for image recognition
Depends: Queue, Threading, cv2
'''

import threading
import cv2
import numpy as np
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ImageProcessThread(threading.Thread):

    def __init__(self, procQ, detectQ):
        threading.Thread.__init__(self)
        self.ProcessQ = procQ
        self.DetectQ = detectQ
        self.running = True
        self.VidPath = './output.png'


    def run(self):
        self.processFrames()

    def isRunning(self):
        return self.running

    def stop(self):
        self.running = False

    def resume(self):
        self.running = True

    def processFrames(self):


        while self.running:
            if not self.ProcessQ.empty():
                frame = {}

                nextImage = self.ProcessQ.get()
                #currentImage is considered pure frame data from capture cam
                currentImage = self.applyEdgeFilter(nextImage)
                frame["img"] = currentImage

                cv2.imwrite(self.VidPath, currentImage)
                self.DetectQ.put(frame)
            else:
                time.sleep(1)



    def applyEdgeFilter(self, imgData):
        sigma = 0.2
        v = np.median(imgData)
        bilateralImage = cv2.bilateralFilter(imgData, 3, 225, 225)

        hsv = cv2.cvtColor(bilateralImage, cv2.COLOR_BGR2GRAY)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edges = cv2.Canny(hsv, lower, upper)
        return edges