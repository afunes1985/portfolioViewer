'''
Created on Mar 9, 2017

@author: afunes
'''
import requests

from dao.dao import DaoMovement, DaoAsset
from modelClass.constant import Constant
from modelClass.movement import Asset, Movement
from modelClass.position import Position    
from modelClass.summaryItem import SummaryItem


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
                summaryItem.addRealizedPnl(position.getNetPnL())         
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
            accBuyCommissionAmount += position.accumulatedBuyCommission
        return accBuyCommissionAmount
    
    @staticmethod
    def getAccBuyCommissionVATAmount(positionDict, assetType ,isSIC):
        accuBuyVATCommission = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
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
            subTotalGrossPNL += position.getGrossPnL()
        return subTotalGrossPNL
    
    @staticmethod
    def getAccNetPNL(positionDict, assetType ,isSIC):
        subTotalNetPNL = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
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
        for (movement) in movementRS:
            asset = assetDict.get(movement[Constant.CONST_ASSET_NAME])
            assetName = asset.name
            if(asset.assetType == 'BOND'):
                assetName = assetName + str(movement[Constant.CONST_MOVEMENT_OID])
            position = positionDict.get(assetName)
            if (position is None):
                position = Position(asset, movement)
                if (position.isMatured):
                    oldPositionDict[assetName] = position
                else:
                    positionDict[assetName] = position
            else:    
                position.addMovement(movement)
        mainCache.setGlobalAttribute(positionDict)
        mainCache.positionDict = positionDict
        mainCache.oldPositionDict = oldPositionDict
    
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        result = requests.get('http://finance.yahoo.com/d/quotes.csv?s='+assetName+'&f=l1')
        return result.text
    
    @staticmethod
    def getMovementListByAsset(assetName, fromDate, toDate):
        movementRS = DaoMovement.getMovementsByAsset(assetName, fromDate, toDate)
        movementList = []
        for (movementRow) in movementRS:
            movement = Movement(movementRow)
            movementList.append(movement)
        return movementList
            