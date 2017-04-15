'''
Created on Mar 9, 2017

@author: afunes
'''
from datetime import date

from dao.dao import DaoMovement, DaoAsset
from modelClass.constant import Constant
from modelClass.gui import MainWindow
from modelClass.movement import Asset
from modelClass.position import Position


class Engine:
    
    def startApp(self):
        mainWindow = MainWindow()
        positionDict = Engine().buildPositions()
        equityNoSICPositionList = self.getPositionByAssetType(positionDict, 'EQUITY', 0)
        mainWindow.renderPositions(equityNoSICPositionList)
        equitySICPositionList = self.getPositionByAssetType(positionDict, 'EQUITY', 1)
        mainWindow.renderPositions(equitySICPositionList)
        fundPositionList = self.getPositionByAssetType(positionDict, 'FUND', 0)
        mainWindow.renderPositions(fundPositionList)
        bondPositionList = self.getPositionByAssetType(positionDict, 'BOND', 0)
        mainWindow.renderPositions(bondPositionList)
        #=======================================================================
        # mainWindow.renderGrandTotal()
        #=======================================================================
        return mainWindow
        
    def getPositionByAssetType(self, positionDict, assetType ,isSIC):
        positionList = []
        for key, position in positionDict.items():
            if position.asset.assetType == assetType and position.asset.isSIC == isSIC:
                positionList.append(position)
        return positionList
    
    def getAssetDict(self):
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
        
    
    def buildPositions(self):
        assetDict = self.getAssetDict()
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