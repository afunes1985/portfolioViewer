'''
Created on Jan 8, 2020

@author: afunes
'''
from dao.assetDao import AssetDao
from dao.movementDao import MovementDao
import pandas as pd
from dao.dao import GenericDao


class MovementEngine():
    
    def getMovementsByDate(self, fromDate, toDate):
        return MovementDao().getMovementsByDate(fromDate, toDate)
    
    def getMovementsForReport(self, fromDate, toDate):
        movement_DF = pd.DataFrame(columns=['Asset Name','Buy Sell','Acquisition Date','Quantity','Price','Gross Amount','Net Amount','Comm %','Comm Amount','Comm VAT Amount', 'Custody'])
        rs = MovementDao().getMovementsForReport(fromDate, toDate)
        for row in rs:
            movement_DF = movement_DF.append(pd.Series([row.name, row.buySell, row.acquisitionDate.strftime("%Y-%m-%d"), row.quantity, row.price, row.grossAmount, row.netAmount, row.commissionPercentage, row.commissionAmount, row.commissionVATAmount, row.custodyName], index=movement_DF.columns), ignore_index=True)
        return movement_DF
    
    def getAssetTypeList(self):
        itemList = AssetDao().getAssetTypeList()
        resultList = []
        for item in itemList:
            resultList.append({'label': item[0], 'value': item[0]})
        return resultList
    
    def getAssetList(self, assetType):
        itemList = AssetDao().getAssetList(assetType)
        resultList = []
        for item in itemList:
            resultList.append({'label': item.getName(), 'value': item.ID})
        return resultList
    
    def getCustodyList(self):
        itemList = AssetDao().getCustodyList()
        resultList = []
        for item in itemList:
            resultList.append({'label': item.name, 'value': item.ID})
        return resultList
    
    def getCustodyByAssetID(self, assetID):
        return AssetDao().getCustodyByAssetID(assetID)
        
    def addMovement(self, movement):
        GenericDao().addObject(objectToAdd=movement, doCommit=True)