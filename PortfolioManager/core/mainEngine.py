'''
Created on May 4, 2017

@author: afunes
'''
from core.cache import Singleton, MainCache
from engine.engine import Engine
from frame.mainWindow import MainWindow


class MainEngine(object):
    _instance = None

    def refreshAll(self, fromDate, toDate):
        mainCache = Singleton(MainCache)
        mainWindow = Singleton(MainWindow)
        mainWindow.clearTable()
        mainCache.positionDict = Engine.buildPositions(fromDate, toDate)
        mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 0)
        mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 1)
        mainWindow.renderPositions(mainCache.positionDict, 'FUND', 0)
        mainWindow.renderPositions(mainCache.positionDict, 'BOND', 0)
        mainWindow.renderSubtotal(mainCache.positionDict, 'ALL', 0)
