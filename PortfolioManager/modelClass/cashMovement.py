'''
Created on Jan 13, 2018

@author: afunes
'''

class CashMovement():
    
    def __init__(self, cashMovementRow):
        from core.cache import Singleton, MainCache
        if(cashMovementRow is not None):
            mainCache = Singleton(MainCache)
            self.OID = cashMovementRow[0]
            self.amount = cashMovementRow[1]
            self.inOut = cashMovementRow[2]
            self.custody = mainCache.custodyDictOID[cashMovementRow[3]]
            self.movementDate = cashMovementRow[4]
            self.comment = cashMovementRow[5]
            
    def setAttr(self, OID, amount, inOut, custodyOID, movementDate, comment):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        self.OID = OID
        self.amount = amount
        self.inOut = inOut
        self.custody = mainCache.custodyDictOID[custodyOID]
        self.movementDate = movementDate
        self.comment = comment