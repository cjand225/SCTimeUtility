'''
Module: AppWindow.py
Purpose: Top level view object that handles most view information and talks with the controller to
         recieve data from modal

Depends On: PyQt5, Table.py, SemiAutoWidget.py,
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


from table.Table import Table
from table.SemiAutoWidget import SemiAutoWidget
from video.VisionWidget import VisionWidget
from log.LogWidget import LogWidget
from graph.GraphOptionsWidget import GraphOptions


class AppWindow(QMainWindow):

    def openSemiAuto(self,e):
        self.semiAuto.show()

    def __init__(self):
        super(AppWindow, self).__init__()
        # initialize Window
        self.initMainWindow()

        # initialize gui
        self.initUi()
        self.semiAuto = SemiAutoWidget()
        self.actionSemiAuto.triggered.connect(self.openSemiAuto)

    def initUi(self):
        self.show()

    def initMainWindow(self):
        self.mainWindowUI = loadUi('./../resources/App.ui', self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        #centers window
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def closeEvent(self, a0: QCloseEvent):
        self.semiAuto.close()
