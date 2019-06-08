'''
Created on May 4, 2017

@author: afunes
'''
from PySide import QtGui, QtCore

from core.cache import Singleton, MainCache
from engine.engine import Engine
from frame.MainWindow import MainWindow
from modelClass.constant import Constant


class MainEngine(object):
    _instance = None

    def refreshAll(self, fromDate, toDate):
        progressBar = QtGui.QProgressDialog("Progress", "Stop", 0, 10)
        progressBar.setLabelText("BUILD POSITION")
        progressBar.setValue(1)
        progressBar.setWindowModality(QtCore.Qt.WindowModal)
        progressBar.setMinimumDuration(0)
        mainCache = Singleton(MainCache)
        mainCache.refreshReferenceData()
        self.mainWindow = MainWindow()
        self.mainWindow.clearTable()
        resultPositionDict = Engine.buildPositions(fromDate, toDate, True)
        mainCache.positionDict = resultPositionDict[Constant.CONST_POSITION_DICT]
        mainCache.oldPositionDict = resultPositionDict[Constant.CONST_OLD_POSITION_DICT]
        mainCache.setGlobalAttribute(resultPositionDict[Constant.CONST_POSITION_DICT])
        mainCache.corporateEventPositionDictAsset = resultPositionDict[Constant.CONST_CORPORATE_POSITION_DICT]
        progressBar.setLabelText("EQUITY")
        progressBar.setValue(3)
        self.mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 0)
        progressBar.setLabelText("EQUITY-SIC")
        progressBar.setValue(6)
        self.mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 1)
        progressBar.setLabelText("FUND")
        progressBar.setValue(7)
        self.mainWindow.renderPositions(mainCache.positionDict, 'FUND', 0)
        progressBar.setLabelText("BOND")
        progressBar.setValue(8)
        self.mainWindow.renderPositions(mainCache.positionDict, 'BOND', 0)
        progressBar.setValue(9)
        self.mainWindow.renderSubtotal(mainCache.positionDict, 'ALL', 0)
        progressBar.setLabelText("CORPORATE EVENT")
        progressBar.setValue(10)
        self.mainWindow.renderCorpEvent(mainCache.corporateEventPositionDictAsset)
        #======================================================================
        mainCache.summaryDict = Engine.buildSummaryByCustody(mainCache.positionDict, mainCache.oldPositionDict)
        self.mainWindow.renderSummary(mainCache.summaryDict)
        self.mainWindow.renderGeneralInfoPanel(mainCache.usdMXN)
        
