'''
Created on Apr 26, 2017

@author: afunes
'''
from decimal import Decimal

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
    custodyDictOID = Engine.getCustodyDictOID()
    corporateEventTypeOID = Engine.getCustodyDictOID()
    
    def __init__(self):
        USDMXN = PricingInterface.getExchangeRateByCurrency('USD','MXN')
        if USDMXN == 0:
            USDMXN = 1
        self.setUSDMXN(USDMXN)
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
    def setGlobalAttribute(self, positionDict):    
        self.totalValuatedAmount = Engine.getSubTotalValuatedAmount2(positionDict, 'ALL')