from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QComboBox
from PyQt5.uic import loadUi
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog
from enum import IntEnum

import matplotlib.pyplot as plt
import numpy as np


class GraphType(IntEnum):
    LAP_TIME = 0,
    AVG_TIME = 1,
    MIN_TIME = 2,
    MAX_TIME = 3


class Graph(QWidget):
    maxGraphNumber = 100

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.GraphDict = ["Lap vs Time", "Average Lap vs Time", "Minimum Time", "Maximum Time"]
        self.graphedTeamList = []
        self.currentGraphType = self.GraphDict[GraphType.LAP_TIME]
        self.currGraphNum = 1
        self.inMinutes = False

        self.teamList = []

        self.initUI()
        self.addGraphs()
        self.handleUpdate(self.teamList)
        self.bindListeners()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    # add graph types
    def addGraphs(self):
        for graph in self.GraphDict:
            self.GraphTypes.addItem(graph)

    def bindListeners(self):
        self.ApplyGraphBtn.clicked.connect(self.drawGraph)
        # action listener for graph type
        self.GraphTypes.activated[str].connect(self.typeChosen)
        # add team list listener
        self.ChosenTeamList.itemDoubleClicked.connect(self.chosenTeamClick)
        self.MinuteButton.toggled.connect(self.timeToggle)
        # add action listener to team choice
        self.TeamChoiceBox.activated.connect(self.teamChosen)

    def updateTeamList(self, newTeamList):
        self.teamList = newTeamList

    def populateTeamChoiceBox(self):
        self.graphedTeamList = []
        self.currGraphNum = 1
        index = 0


        for car in self.teamList:
            print(car.getOrg())
            self.TeamChoiceBox.addItem(str(car.getOrg()), index)
            index += 1

    def timeToggle(self):
        self.inMinutes = self.MinuteButton.isChecked()

    def handleUpdate(self, newTeamList):
        self.updateTeamList(newTeamList)
        self.populateTeamChoiceBox()

    def drawGraph(self):
        if self.currentGraphType == self.GraphDict[GraphType.LAP_TIME]:
            self.lapVsTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.AVG_TIME]:
            self.avgLapVsTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.MIN_TIME]:
            self.minTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.MAX_TIME]:
            self.maxTimeGraph()

    def teamChosen(self, index):
        self.addTeamToGraphList(self.TeamChoiceBox.itemData(index))

    def addTeamToGraphList(self, index):
        # check for space in list
        if len(self.graphedTeamList) >= self.maxGraphNumber:
            return False

        # if not in list add it
        if self.teamList[index] not in self.graphedTeamList:
            self.ChosenTeamList.addItem(self.teamList[index].getOrg())
            self.graphedTeamList.append(self.teamList[index])
            return True
        return False

    def removeTeamFromGraphList(self, teamName):
        # search graph list and remove found element
        for i in range(len(self.graphedTeamList)):
            team = self.graphedTeamList[i]
            if team.getOrg() == teamName:
                self.graphedTeamList.pop(i)
                return True
        return False

    def chosenTeamClick(self):
        # if the team is double clicked then remove it
        teamName = self.ChosenTeamList.currentItem().text()
        self.removeTeamFromGraphList(teamName)
        # remove the team from the list
        self.ChosenTeamList.takeItem(self.ChosenTeamList.currentRow())

    def typeChosen(self, text):
        # checks that type is valid (in types list)
        if text in self.GraphDict:
            self.currentGraphType = text

    def getElapsed(self, lapList):
        elapsed = []
        if self.inMinutes:
            for lap in lapList:
                elapsed.append(lap.elapsedTime / 60)
        else:
            for lap in lapList:
                elapsed.append(lap.elapsedTime)

        return elapsed

    def lapVsTimeGraph(self):
        # increments the figure number to guarantee new window
        plt.figure(self.currGraphNum)
        self.currGraphNum += 1

        graphRange = np.arange(1.0, len(self.graphedTeamList[0].LapList) + 1, 1.0)

        # plot data
        for team in self.graphedTeamList:
            plt.plot(graphRange, self.getElapsed(team.LapList), label=team.getOrg())

        # set labels
        plt.title('Lap vs Time')
        plt.xlabel('Lap')
        if self.inMinutes:
            plt.ylabel('Time (minutes)')
        else:
            plt.ylabel('Time (seconds)')

        plt.xticks(np.arange(1.0, len(self.graphedTeamList[0].LapList) + 1, 1.0))
        plt.legend()

        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def avgLapVsTimeGraph(self):
        # increments the figure number to guarantee new window
        plt.figure(self.currGraphNum)
        self.currGraphNum += 1

        graphRange = np.arange(1.0, len(self.graphedTeamList[0].LapList) + 1, 1.0)

        # plot team lap averages
        for team in self.graphedTeamList:
            lapAverages = []
            lapList = team.LapList

            # for every lap for current team calculate the average time
            if self.inMinutes:
                for i in range(len(team.LapList)):
                    lapAverages.append(lapList[i].recordedTime / ((i + 1) * 60))
            else:
                for i in range(len(team.LapList)):
                    lapAverages.append(lapList[i].recordedTime / (i + 1))

            plt.plot(graphRange, lapAverages, label=team.getOrg())

        # set labels
        plt.title('Lap vs Average Time')
        plt.xlabel('Lap')
        if self.inMinutes:
            plt.ylabel('Average Time (minutes)')
        else:
            plt.ylabel('Average Time (seconds)')

        plt.xticks(np.arange(1.0, len(self.graphedTeamList[0].LapList) + 1, 1.0))
        plt.legend()

        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def minTimeGraph(self):
        labels = []
        data = []

        # calculate minimum times for teams
        for team in self.graphedTeamList:
            data.append(min(self.getElapsed(team.LapList)))
            labels.append(team.getOrg())

        # send data to bar graph
        if self.inMinutes:
            self.barGraph(data, labels, 'Minimum Times', 'Teams', 'Time (minutes)')
        else:
            self.barGraph(data, labels, 'Minimum Times', 'Teams', 'Time (seconds)')

    def maxTimeGraph(self):
        labels = []
        data = []

        # calculate maximum times for teams
        for team in self.graphedTeamList:
            data.append(max(self.getElapsed(team.LapList)))
            labels.append(team.getOrg())

        # send data to bar graph
        if self.inMinutes:
            self.barGraph(data, labels, 'Maximum Times', 'Teams', 'Time (minutes)')
        else:
            self.barGraph(data, labels, 'Maximum Times', 'Teams', 'Time (seconds)')

    def barGraph(self, data, labels, title, x_axis, y_axis):
        # increments the figure number to guarantee new window
        plt.figure(self.currGraphNum)
        self.currGraphNum += 1

        # graph settings
        # range is 1 because only 1 set of bars
        index = np.arange(1)
        bar_width = .5
        opacity = .8

        # add team to legend and plot their data
        for i in range(len(data)):
            plt.bar(index + bar_width * i, data[i],
                    width=bar_width,
                    label=labels[i],
                    alpha=opacity)

        # set labels
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        # remove x ticks
        plt.xticks(index, ' ')
        # add legend
        plt.legend()

        plt.tight_layout()
        plt.show()
