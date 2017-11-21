'''
Created on 8 nov. 2017

@author: afunes
'''
from decimal import Decimal
import logging
import string
import httplib
import json
import requests


class PricingInterface:
    
    @staticmethod
    def getPriceInterfacesDict():
        return dict({"EXCEL":PricingInterfaceExcel, 
                    "YAHOO":PricingInterfaceYahoo,
                    "TRADIER":PricingInterfaceTradier,
                    "ALPHAVANTAGE":PricingInterfaceAlphaVantage}) 
        
    @staticmethod
    def getExchangeRateByCurrency(fromCurrency, toCurrency):
        try:
            return PricingInterface.getPriceInterfacesDict()["ALPHAVANTAGE"].getExchangeRateByCurrency(fromCurrency, toCurrency)
        except Exception as e:
            logging.warning(e)
            return 0
        
    @staticmethod
    def getMarketPriceByAssetName(assetName, priceSource):
        try:
            return PricingInterface.getPriceInterfacesDict()[priceSource].getMarketPriceByAssetName(assetName)
        except Exception as e:
            logging.warning(e)
            return 0
        
    @staticmethod
    def getReferenceDataByAssetNames(assetNames, priceSource):
        try:    
            return PricingInterface.getPriceInterfacesDict()[priceSource].getReferenceDataByAssetNames(assetNames)
        except Exception as e:
            logging.warning(e)
            return []




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
        result = requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+fromCurrency+'&to_currency='+toCurrency+'&apikey=Z09WI322376KBA3P')
        json_data = json.loads(result.text)
        return Decimal(json_data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    
    
    
class PricingInterfaceTradier:
    @staticmethod
    def getMarketPriceByAssetName(assetName):
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
        return Decimal(json_data['quotes']['quote']['last']) 
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        returnList = []
        # Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
        connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
        # Headers
        headers = {"Accept":"application/json",
                   "Authorization":"Bearer XGabnWN7VqBkIuSVvS6QrhwtiQcK"}
        # Send synchronously
        connection.request('GET', '/v1/markets/quotes?symbols='+assetNames, None, headers)
        response = connection.getresponse()
        content = response.read()
        json_data = json.loads(content)
        if isinstance(json_data['quotes']['quote'], list): 
            for row in json_data['quotes']['quote']:
                returnRow = []
                returnRow.append(row['symbol'])
                returnRow.append(row['last'])
                returnRow.append(row['change_percentage'])
                returnList.append(returnRow)
        else:
            returnRow = []
            returnRow.append(json_data['quotes']['quote']['symbol'])
            returnRow.append(json_data['quotes']['quote']['last'])
            returnRow.append(json_data['quotes']['quote']['change_percentage'])
            returnList.append(returnRow)
        return returnList
    
class PricingInterfaceExcel:
    @staticmethod
    def getMarketPriceByAssetName(assetName):
        return 0
    
    @staticmethod
    def getReferenceDataByAssetNames(assetNames):
        import pandas
        #df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
        df = pandas.read_csv('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv');
        #get the values for a given column
        symbolValues = df['Symbol'].values
        curPriceValues = df['Current Price'].values
        changeValues = df['Change'].values
        returnList = []
        for index, rfRow in enumerate(symbolValues):
            if assetNames == rfRow:
                returnRow = []
                returnRow.append(rfRow)
                currentPrice = curPriceValues[index]
                returnRow.append(round(currentPrice,2))
                change = changeValues[index]
                returnRow.append(round((((currentPrice)/(currentPrice-change)-1)*100), 2))
                returnList.append(returnRow)
        return returnList
