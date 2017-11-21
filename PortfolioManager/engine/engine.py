'''
Created on Mar 9, 2017

@author: afunes
'''
import threading

from dao.dao import DaoMovement, DaoAsset, DaoCorporateEvent
from modelClass.constant import Constant
from modelClass.movement import Asset, Movement
from modelClass.position import Position    
from modelClass.summaryItem import SummaryItem
from modelClass.corporateEvent import CorporateEvent


class Engine:
    
    @staticmethod
    def buildSummaryByCustody(positionDict, oldPositionDict):
        summaryDict = {}
        for (positionKey, position) in positionDict.iteritems():
            summaryKey = position.custodyName + position.asset.assetType
            summaryItem = summaryDict.get(summaryKey)
            if (summaryItem == None):
                summaryItem = SummaryItem(position)
                summaryDict[summaryKey] = summaryItem
            else:
                summaryItem.sumPosition(position) 
        for (positionKey, position) in oldPositionDict.iteritems():
            summaryKey = position.custodyName + position.asset.assetType
            summaryItem = summaryDict.get(summaryKey)
            if (summaryItem is not None):
                summaryItem.addRealizedPnl(position.realizedPnl)
        return summaryDict         
    
    @staticmethod
    def getAccRealizedPnl(positionDict):
        accRealizedPnl = 0
        for key, position in positionDict.items():
            accRealizedPnl += position.getNetPnL()
        return accRealizedPnl       
                
    @staticmethod
    def getSubTotalInvestedAmount(positionDict, assetType ,isSIC):
        subTotalInvestedAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalInvestedAmount += position.getInvestedAmount()
        return subTotalInvestedAmount
    
    @staticmethod
    def getSubTotalValuatedAmount2(positionDict, assetType):
        return Engine.getSubTotalValuatedAmount(positionDict, assetType ,None)
    
    @staticmethod
    def getAccPositionPercentage(positionDict, assetType, isSIC):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accPositionPercentage = (accValuatedAmount * 100) / mainCache.totalValuatedAmount
        return accPositionPercentage
    
    @staticmethod
    def getAccGrossPnlPercentage(positionDict, assetType, isSIC):
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        accGrossPnlPercentage = (accValuatedAmount / accInvestedAmount -1 ) * 100
        return accGrossPnlPercentage
    
    @staticmethod
    def getAccWeightedPNL(positionDict, assetType, isSIC):
        accGrossPnlPercentage = Engine.getAccGrossPnlPercentage(positionDict, assetType, isSIC)
        accPositionPercentage = Engine.getAccPositionPercentage(positionDict, assetType, isSIC)
        accWeightedPNL = accGrossPnlPercentage * accPositionPercentage / 100
        return accWeightedPNL
    
    @staticmethod
    def getAccNetPnlPercentage(positionDict, assetType, isSIC):
        accBuyCommissionAmount = Engine.getAccBuyCommissionAmount(positionDict, assetType, isSIC)
        accBuyVATCommissionAmount = Engine.getAccBuyCommissionVATAmount(positionDict, assetType, isSIC)
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        subTotalNetPnlPercentage = (accValuatedAmount / (accInvestedAmount + accBuyCommissionAmount + accBuyVATCommissionAmount) -1 ) * 100
        return subTotalNetPnlPercentage
    
    @staticmethod
    def getTotalValuatedAmount():
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        return mainCache.totalValuatedAmount
    
    @staticmethod
    def getSubTotalValuatedAmount(positionDict, assetType ,isSIC):
        subTotalValuatedAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalValuatedAmount += position.getValuatedAmount()
        return subTotalValuatedAmount
    
    @staticmethod
    def getAccBuyCommissionAmount(positionDict, assetType ,isSIC):
        accBuyCommissionAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                accBuyCommissionAmount += position.accumulatedBuyCommission
        return accBuyCommissionAmount
    
    @staticmethod
    def getAccBuyCommissionVATAmount(positionDict, assetType ,isSIC):
        accuBuyVATCommission = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                accuBuyVATCommission += position.accumulatedBuyVATCommission
        return accuBuyVATCommission
    
    @staticmethod
    def getAccRealizedPnL(positionDict, assetType ,isSIC):
        accRealizedPnl = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            accRealizedPnl += position.realizedPnl
        return accRealizedPnl
    
    @staticmethod
    def getPositionByAssetType(positionDict, assetType ,isSIC):
        positionList = []
        for key, position in positionDict.items():
            if assetType == 'ALL' or (position.asset.assetType == assetType and position.asset.isSIC == isSIC):
                positionList.append(position)
        return positionList
    
    @staticmethod
    def getSubtotalGrossPNL(positionDict, assetType ,isSIC):
        subTotalGrossPNL = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                subTotalGrossPNL += position.getGrossPnL()
        return subTotalGrossPNL
    
    @staticmethod
    def getAccNetPNL(positionDict, assetType ,isSIC):
        subTotalNetPNL = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                subTotalNetPNL += position.getNetPnL()
        return subTotalNetPNL
    
    @staticmethod
    def getPortfolioPercentage(positionDict, valuatedAmount):
        totalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, 'ALL', 0)
        return (valuatedAmount * 100) / totalValuatedAmount
        
    @staticmethod
    def getAssetDict():
        assetRS = DaoAsset().getAssetList()
        assetDict = {}
        for (assetRow) in assetRS:
            asset = Asset(assetRow)
            assetDict[asset.name] = asset
        return assetDict 
        
    @staticmethod
    def buildPositions(fromDate, toDate):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        assetDict = Engine.getAssetDict()
        movementRS = DaoMovement.getMovementsByDate(fromDate, toDate)
        positionDict = {}
        oldPositionDict = {}
        position = None
        threads = []
        previousAssetName  = None
        position = None
        for (movement) in movementRS:
            asset = assetDict.get(movement[Constant.CONST_ASSET_NAME])
            assetName = asset.name
            if previousAssetName is None:
                previousAssetName = asset.name
            if(asset.assetType == 'BOND'):
                assetName = assetName + str(movement[Constant.CONST_MOVEMENT_OID])
              
            if position == None:
                    position = Position(asset, movement)
                        
            if previousAssetName == assetName:
                    position.addMovement(movement)
            else:
                if (position.isMatured or position.totalQuantity == 0):
                    oldPositionDict[assetName] = position
                else:
                    positionDict[assetName] = position
                position = Position(asset, movement)
                previousAssetName = asset.name
                    
        #print(datetime.datetime.now())
        for key, position2 in positionDict.items():
            t = threading.Thread(target=position2.refreshMarketData)
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        #print(datetime.datetime.now())
        mainCache.positionDict = positionDict
        mainCache.oldPositionDict = oldPositionDict
        mainCache.setGlobalAttribute(positionDict)
    
    @staticmethod
    def getCorporateEventList(self):
        resultList = []
        resultSet = DaoCorporateEvent.getCorporateEventList()
        for (row) in resultSet:
            o = CorporateEvent(row)
            resultList.append(o)
        return resultList
    
    @staticmethod
    def getMovementListByAsset(assetName, fromDate, toDate):
        movementRS = DaoMovement.getMovementsByAsset(assetName, fromDate, toDate)
        movementList = []
        for (movementRow) in movementRS:
            movement = Movement(movementRow)
            movementList.append(movement)
        return movementList
            