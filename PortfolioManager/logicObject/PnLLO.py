'''
Created on 29 ene. 2018

@author: afunes
'''
from decimal import Decimal


class PnLLO():
    
    def setCashMovement(self, cashMovementList):
        self.cashMovementList = cashMovementList
        
    def getTotalCashIn(self):
        totalCashIn = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == "IN":
                totalCashIn += cashMovement.amount
        return totalCashIn
    
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
    
    def getTotalCashOut(self):
        totalCashOut = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == "OUT":
                totalCashOut += cashMovement.amount
        return totalCashOut
    
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
    
    def calculatePnl(self):
        from engine.engine import Engine
        self.totalCashIn = self.getTotalCashIn()
        self.totalCashOut = self.getTotalCashOut()
        self.totalWeightedCashIn = self.getTotalWeightedCashIn()
        self.totalWeightedCashOut = self.getTotalWeightedCashOut()
        self.finalPosition = Engine.getTotalValuatedAmount()
        self.initialPosition = 0
        self.pnlAmount =  self.finalPosition - self.initialPosition - (self.totalCashIn - self.totalCashOut)
        self.pnlWeightedAmount =  self.finalPosition - self.initialPosition - (self.totalWeightedCashIn - self.totalWeightedCashOut)
        self.tir = (self.pnlAmount / (self.initialPosition + (self.totalCashIn - self.totalCashOut)))*100
        self.weightedTir = (self.pnlAmount / (self.initialPosition + (self.totalWeightedCashIn - self.totalWeightedCashOut)))*100
