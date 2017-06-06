'''
Created on Mar 18, 2017

@author: afunes
'''
import datetime
from decimal import Decimal, InvalidOperation

import requests

from modelClass.constant import Constant


class Position():
    unitCost = 0
    rate = 0
    totalQuantity = 0
    accumulatedAmount = 0
    accumulatedBuyCommission = 0
    accumulatedBuyVATCommission = 0
    accumulatedSellCommission = 0
    accumulatedSellVATCommission = 0
    realizedPnl = 0
    realizedPnlPercentage = 0
    marketPrice = 0
    marketPriceOrig = 0
    movementList = []
    acquisitionDate = 0
    asset = None
    tenor = 0
    row = 0
    custodyName = None
    
    def __init__(self, asset, movement):
        self.asset = asset
        self.acquisitionDate = movement[Constant.CONST_MOVEMENT_ACQUISITION_DATE]
        if (self.asset.assetType == 'BOND'):
            self.addBondMovement(movement)
        else:    
            self.addMovement(movement)
        
    def addMovement(self, movement):   
        self.movementList.append(movement)
        quantity = movement[Constant.CONST_MOVEMENT_QUANTITY]
        grossAmount = movement[Constant.CONST_MOVEMENT_GROSS_AMOUNT]
        if movement[Constant.CONST_MOVEMENT_BUY_SELL] == 'BUY':
            self.totalQuantity = self.totalQuantity + abs(quantity)#quantity
            self.accumulatedAmount = self.accumulatedAmount + abs(grossAmount)#gross amount
            self.accumulatedBuyCommission += movement[Constant.CONST_MOVEMENT_COM_AMOUNT]
            self.accumulatedBuyVATCommission += movement[Constant.CONST_MOVEMENT_COM_VAT_AMOUNT]
        else:
            self.accumulatedAmount = self.accumulatedAmount - abs(quantity) * self.unitCost
            self.totalQuantity = self.totalQuantity - abs(quantity)#quantity
            sellCommissionAmount = movement[Constant.CONST_MOVEMENT_COM_AMOUNT]
            sellVATCommissionAmount = movement[Constant.CONST_MOVEMENT_COM_VAT_AMOUNT]
            self.accumulatedSellCommission += sellCommissionAmount
            self.accumulatedSellVATCommission += sellVATCommissionAmount
            self.realizedPnl += (grossAmount - (quantity * self.unitCost) - sellCommissionAmount - sellVATCommissionAmount)
            # self.realizedPnlPercentage =
            
        if self.totalQuantity == 0:        
            self.unitCost = 0
            self.accumulatedAmount = 0
        else:
            self.unitCost = self.accumulatedAmount / self.totalQuantity
        self.custodyName = movement[Constant.CONST_MOVEMENT_CUSTODY] 
    
    def addBondMovement(self, movement):
        self.movementList.append(movement)
        self.totalQuantity = movement[Constant.CONST_MOVEMENT_QUANTITY]
        self.accumulatedAmount = movement[Constant.CONST_MOVEMENT_GROSS_AMOUNT]
        self.unitCost = movement[Constant.CONST_MOVEMENT_PRICE]
        self.rate = movement[Constant.CONST_MOVEMENT_RATE]
        self.tenor = movement[Constant.CONST_MOVEMENT_TENOR]
        self.custodyName = movement[Constant.CONST_MOVEMENT_CUSTODY] 
        
    
    def getAssetName(self):
        return self.asset.name
    
    def getTotalQuantity(self):
        return self.totalQuantity;
    
    def getInvestedAmount(self):
        return self.totalQuantity * self.unitCost;
    
    def getElapsedDays(self):
        elapsedDays = datetime.datetime.now() - self.acquisitionDate
        return elapsedDays.days
    
    def getMaturityDate(self):
        if (self.asset.assetType == 'BOND'):
            return (self.acquisitionDate + datetime.timedelta(days = int(self.tenor))).strftime("%Y-%m-%d")
        return None
    
    def getValuatedAmount(self):
        if (self.asset.assetType == 'BOND'):
            return self.accumulatedAmount * (1 + (self.getElapsedDays() * (self.rate / 360)))
        else:  
            if (self.marketPrice == 0):
                return Decimal(self.totalQuantity) * self.unitCost
            else:
                return Decimal(self.totalQuantity) * self.marketPrice
            
    def getValuatedAmountOrig(self):
        if (self.asset.assetType == 'BOND'):
            return 0
        else:  
            if (self.asset.isSIC):
                return Decimal(self.totalQuantity) * self.marketPriceOrig
            else:
                return 0
    
    def getMovementList(self):
        return self.movementList
    
    def setMarketPriceOrig(self, marketPriceOrig):
        try:
            self.marketPriceOrig = Decimal(marketPriceOrig)
        except InvalidOperation:
            self.marketPriceOrig = 0
    
    def setMarketPrice(self, marketPrice):
        try:
            self.marketPrice = Decimal(marketPrice)
        except InvalidOperation:
            self.marketPrice = 0
        
    def getMarketPrice(self):
        from engine.engine import Engine
        if self.asset.isOnlinePrice:
            try:
                marketPrice = Engine.getMarketPriceByAssetName(self.getAssetName())
                self.setMarketPrice(marketPrice)
            except requests.exceptions.ConnectionError:
                return 0   
        return self.marketPrice
    
    def getMarketPriceOrig(self):
        from engine.engine import Engine
        from core.cache import MainCache
        from core.cache import Singleton
        if self.asset.isOnlinePrice and self.asset.isSIC:
            try:
                self.setMarketPriceOrig(Engine.getMarketPriceByAssetName(self.asset.originName))
                self.marketPriceOrig = self.marketPriceOrig * Singleton(MainCache).usdMXN
            except requests.exceptions.ConnectionError:
                return 0   
        return self.marketPriceOrig
    
    def getGrossPnL(self):
        return self.getValuatedAmount() - self.getInvestedAmount()
    
    def getNetPnL(self):
        return self.getGrossPnL() - self.accumulatedBuyCommission - self.accumulatedBuyVATCommission
        
    def getGrossPnLPercentage(self):
        return (self.getValuatedAmount() / self.getInvestedAmount() -1 ) * 100
    
    def getNetPnLPercentage(self):
        return (self.getValuatedAmount() / (self.getInvestedAmount() + self.accumulatedBuyCommission + self.accumulatedBuyVATCommission) -1 ) * 100
    