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
    #DICTIONARY
    positionDict = None
    oldPositionDict = None
    summaryDict = None
    corpEventDict = None
    corporateEventPositionDict = None
    #REFERENCE DATA
    custodyDictOID = None
    corporateEventTypeOID = None
    assetDictOID = None
    #COMMON VALUE
    usdMXN = None
    totalValuatedAmount = None
    
    
    def __init__(self):
        USDMXN = PricingInterface.getExchangeRateByCurrency('USD','MXN')
        if USDMXN == 0:
            USDMXN = 1
        self.setUSDMXN(USDMXN)
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
    def setGlobalAttribute(self, positionDict):    
        self.totalValuatedAmount = Engine.getSubTotalValuatedAmount2(positionDict, 'ALL')
    
    def refreshReferenceData(self):
        self.custodyDictOID = Engine.getCustodyDictOID()
        self.corporateEventTypeOID = Engine.getCustodyDictOID()
        self.assetDictOID = Engine.getAssetDictOID()