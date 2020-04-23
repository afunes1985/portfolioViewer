'''
Created on Apr 26, 2017

@author: afunes
'''
from decimal import Decimal

from pricingAPI.PricingInterface import PricingInterface


class MainCache():
    #DICTIONARY
    oldPositionDict = None
    #COMMON VALUE
    usdMXN = None
    
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
    @staticmethod
    def refreshReferenceData():
        USDMXN = PricingInterface().getExchangeRateByCurrency('USD','MXN')
        if USDMXN == 0:
            USDMXN = 1
        MainCache.usdMXN = USDMXN
