'''
Created on Mar 9, 2017

@author: afunes
'''
from datetime import date

from dao.dao import DaoMovement, DaoAsset
from modelClass.constant import Constant
from modelClass.movement import Asset
from modelClass.position import Position    


class Engine:
    
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
        assetResultSet = DaoAsset().getAssetList()
        assetDict = {}
        for (assetRow) in assetResultSet:
            asset = Asset()
            asset.OID = assetRow[0]
            asset.assetType = assetRow[1]
            asset.name = assetRow[2]
            asset.isSIC = assetRow[3]
            asset.isOnlinePrice = assetRow[4]
            assetDict[asset.name] = asset
        return assetDict 
        
    @staticmethod
    def buildPositions():
        assetDict = Engine.getAssetDict()
        movementList = DaoMovement().getMovementsByDate(date(2001, 7, 14), date(2020, 7, 14))
        positionDict = {}
        position = 0
        for (movement) in movementList:
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