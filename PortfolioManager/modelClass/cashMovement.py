'''
Created on Jan 13, 2018

@author: afunes
'''
from modelClass.constant import Constant


class CashMovement():
    
    def __init__(self, cashMovementRow):
        if(cashMovementRow is not None):
            self.setAttr(cashMovementRow[0], cashMovementRow[1], cashMovementRow[2], cashMovementRow[3], cashMovementRow[4], cashMovementRow[5], cashMovementRow[6])
            
    def setAttr(self, OID, amount, inOut, custodyOID, movementDate, comment, externalID, assetOID = None):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        self.OID = OID
        self.amount = amount
        self.inOut = inOut
        self.custody = mainCache.custodyDictOID[custodyOID]
        self.movementDate = movementDate
        self.comment = comment
        self.externalID = externalID
        self.asset = mainCache.assetDictOID.get(assetOID,None)
        self.tax = None
        
    def getMovementType(self):
        return Constant.CONST_MOVEMENT_TYPE    
    
    def getMovementSubType(self):
        return Constant.CONST_CASH_MOVEMENT_SUB_TYPE