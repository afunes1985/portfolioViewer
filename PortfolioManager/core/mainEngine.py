'''
Created on May 4, 2017

@author: afunes
'''
from PySide import QtGui, QtCore

from core.cache import Singleton, MainCache
from engine.engine import Engine
from frame.mainWindow import MainWindow


class MainEngine(object):
    _instance = None

    def refreshAll(self, fromDate, toDate):
        progressBar = QtGui.QProgressDialog("Progress", "Stop", 0, 10)
        progressBar.setWindowModality(QtCore.Qt.WindowModal)
        progressBar.setMinimumDuration(0)
        mainCache = Singleton(MainCache)
        mainWindow = Singleton(MainWindow)
        mainWindow.clearTable()
        mainCache.positionDict = Engine.buildPositions(fromDate, toDate)
        progressBar.setLabelText("EQUITY")
        progressBar.setValue(3)
        mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 0)
        progressBar.setLabelText("EQUITY-SIC")
        progressBar.setValue(6)
        mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 1)
        progressBar.setLabelText("FUND")
        progressBar.setValue(8)
        mainWindow.renderPositions(mainCache.positionDict, 'FUND', 0)
        progressBar.setLabelText("BOND")
        progressBar.setValue(9)
        mainWindow.renderPositions(mainCache.positionDict, 'BOND', 0)
        progressBar.setValue(10)
        mainWindow.renderSubtotal(mainCache.positionDict, 'ALL', 0)
        #======================================================================
        mainCache.summaryDict = Engine.buildSummaryByCustody(mainCache.positionDict)
        mainWindow.renderSummary(mainCache.summaryDict)
        
