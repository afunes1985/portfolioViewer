'''
Created on Apr 26, 2017

@author: afunes
'''
from decimal import Decimal

import requests
from engine.engine import Engine
from pricingAPI.PricingInterface import PricingInterface


def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance

class MainCache:
    _instance = None
    positionDict = None
    oldPositionDict = None
    summaryDict = None
    usdMXN = None
    totalValuatedAmount = None
    corpEventList = None
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
    def __init__(self):
        try:
            USDMXN = PricingInterface.getMarketPriceByAssetName('MXN=X')
            if USDMXN == 0:
                USDMXN = 1
            self.setUSDMXN(USDMXN)
        except requests.exceptions.ConnectionError:
            return self.setUSDMXN(1)
        
    def setGlobalAttribute(self, positionDict):    
        self.totalValuatedAmount = Engine.getSubTotalValuatedAmount2(positionDict, 'ALL')