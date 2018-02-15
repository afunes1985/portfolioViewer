'''
Created on 29 ene. 2018

@author: afunes
'''
from decimal import Decimal

from valueObject.PnLVO import PnLVO


class PnLLO():
    
    def setCashMovement(self, cashMovementList):
        self.cashMovementList = cashMovementList
    
    def getTotalCash(self, inOut, custodyOID):
        totalCash = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == inOut and (cashMovement.custody.OID == custodyOID or custodyOID is None):
                totalCash += cashMovement.amount
        return totalCash
       
    def getTotalCashIn(self, custodyOID):
        return self.getTotalCash("IN", custodyOID)
    
    def getTotalWeightedCashIn(self):
        totalWeightedCashIn = 0
        firstOcurrence = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == "IN":
                if firstOcurrence == 0:
                    firstOcurrence = 1 
                    self.date = cashMovement.movementDate
                totalWeightedCashIn += cashMovement.amount * Decimal(((float(436) + (cashMovement.movementDate - self.date).days)) /436)  
        return totalWeightedCashIn
    
    def getTotalCashOut(self, custodyOID):
        return self.getTotalCash("OUT", custodyOID)
    
    def getTotalWeightedCashOut(self):
        totalWeightedCashOut = 0
        firstOcurrence = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == "OUT":
                if firstOcurrence == 0:
                    firstOcurrence = 1 
                    #date = cashMovement.movementDate
                totalWeightedCashOut += cashMovement.amount * Decimal(((float(436) + (cashMovement.movementDate - self.date).days)) /436)  
        return totalWeightedCashOut
    
    def calculatePnL(self):
        pnlCalculationList = []
        pnlCalculationList.append(self.calculateConsolidatedPnl())
        self.calculateCustodyPnL(pnlCalculationList)
        return pnlCalculationList
        
    def calculateConsolidatedPnl(self): 
        return self.calculatePnl(None)
        
    def calculatePnl(self, custodyOID):
        from core.cache import Singleton, MainCache
        from engine.engine import Engine
        mainCache = Singleton(MainCache)
        pnlVO = PnLVO() 
        pnlVO.totalCashIn = self.getTotalCashIn(custodyOID)
        pnlVO.totalCashOut = self.getTotalCashOut(custodyOID)
        pnlVO.totalWeightedCashIn = 0#self.getTotalWeightedCashIn()
        pnlVO.totalWeightedCashOut = 0#self.getTotalWeightedCashOut()
        pnlVO.finalPosition = Engine.getSubTotalValuatedAmountByCustodyOID(mainCache.positionDict, custodyOID)
        pnlVO.initialPosition = 0
        pnlVO.pnlAmount =  pnlVO.finalPosition - pnlVO.initialPosition - (pnlVO.totalCashIn - pnlVO.totalCashOut)
        pnlVO.pnlWeightedAmount =  0#pnlVO.finalPosition - pnlVO.initialPosition - (pnlVO.totalWeightedCashIn - pnlVO.totalWeightedCashOut)
        pnlVO.tir = (pnlVO.pnlAmount / (pnlVO.initialPosition + (pnlVO.totalCashIn - pnlVO.totalCashOut)))*100
        pnlVO.weightedTir = 0#(pnlVO.pnlAmount / (pnlVO.initialPosition + (pnlVO.totalWeightedCashIn - pnlVO.totalWeightedCashOut)))*100
        return pnlVO
        
    def calculateCustodyPnL(self, pnlCalculationList):
        from engine.engine import Engine
        custodyDictOID = Engine.getCustodyDictOID()
        for custodyOID in custodyDictOID.iterkeys():
            pnlCalculationList.append(self.calculatePnl(custodyOID))
        
