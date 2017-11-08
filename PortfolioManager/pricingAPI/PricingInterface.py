'''
Created on 8 nov. 2017

@author: afunes
'''
from decimal import Decimal, InvalidOperation
import string

import requests


class PricingInterface:
    
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        try:
            result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetName+'&f=l1')
            return Decimal(result.text)
        except requests.exceptions.ConnectionError:
            return 0   
        except InvalidOperation:
            return 0
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetNames+'&f=sl1p2')
        wsResult = string.replace(result.text,'"', '')
        return wsResult.split()