'''
Created on May 4, 2017

@author: afunes
'''

from datetime import datetime
import threading

from core.cache import Singleton, MainCache
from core.constant import Constant
from core.position import Position
from dao.movementDao import MovementDao


class PositionEngine():

    def refreshAll(self, fromDate, toDate):
        mainCache = Singleton(MainCache)
        #mainCache.refreshReferenceData()
        resultPositionDict = self.buildPositions(fromDate, toDate, False)
        mainCache.positionDict = resultPositionDict[Constant.CONST_POSITION_DICT]
        #mainCache.oldPositionDict = resultPositionDict[Constant.CONST_OLD_POSITION_DICT]
        #mainCache.setGlobalAttribute(resultPositionDict[Constant.CONST_POSITION_DICT])
        #mainCache.corporateEventPositionDictAsset = Engine.buildCorporateEventPosition()
        #mainCache.summaryDict = Engine.buildSummaryByCustody(mainCache.positionDict, mainCache.oldPositionDict, mainCache.corporateEventPositionDictAsset)
        #return mainCache
        print(resultPositionDict)
        
    def buildPositions(self, fromDate, toDate, setLastMarketData):
        movementList = MovementDao().getMovementsByDate(fromDate, toDate)
        positionDict = {}
        oldPositionDict = {}
        threads = []
        today = datetime.now().date()
        for movement in movementList:
            position = None
            asset = movement.asset
            assetName = asset.name
            if(asset.assetType == 'BOND'):
                assetName = assetName + str(movement.ID)
            position =  positionDict.get(assetName, None)
            if position == None:
                position = Position(asset, movement)
                positionDict[assetName] = position
            else:           
                position.addMovement(movement)
            #pasa la posicion al viejo diccionario de posiciones si no tiene mas posicion o esta vencida
            if (position.asset.assetType == 'BOND'
                 and ((position.isMatured and today == toDate)
                    or (position.maturityDate.date() < toDate and today != toDate))
                or position.totalQuantity == 0):
                oldPosition =  oldPositionDict.get(assetName, None)
                if oldPosition == None:
                    oldPositionDict[assetName] = position
                else:
                    oldPosition.addPositionToOldPosition(position)#TODO TESTEAR
                positionDict.pop(assetName, None)
        if setLastMarketData:         
            for key, position2 in positionDict.items():
                t = threading.Thread(target=position2.refreshMarketData)
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()
        
        returnDict = {}
        returnDict[Constant.CONST_POSITION_DICT] = positionDict
        returnDict[Constant.CONST_OLD_POSITION_DICT] = oldPositionDict
        return returnDict

