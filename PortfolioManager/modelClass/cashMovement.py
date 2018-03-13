'''
Created on Jan 13, 2018

@author: afunes
'''

class CashMovement():
    
    def __init__(self, cashMovementRow):
        if(cashMovementRow is not None):
            self.setAttr(cashMovementRow[0], cashMovementRow[1], cashMovementRow[2], cashMovementRow[3], cashMovementRow[4], cashMovementRow[5], None)
            
    def setAttr(self, OID, amount, inOut, custodyOID, movementDate, comment, externalID ):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        self.OID = OID
        self.amount = amount
        self.inOut = inOut
        self.custody = mainCache.custodyDictOID[custodyOID]
        self.movementDate = movementDate
        self.comment = comment
        self.externalID = externalID