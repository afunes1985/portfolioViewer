'''
Created on Apr 26, 2017

@author: afunes
'''
from engine.engine import Engine
from decimal import Decimal


def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance

class MainCache:
    _instance = None
    positionDict = None
    summaryDict = None
    usdMXN = None
    
    def setUSDMXN(self, usdMXN):
        self.usdMXN = Decimal(usdMXN)
    
    def __init__(self):
        self.setUSDMXN(Engine.getMarketPriceByAssetName('MXN=X'))