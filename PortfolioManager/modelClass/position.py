'''
Created on Mar 18, 2017

@author: afunes
'''
import datetime
from decimal import Decimal, InvalidOperation

from modelClass.constant import Constant


class Position():
    assetType = ''
    assetName = ''
    ppp = 0
    rate = 0
    totalQuantity = 0
    accumulatedAmount = 0
    marketPrice = 0
    isSic = 0
    movementList = []
    acquisitionDate = 0
    
    def __init__(self, assetName, movement):
        self.assetName = assetName
        self.assetType = movement[Constant.CONST_ASSET_TYPE]
        self.isSIC = movement[Constant.CONST_ASSET_IS_SIC]
        self.acquisitionDate = movement[Constant.CONST_MOVEMENT_ACQUISITION_DATE]
        if (self.assetType == 'CETES'):
            self.addMovementCetes(movement)
        else:    
            self.addMovement(movement)
        
    def addMovement(self, movement):   
        self.movementList.append(movement)
        quantity = movement[Constant.CONST_MOVEMENT_QUANTITY]
        grossAmount = movement[Constant.CONST_MOVEMENT_GROSS_AMOUNT]
        if movement[Constant.CONST_MOVEMENT_BUY_SELL] == 'BUY':
            self.totalQuantity = self.totalQuantity + abs(quantity)#quantity
            self.accumulatedAmount = self.accumulatedAmount + abs(grossAmount)#gross amount
        else:
            self.accumulatedAmount = self.accumulatedAmount - abs(quantity) * self.getPPP()
            self.totalQuantity = self.totalQuantity - abs(quantity)#quantity
        
        if self.totalQuantity == 0:        
            self.ppp = 0
            self.accumulatedAmount = 0
        else:
            self.ppp = self.accumulatedAmount / self.totalQuantity
    
    def addMovementCetes(self, movement):
        self.movementList.append(movement)
        self.totalQuantity = movement[Constant.CONST_MOVEMENT_QUANTITY]
        self.accumulatedAmount = movement[Constant.CONST_MOVEMENT_GROSS_AMOUNT]
        self.ppp = movement[Constant.CONST_MOVEMENT_PRICE]
        self.rate = movement[Constant.CONST_MOVEMENT_RATE]
        
    def getPPP(self):
        return self.ppp
    
    def getAssetName(self):
        return self.assetName
    
    def getTotalQuantity(self):
        return self.totalQuantity;
    
    def getInvestedAmount(self):
        return self.totalQuantity * self.ppp;
    
    def getElapsedDays(self):
        elapsedDays = datetime.datetime.now() - self.acquisitionDate
        return elapsedDays.days
    
    def getValuatedAmount(self):
        if (self.assetType == 'CETES'):
            return self.accumulatedAmount * (1 + (self.getElapsedDays() * (self.rate / 360)))
        else:    
            return Decimal(self.totalQuantity) * self.marketPrice
    
    def getMovementList(self):
        return self.movementList
    
    def setMarketPrice(self, marketPrice):
        try:
            self.marketPrice = Decimal(marketPrice)
        except InvalidOperation:
            self.marketPrice = 0
        
    def getMarketPrice(self):
        return self.marketPrice
    
    def getPnL(self):
        return self.getValuatedAmount() - self.getInvestedAmount()
    