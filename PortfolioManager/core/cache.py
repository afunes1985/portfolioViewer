'''
Created on Apr 26, 2017

@author: afunes
'''
from decimal import Decimal

from pricingAPI.PricingInterface import PricingInterface


# from engine.engine import Engine
#from pricingAPI.PricingInterface import PricingInterface
class MainCache():
    _instance = None
    #DICTIONARY
    positionDf = None
    oldPositionDict = None
    summaryDict = None
    corporateEventPositionDictAsset = None
    #REFERENCE DATA
    custodyDictOID = None
    corporateEventTypeOID = None
    assetDictOID = None
    #COMMON VALUE
    usdMXN = None
    totalValuatedAmount = None
    
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
#     def setGlobalAttribute(self, positionDict):    
#         self.totalValuatedAmount = Engine.getSubTotalValuatedAmount2(positionDict, 'ALL')
    
    @staticmethod
    def refreshReferenceData():
        USDMXN = PricingInterface().getExchangeRateByCurrency('USD','MXN')
        if USDMXN == 0:
            USDMXN = 1
        MainCache.usdMXN = USDMXN