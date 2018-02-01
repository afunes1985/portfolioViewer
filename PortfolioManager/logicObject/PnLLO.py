'''
Created on 29 ene. 2018

@author: afunes
'''
class PnLLO():
    
    def setCashMovement(self, cashMovementList):
        self.cashMovementList = cashMovementList
        
    def getTotalCashIn(self):
        totalCashIn = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == "IN":
                totalCashIn += cashMovement.amount
        return totalCashIn
    
    def getTotalCashOut(self):
        totalCashOut = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == "OUT":
                totalCashOut += cashMovement.amount
        return totalCashOut
    
    def calculatePnl(self):
        from engine.engine import Engine
        self.totalCashIn = self.getTotalCashIn()
        self.totalCashOut = self.getTotalCashOut()
        self.finalPosition = Engine.getTotalValuatedAmount()
        self.initialPosition = 0
        self.pnlAmount =  self.finalPosition - self.initialPosition - (self.totalCashIn - self.totalCashOut)
        self.tir = (self.pnlAmount / (self.initialPosition + (self.totalCashIn - self.totalCashOut)))*100
