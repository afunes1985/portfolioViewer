'''
Created on Mar 18, 2017

@author: afunes
'''
import datetime
from decimal import Decimal, InvalidOperation

from modelClass.constant import Constant
import requests

class Position():
    assetName = ''
    ppp = 0
    rate = 0
    totalQuantity = 0
    accumulatedAmount = 0
    marketPrice = 0
    movementList = []
    acquisitionDate = 0
    asset = 0
    
    def __init__(self, asset, movement):
        self.asset = asset
        self.assetName = asset.name
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
        else:
            self.accumulatedAmount = self.accumulatedAmount - abs(quantity) * self.getPPP()
            self.totalQuantity = self.totalQuantity - abs(quantity)#quantity
        
        if self.totalQuantity == 0:        
            self.ppp = 0
            self.accumulatedAmount = 0
        else:
            self.ppp = self.accumulatedAmount / self.totalQuantity
    
    def addBondMovement(self, movement):
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
        if (self.asset.assetType == 'BOND'):
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
        if self.asset.isOnlinePrice:
            result = requests.get('http://finance.yahoo.com/d/quotes.csv?s='+self.getAssetName() +'&f=l1')
            self.setMarketPrice(result.text)
        return self.marketPrice
    
    def getPnL(self):
        return self.getValuatedAmount() - self.getInvestedAmount()
    