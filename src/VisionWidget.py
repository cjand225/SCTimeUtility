import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VisionWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Vision Widget'
        # default sizing for Widget
        self.width = 500
        self.height = 500
        self.layout = QGridLayout()  # Defines Layout - grid
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.setLayout(self.layout)  # applies layout to widget
        self.show()  # displays widget

    #def initVisionWidget(self):
