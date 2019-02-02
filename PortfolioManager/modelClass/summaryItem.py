'''
Created on Jun 4, 2017

@author: afunes
'''
from modelClass.position import Position
class SummaryItem:

    def __init__(self, obj):
        self.custodyName = None
        self.assetType = None
        self.valuatedAmount = 0
        self.investedAmount = 0
        self.accumulatedBuyCommissionAmount = 0
        self.accumulatedBuyVATCommissionAmount = 0
        self.realizedPnl = 0
        self.positionPercentage = 0
        self.weightedPnL = 0
        self.netPnL = 0
        if isinstance(obj, Position):
            self.sumPosition(obj)
        elif isinstance(obj, SummaryItem):
            self.sumSubTotal(obj)
    
    def sumSubTotal(self, summaryItem):
        self.valuatedAmount += summaryItem.valuatedAmount
        self.investedAmount += summaryItem.investedAmount 
        self.accumulatedBuyCommissionAmount += summaryItem.accumulatedBuyCommissionAmount
        self.accumulatedBuyVATCommissionAmount += summaryItem.accumulatedBuyVATCommissionAmount
        self.realizedPnl += summaryItem.realizedPnl
        self.positionPercentage += summaryItem.positionPercentage
        self.weightedPnL += summaryItem.weightedPnL
        self.netPnL += summaryItem.netPnL
    
    def sumPosition(self, position):    
        self.custodyName = position.custody.name
        self.assetType = position.asset.assetType
        self.valuatedAmount += position.getValuatedAmount()
        self.investedAmount += position.getInvestedAmount()  
        self.accumulatedBuyCommissionAmount += position.accumulatedBuyCommission
        self.accumulatedBuyVATCommissionAmount += position.accumulatedBuyVATCommission
        self.realizedPnl += position.realizedPnl
        self.positionPercentage += position.getPositionPercentage()
        self.weightedPnL += position.getWeightedPnl()
        self.netPnL += position.getNetPnL()
        
    def addRealizedPnl(self, realizedPnl):
            self.realizedPnl += realizedPnl
        
    def getGrossPnLPercentage(self):
        return (self.valuatedAmount / self.investedAmount -1 ) * 100
    
    def getNetPnLPercentage(self):
        try:
            return (self.valuatedAmount / (self.investedAmount + self.accumulatedBuyCommissionAmount + self.accumulatedBuyVATCommissionAmount) -1 ) * 100
        except Exception as e:
            raise e