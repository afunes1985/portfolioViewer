'''
Created on Jun 4, 2017

@author: afunes
'''
class SummaryItem:
    custodyName = None
    assetType = None
    valuatedAmount = 0
    #pnlPercentage = 0
    investedAmount = 0
    accumulatedBuyCommissionAmount = 0
    accumulatedBuyVATCommissionAmount = 0
    realizedPnl = 0
    
    def __init__(self, position):
        self.sumPosition(position)
        
    def sumPosition(self, position):    
        self.custodyName = position.custodyName
        self.assetType = position.asset.assetType
        self.valuatedAmount += position.getValuatedAmount()
        self.investedAmount += position.getInvestedAmount()  
        self.accumulatedBuyCommissionAmount += position.accumulatedBuyCommission
        self.accumulatedBuyVATCommissionAmount += position.accumulatedBuyVATCommission
        self.realizedPnl += position.realizedPnl
        
    def addRealizedPnl(self, realizedPnl):
            self.realizedPnl += realizedPnl
        
    def getGrossPnLPercentage(self):
        return (self.valuatedAmount / self.investedAmount -1 ) * 100
    
    def getNetPnLPercentage(self):
        return (self.valuatedAmount / (self.investedAmount + self.accumulatedBuyCommissionAmount + self.accumulatedBuyVATCommissionAmount) -1 ) * 100