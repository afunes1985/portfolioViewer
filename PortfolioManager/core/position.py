'''
Created on Mar 18, 2017

@author: afunes
'''
import datetime
from decimal import Decimal

from sqlalchemy.sql.sqltypes import Float

from core.cache import MainCache


class Position():
    unitCost = Decimal(0)
    rate = Decimal(0)
    totalQuantity = Decimal(0)
    accumulatedAmount = Decimal(0)
    accumulatedBuyCommission = Decimal(0)
    accumulatedBuyVATCommission = Decimal(0)
    accumulatedSellCommission = Decimal(0)
    accumulatedSellVATCommission = Decimal(0)
    realizedPnl = Decimal(0)
    realizedPnlPercentage = Decimal(0)
    marketPrice = Decimal(0)
    marketPriceOrig = 0
    acquisitionDate = 0
    asset = None
    tenor = Decimal(0)
    row = 0
    isMatured = 0
    maturityDate = None
    changePercentage = None
    realizedPnlCorporateEvent = Decimal(0)
    
    def __init__(self, asset, movement):
        self.asset = asset
        #print('New position ' + self.getAssetName())
        self.custody = movement.custody
        self.acquisitionDate = movement.acquisitionDate
        if (self.asset.assetType == 'BOND'):
            self.addBondMovement(movement)
        else:    
            self.addMovement(movement)
    
    def refreshMarketData(self):
        from pricingAPI.PricingInterface import PricingInterface
        if(self.asset.isOnlinePrice):
            if(self.asset.isSIC):
                rfList = PricingInterface.getReferenceDataByAssetNames(self.asset.name+","+self.asset.originName, self.asset.priceSource)
            else:
                rfList = PricingInterface.getReferenceDataByAssetNames(self.asset.name, self.asset.priceSource)     
            for rfRow in rfList:
                self.setReferenceData(rfRow[0], rfRow[1], rfRow[2])

        
    def setReferenceData(self, assetName, price, changePercentage):
        if(assetName == self.asset.name):
            self.setMarketPrice(marketPrice=price)
            self.changePercentage = changePercentage / 100
        elif(assetName == self.asset.originName):
            self.setMarketPriceOrig(Decimal(price)) 
            self.setMarketPrice(marketPrice=Decimal(price), exchangeRate=Decimal(MainCache.usdMXN))
            self.changePercentage = changePercentage / 100
    
    def addPositionToOldPosition(self, position):
        self.realizedPnl += position.realizedPnl
        self.accumulatedSellCommission += position.accumulatedSellCommission
        self.accumulatedSellVATCommission += position.accumulatedSellVATCommission
        self.accumulatedBuyCommission += position.accumulatedBuyCommission
        self.accumulatedBuyVATCommission += position.accumulatedBuyVATCommission
    
    def addMovement(self, movement):   
        quantity = movement.quantity
        grossAmount = movement.grossAmount
        if movement.buySell == 'BUY':
            self.totalQuantity = self.totalQuantity + abs(quantity)#quantity
            self.accumulatedAmount = self.accumulatedAmount + abs(grossAmount)#gross amount
            self.accumulatedBuyCommission += movement.commissionAmount
            self.accumulatedBuyVATCommission += movement.commissionVATAmount
        else:
            self.accumulatedAmount = self.accumulatedAmount - abs(quantity) * self.unitCost
            self.totalQuantity = self.totalQuantity - abs(quantity)#quantity
            sellCommissionAmount = movement.commissionAmount
            sellVATCommissionAmount = movement.commissionVATAmount
            self.accumulatedSellCommission += sellCommissionAmount
            self.accumulatedSellVATCommission += sellVATCommissionAmount
            self.realizedPnl += (grossAmount - (quantity * self.unitCost) - sellCommissionAmount - sellVATCommissionAmount)
        if self.totalQuantity == 0:        
            self.unitCost = 0
            self.accumulatedAmount = 0
        else:
            self.unitCost = self.accumulatedAmount / self.totalQuantity
        
    
    def addBondMovement(self, movement):
        self.totalQuantity = movement.quantity
        self.accumulatedAmount = movement.grossAmount
        self.unitCost = movement.price
        self.rate = movement.rate
        self.tenor = movement.tenor
        self.maturityDate = movement.maturityDate
        today = datetime.datetime.now()
