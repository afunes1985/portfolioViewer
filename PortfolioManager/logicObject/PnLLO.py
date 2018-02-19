'''
Created on 29 ene. 2018

@author: afunes
'''
from decimal import Decimal

from valueObject.PnLVO import PnLVO


class PnLLO():
    
    def setCashMovement(self, cashMovementList):
        self.cashMovementList = cashMovementList
    
    def setPnlVOlist(self, pnlVOList):
        self.pnlVOList = pnlVOList
    
    def getTotalCash(self, inOut, custodyOID):
        totalCash = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == inOut and (cashMovement.custody.OID == custodyOID or custodyOID is None):
                totalCash += cashMovement.amount
        return totalCash
    
    def getTotalWeightedCash(self, inOut, custodyOID, fromDate, toDate):
        totalWeightedCash = 0
        difFromTo = fromDate.daysTo(toDate)
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == inOut and (cashMovement.custody.OID == custodyOID or custodyOID is None):
                totalWeightedCash += cashMovement.amount * Decimal(((float(difFromTo) - fromDate.daysTo(cashMovement.movementDate))) /difFromTo)  
        return totalWeightedCash
       
    def getTotalCashIn(self, custodyOID):
        return self.getTotalCash("IN", custodyOID)
    
    def getTotalCashOut(self, custodyOID):
        return self.getTotalCash("OUT", custodyOID)
    
    def getTotalWeightedCashIn(self, custodyOID, fromDate, toDate):
        return self.getTotalWeightedCash("IN", custodyOID, fromDate, toDate)
    
    def getTotalWeightedCashOut(self, custodyOID, fromDate, toDate):
        return self.getTotalWeightedCash("OUT", custodyOID, fromDate, toDate)
    
    def calculatePnL(self, fromDate, toDate):
        pnlCalculationList = []
        pnlCalculationList.append(self.calculateConsolidatedPnl(fromDate, toDate))
        self.calculateCustodyPnL(pnlCalculationList, fromDate, toDate)
        return pnlCalculationList
        
    def calculateConsolidatedPnl(self, fromDate, toDate): 
        return self.calculatePnl(None, fromDate, toDate)
        
    def calculatePnl(self, custodyOID, fromDate, toDate):
        from core.cache import Singleton, MainCache
        from engine.engine import Engine
        mainCache = Singleton(MainCache)
        pnlVO = PnLVO() 
        custody = mainCache.custodyDictOID.get(custodyOID)
        if (custody is None):
            pnlVO.itemName = "Total"
        else:
            pnlVO.itemName = custody.name
        pnlVO.totalCashIn = self.getTotalCashIn(custodyOID)
        pnlVO.totalCashOut = self.getTotalCashOut(custodyOID)
        pnlVO.totalWeightedCashIn = self.getTotalWeightedCashIn(custodyOID, fromDate, toDate)
        pnlVO.totalWeightedCashOut = self.getTotalWeightedCashOut(custodyOID, fromDate, toDate)
        pnlVO.finalPosition = Engine.getSubTotalValuatedAmountByCustodyOID(mainCache.positionDict, custodyOID)
        pnlVO.initialPosition = 0
        pnlVO.pnlAmount =  pnlVO.finalPosition - pnlVO.initialPosition - (pnlVO.totalCashIn - pnlVO.totalCashOut)
        pnlVO.pnlWeightedAmount =  pnlVO.finalPosition - pnlVO.initialPosition - (pnlVO.totalWeightedCashIn - pnlVO.totalWeightedCashOut)
        pnlVO.tir = (pnlVO.pnlAmount / (pnlVO.initialPosition + (pnlVO.totalCashIn - pnlVO.totalCashOut)))*100
        pnlVO.weightedTir = (pnlVO.pnlAmount / (pnlVO.initialPosition + (pnlVO.totalWeightedCashIn - pnlVO.totalWeightedCashOut)))*100
        return pnlVO
        
    def calculateCustodyPnL(self, pnlCalculationList, fromDate, toDate):
        from engine.engine import Engine
        custodyDictOID = Engine.getCustodyDictOID()
        for custodyOID in custodyDictOID.iterkeys():
            pnlCalculationList.append(self.calculatePnl(custodyOID, fromDate, toDate))
        
