'''
Created on 8 nov. 2017

@author: afunes
'''
from decimal import Decimal
import logging
import string

import requests


class PricingInterface:
    @staticmethod
    def getExchangeRateByCurrency(fromCurrency, toCurrency):
        try:
            return PricingInterfaceAlphaVantage.getExchangeRateByCurrency(fromCurrency, toCurrency)
        except Exception as e:
            logging.warning(e)
            return 0
        
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        try:
            return PricingInterfaceTradier.getMarketPriceByAssetName(assetName)
        except Exception as e:
            logging.warning(e)
            return 0
        
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        try:    
            return PricingInterfaceTradier.getReferenceDataByAssetNames(assetNames)
        except Exception as e:
            logging.warning(e)
            return 0




class PricingInterfaceYahoo:
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetName+'&f=l1')
        return Decimal(result.text)
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetNames+'&f=sl1p2')
        wsResult = string.replace(result.text,'"', '')
        return wsResult.split()




class PricingInterfaceAlphaVantage:
    @staticmethod
    def getExchangeRateByCurrency(fromCurrency, toCurrency):
        import json
        result = requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+fromCurrency+'&to_currency='+toCurrency+'&apikey=Z09WI322376KBA3P')
        json_data = json.loads(result.text)
        return Decimal(json_data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    
    
    
class PricingInterfaceTradier:
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        import httplib
        import json
        # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
        connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
        # Headers
        headers = {"Accept":"application/json",
                   "Authorization":"Bearer XGabnWN7VqBkIuSVvS6QrhwtiQcK"}
        # Send synchronously
        connection.request('GET', '/v1/markets/quotes?symbols='+assetName, None, headers)
        response = connection.getresponse()
        content = response.read()
        json_data = json.loads(content)
        return Decimal(json_data['quotes']['quote']['bid']) 
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetNames+'&f=sl1p2')
        wsResult = string.replace(result.text,'"', '')
        return wsResult.split()
