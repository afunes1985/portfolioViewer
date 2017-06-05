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
    
    def getGrossPnLPercentage(self):
        return (self.valuatedAmount / self.investedAmount -1 ) * 100