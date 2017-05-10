'''
Created on Mar 9, 2017

@author: afunes
'''
import requests

from dao.dao import DaoMovement, DaoAsset
from modelClass.constant import Constant
from modelClass.movement import Asset, Movement
from modelClass.position import Position    


class Engine:
    
    @staticmethod
    def getSubTotalInvestedAmount(positionDict, assetType ,isSIC):
        subTotalInvestedAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalInvestedAmount += position.getInvestedAmount()
        return subTotalInvestedAmount
    
    @staticmethod
    def getSubTotalValuatedAmount(positionDict, assetType ,isSIC):
        subTotalValuatedAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalValuatedAmount += position.getValuatedAmount()
        return subTotalValuatedAmount
    
    @staticmethod
    def getPositionByAssetType(positionDict, assetType ,isSIC):
        positionList = []
        for key, position in positionDict.items():
            if assetType == 'ALL' or (position.asset.assetType == assetType and position.asset.isSIC == isSIC):
                positionList.append(position)
        return positionList
    
    @staticmethod
    def getSubtotalPNL(positionDict, assetType ,isSIC):
        subTotalPNL = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalPNL += position.getPnL()
        return subTotalPNL
    
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
        assetDict = Engine.getAssetDict()
        movementRS = DaoMovement.getMovementsByDate(fromDate, toDate)
        positionDict = {}
        position = 0
        for (movement) in movementRS:
            asset = assetDict.get(movement[Constant.CONST_ASSET_NAME])
            assetName = asset.name
            if(asset.assetType == 'BOND'):
                assetName = assetName + str(movement[Constant.CONST_MOVEMENT_OID])
            position = positionDict.get(assetName)
            if (position is None):
                position = Position(asset, movement)
                positionDict[assetName] = position
            else:    
                position.addMovement(movement)
        return positionDict
    
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
            