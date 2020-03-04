'''
Created on Apr 26, 2017

@author: afunes
'''
from decimal import Decimal

from pricingAPI.PricingInterface import PricingInterface


class MainCache():
    #DICTIONARY
    positionDf = None
    oldPositionDict = None
    summaryDict = None
    corporateEventPositionDictAsset = None
    #COMMON VALUE
    usdMXN = None
    totalValuatedAmount = None
    
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
    @staticmethod
    def refreshReferenceData():
        USDMXN = PricingInterface().getExchangeRateByCurrency('USD','MXN')
        if USDMXN == 0:
            USDMXN = 1
        MainCache.usdMXN = USDMXN