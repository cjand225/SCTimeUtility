import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


from Table import Table
from ButtonWidget import ButtonWidget
from VisionWidget import VisionWidget
from LogWidget import LogWidget


class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        # initialize Window
        self.initMainWindow()

        # setup Menu Bar
        self.initMainMenu()

        # setup widgets

        self.initButtonWidget()
        self.initVisionWidget()
        self.initLogWidget()
        self.initTableWidget()

        # initialize gui
        self.initUi()

    def initMainWindow(self):
        self.mainWindow = loadUi('./../resources/Buttons.ui')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Main Window")
        # keeps only toolbar for main App
        self.resize(800,0)
        #centers window
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))


    # Overloads closeEvent function to define what happens when main window X is clicked
    def closeEvent(self, a0: QCloseEvent):
         self.initCloseDialog()
         retval = self.msg.exec()  #grabs event code from Message box execution
         print(retval)
         if retval == 1:    #if OK clicked - Close
             a0.accept()
             self.mTable.close()
             self.mButton.close()
             self.mVision.close()
             self.close()
         #if Cancel or MessageBox is closed - Ignore the signal
         if retval == 0:
             a0.ignore()

    def close(self):
        exit(0)

    def initCloseDialog(self):
        self.msg = QDialog()
        self.msg.ui = loadUi('./../resources/QuitDialog.ui', self.msg)
        self.msg.show()


    def initMainMenu(self):
        mBar = self.menuBar()
        mList = [None] * 4

        self.menuList = ["File", "Edit", "View", "Help"]
        self.mActions = [["New", "Open", "Export", "Quit"], ["Cut", "Copy", "Paste"], ["Table", "Log", "Semi-Auto", "Auto"], ["About"]]

        for i in range(4):
            mList[i] = mBar.addMenu(self.menuList[i])
            for action in self.mActions[i]:
                mList[i].addAction(action)
            # set Bindings for handler functions for menus
            if i == 0:
                mList[i].triggered[QAction].connect(self.handleFileMenu)
            if i == 1:
                mList[i].triggered[QAction].connect(self.handleEditMenu)
            if i == 2:
                mList[i].triggered[QAction].connect(self.handleViewMenu)


    # Initalize/show ui components here
    def initUi(self):
        self.show()

    # handles TableWidget stuff
    def initTableWidget(self):
        self.mTable = Table()

    def initButtonWidget(self):
        self.mButton = ButtonWidget()

    def initVisionWidget(self):
        self.mVision = VisionWidget()

    def initLogWidget(self):
        self.mLog = LogWidget()

    #placeholder function
    def handleFileMenu(self, action):
        print("hi")

    # placeholder function
    def handleEditMenu(self, action):
        print("hi")

    def handleViewMenu(self, action):
        if action.text() == "Table":
            self.toggleTableWidget()
        if action.text() == "Log":
            self.toggleLogWidget()
        if action.text() == "Semi-Auto":
            self.toggleButtonWidget()
        if action.text() == "Auto":
            self.toggleVisionWidget()

    # placeholder function
    def handleHelpMenu(self, action):
        print("hi")

    #---------Widget Toggle Effects------------
    def toggleTableWidget(self):
        if self.mTable.isVisible():
            self.mTable.hide()
        else:
            self.mTable.show()

    def toggleButtonWidget(self):
        if self.mButton.isVisible():
            self.mButton.hide()
        else:
            self.mButton.show()

    def toggleVisionWidget(self):
        if self.mVision.isVisible():
            self.mVision.hide()
        else:
            self.mVision.show()

    def toggleLogWidget(self):
        if self.mLog.isVisible():
            self.mLog.hide()
        else:
            self.mLog.show()

