'''
Created on 8 nov. 2017

@author: afunes
'''
from decimal import Decimal, InvalidOperation
import string


class PricingInterface:
    
    @staticmethod
    def getExchangeRateByCurrency(fromCurrency, toCurrency):
        return PricingInterfaceAlphaVantage.getExchangeRateByCurrency(fromCurrency, toCurrency)
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        return PricingInterfaceTradier.getMarketPriceByAssetName(assetName)
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        return PricingInterfaceTradier.getReferenceDataByAssetNames(assetNames)

class PricingInterfaceYahoo:
    
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        import requests
        try:
            result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetName+'&f=l1')
            return Decimal(result.text)
        except requests.exceptions.ConnectionError:
            return 0   
        except InvalidOperation:
            return 0
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        import requests
        result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetNames+'&f=sl1p2')
        wsResult = string.replace(result.text,'"', '')
        return wsResult.split()

class PricingInterfaceAlphaVantage:
    
    @staticmethod
    def getExchangeRateByCurrency(fromCurrency, toCurrency):
        import requests
        import json
        try:
            result = requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+fromCurrency+'&to_currency='+toCurrency+'&apikey=Z09WI322376KBA3P')
            json_data = json.loads(result.text)
            return Decimal(json_data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
        except Exception as e:
            return 0
    
class PricingInterfaceTradier:
    
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        import requests
        import httplib
        import json
        # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
        connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
        # Headers
        headers = {"Accept":"application/json",
                   "Authorization":"Bearer XGabnWN7VqBkIuSVvS6QrhwtiQcK"}
        # Send synchronously
        connection.request('GET', '/v1/markets/quotes?symbols='+assetName, None, headers)
        try:
            response = connection.getresponse()
            content = response.read()
            json_data = json.loads(content)
            return Decimal(json_data['quotes']['quote']['bid']) 
        except httplib.HTTPException:
            return 0
        except requests.exceptions.ConnectionError:
            return 0   
        except InvalidOperation:
            return 0
        except Exception as e:
            return 0
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        import requests
        result = requests.get('http://download.finance.yahoo.com/d/quotes.csv?s='+assetNames+'&f=sl1p2')
        wsResult = string.replace(result.text,'"', '')
        return wsResult.split()
