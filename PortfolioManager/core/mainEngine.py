'''
Created on May 4, 2017

@author: afunes
'''

from core.cache import Singleton, MainCache
from engine.engine import Engine
from frame.MainWindow import MainWindow
from core.constant import Constant


class MainEngine(object):
    _instance = None

    def refreshAll(self, fromDate, toDate):
        mainCache = Singleton(MainCache)
        mainCache.refreshReferenceData()
        resultPositionDict = Engine.buildPositions(fromDate, toDate, True)
        mainCache.positionDict = resultPositionDict[Constant.CONST_POSITION_DICT]
        #mainCache.oldPositionDict = resultPositionDict[Constant.CONST_OLD_POSITION_DICT]
        #mainCache.setGlobalAttribute(resultPositionDict[Constant.CONST_POSITION_DICT])
        #Engine.buildCorporateEventPosition()
        #======================================================================
        #mainCache.summaryDict = Engine.buildSummaryByCustody(mainCache.positionDict, mainCache.oldPositionDict, mainCache.corporateEventPositionDictAsset)
        