#         if (movement.tax is not None):
#             self.taxAmount = movement.tax.taxAmount
#         else:
#             self.taxAmount  = 0
        self.taxAmount  = 0
        if((self.maturityDate)<today):
            self.isMatured = 1
            self.realizedPnl = self.getNetPnL()
    
    def getAssetName(self):
        return self.asset.name
    
    def getTotalQuantity(self):
        return self.totalQuantity;
    
    def getInvestedAmount(self):
        return self.totalQuantity * self.unitCost;
    
    def getElapsedDays(self):
        elapsedDays = datetime.datetime.now() - self.acquisitionDate
        if (elapsedDays.days > self.tenor):
            return self.tenor
        return elapsedDays.days
    
    def getMaturityDate(self):
        if (self.asset.assetType == 'BOND'):
            return (self.maturityDate).strftime("%Y-%m-%d")
        return None
    
    def getValuatedAmount(self):
        if (self.asset.assetType == 'BOND'):
            return self.accumulatedAmount * (1 + (self.getElapsedDays() * (self.rate / 360))) - self.taxAmount
        else:  
            if (self.marketPrice == 0):
                return self.totalQuantity * 0
            else:
                return self.totalQuantity * self.marketPrice
            
    def getValuatedAmountOrig(self):
        if (self.asset.assetType == 'BOND'):
            return 0
        else:  
            if (self.asset.isSIC):
                return self.totalQuantity * self.marketPriceOrig
            else:
                return 0
    
    def setMarketPriceOrig(self, marketPriceOrig):
        self.marketPriceOrig = Decimal(marketPriceOrig)
    
    def setMarketPrice(self, marketPrice, exchangeRate = None):
        if (self.asset.isSIC):
            self.marketPrice = Decimal(marketPrice) * exchangeRate
            self.marketPriceOrig = Decimal(marketPrice)
        else:
            self.marketPrice = Decimal(marketPrice)
        
    def getMarketPrice(self):
        from pricingAPI.PricingInterface import PricingInterface
        if self.asset.isOnlinePrice:
            if (self.marketPrice == 0):
                self.setMarketPrice(marketPrice=PricingInterface.getMarketPriceByAssetName(self.getMainName(), self.asset.priceSource),
                                    exchangeRate=MainCache.usdMXN)
        return self.marketPrice
    
    def getMarketPriceOrig(self):
        from pricingAPI.PricingInterface import PricingInterface
        if self.asset.isOnlinePrice and self.asset.isSIC:
            if (self.marketPriceOrig == 0):
                self.setMarketPriceOrig(PricingInterface.getMarketPriceByAssetName(self.asset.originName, self.asset.priceSource))
                self.marketPriceOrig = self.marketPriceOrig * Decimal(MainCache.usdMXN)
        return self.marketPriceOrig
    
    def getGrossPnL(self):
        return Decimal(self.getValuatedAmount()) - Decimal(self.getInvestedAmount())
    
    def getNetPnL(self):
        return Decimal(self.getGrossPnL()) - Decimal(self.accumulatedBuyCommission) - Decimal(self.accumulatedBuyVATCommission)
        
    def getGrossPnLPercentage(self):
        try:
            return (self.getValuatedAmount() / self.getInvestedAmount() -1 )
        except Exception as err:
            return 0
    
    def getNetPnLPercentage(self):
        try:
            return (self.getValuatedAmount() / (self.getInvestedAmount() + self.accumulatedBuyCommission + self.accumulatedBuyVATCommission) -1 )
        except Exception as e:
            raise e
    
    def getPositionPercentage(self):
        from core.cache import MainCache
        return Decimal(1) #'FIX' #(self.getValuatedAmount() * 100) / Singleton(MainCache).totalValuatedAmount
    
    def getWeightedPnl(self):
        return self.getGrossPnLPercentage() * self.getPositionPercentage() / 100
    
    def getUnitCostOrRate(self):
        if self.asset.assetType == 'BOND':
            return self.rate * 100 
        else:
            return self.unitCost 
        
    def getMainName(self):
        if self.asset.isSIC:
            return self.asset.originName
        else:
            return self.asset.name
    
    def addRealizedPnlCorporateEvent(self, corporateEventGrossAmount):
        self.realizedPnlCorporateEvent += corporateEventGrossAmount 
        
    def getConsolidatedRealizedPnl(self):
        return self.realizedPnl + self.realizedPnlCorporateEvent
    