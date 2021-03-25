'''
Created on Apr 18, 2020

@author: afunes
'''
from datetime import datetime
import logging

from base.dbConnector import DBConnector
from base.initializer import Initializer
from core.cache import MainCache
from core.constant import Constant
from dao.cashMovementDao import CashMovementDao
from dao.exchangeRateDao import ExchangeRateDao
from dao.dao import GenericDao
from dao.priceDao import PriceDao
from engine.positionEngine import PositionEngine
from modelClass.currency import ExchangeRate
import pandas as pd
from pricingAPI.PricingInterface import PricingInterfaceExcel, PricingInterface
from tools.tools import getLastWorkingDay

class PnlEngine():
    
    def calculatePnl(self, fromDate, toDate):
        MainCache.refreshReferenceData()
        initDate = datetime(2001, 1, 1).date()
        initialExchangeRateValue = None
        finalExchangeRateValue = None
        initialPositionDict = PositionEngine().buildPositions(fromDate=initDate, toDate=fromDate, setLastMarketData=False)
        if len(initialPositionDict) == 0:
            logging.warning("Empty initial position dict")
        finalPositionDict = PositionEngine().buildPositions(fromDate=initDate, toDate=toDate, setLastMarketData=False)
        if len(finalPositionDict) == 0:
            logging.warning("Empty final position dict")
        # set reference data
        initialExchangeRateValue = self.setReferenceData(positionDict=initialPositionDict[Constant.CONST_POSITION_DICT], date=fromDate)
        finalExchangeRateValue = self.setReferenceData(positionDict=finalPositionDict[Constant.CONST_POSITION_DICT], date=toDate)
        # Convert to DF
        initialPosition_DF = self.convertToDFPosition(initialPositionDict[Constant.CONST_POSITION_DICT])
        finalPosition_DF = self.convertToDFPosition(finalPositionDict[Constant.CONST_POSITION_DICT])
        # cash movements
        cashMovementList = CashMovementDao().getCashMovementsByDate(fromDate, toDate)
        cashMovementDF = self.convertToDFCashMovement(cashMovementList)
        cashInMovementDF = cashMovementDF.loc[(cashMovementDF['In Out'] == 'IN')]
        cashOutMovementDF = cashMovementDF.loc[(cashMovementDF['In Out'] == 'OUT')]
        # set position summary DF
        position_SummaryDF = pd.DataFrame(columns=['Custody Name', 'Initial Position USD', 'Final Position USD', 'PnL USD', 'Initial Position', 'Final Position', 'Cash In', 'Cash Out', 'PnL', 'TIR'])
        position_SummaryDF = position_SummaryDF.append(pd.Series(self.getSerieForSummary(cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, 'CETESDIRECTO', finalExchangeRateValue), index=position_SummaryDF.columns), ignore_index=True)
        position_SummaryDF = position_SummaryDF.append(pd.Series(self.getSerieForSummary(cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, 'GBM', finalExchangeRateValue), index=position_SummaryDF.columns), ignore_index=True)
        position_SummaryDF = position_SummaryDF.append(pd.Series(self.getSerieForSummary(cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, None, finalExchangeRateValue), index=position_SummaryDF.columns), ignore_index=True)
        return position_SummaryDF
        
    def getSerieForSummary(self, cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, custodyName=None, exchangeRateValue=None):
        if custodyName is None:
            totalCashIn = cashInMovementDF['Amount'].sum()
            totalCashOut = cashOutMovementDF['Amount'].sum()
            totalInitialPosition = initialPosition_DF['Valuated Amount'].sum()
            totalInitialPositionUSD = initialPosition_DF['Valuated Amount USD'].sum()
            totalFinalPosition = finalPosition_DF['Valuated Amount'].sum()
            totalFinalPositionUSD = finalPosition_DF['Valuated Amount USD'].sum()
            totalPnlAmount =  totalFinalPosition - totalInitialPosition - (totalCashIn - totalCashOut)
            totalPnlAmountUSD = totalFinalPositionUSD - totalInitialPositionUSD - ((totalCashIn - totalCashOut) / exchangeRateValue)
            totalTir = (totalPnlAmount / (totalInitialPosition + (totalCashIn - totalCashOut)))
            return ["Total", totalInitialPositionUSD, totalFinalPositionUSD, totalPnlAmountUSD, totalInitialPosition, totalFinalPosition, totalCashIn, totalCashOut, totalPnlAmount, totalTir]
        else:
            totalCashIn = cashInMovementDF.loc[(cashInMovementDF['Custody Name'] == custodyName)]['Amount'].sum()
            totalCashOut = cashOutMovementDF.loc[(cashOutMovementDF['Custody Name'] == custodyName)]['Amount'].sum()
            totalInitialPosition = initialPosition_DF.loc[(initialPosition_DF['Custody Name'] == custodyName)]['Valuated Amount'].sum()
            totalInitialPositionUSD = initialPosition_DF.loc[(initialPosition_DF['Custody Name'] == custodyName)]['Valuated Amount USD'].sum()
            totalFinalPosition = finalPosition_DF.loc[(finalPosition_DF['Custody Name'] == custodyName)]['Valuated Amount'].sum()
            totalInitialPositionUSD = initialPosition_DF.loc[(initialPosition_DF['Custody Name'] == custodyName)]['Valuated Amount USD'].sum()
            totalFinalPositionUSD = finalPosition_DF.loc[(finalPosition_DF['Custody Name'] == custodyName)]['Valuated Amount USD'].sum()
            totalPnlAmount =  totalFinalPosition - totalInitialPosition - (totalCashIn - totalCashOut)
            totalPnlAmountUSD = totalFinalPositionUSD - totalInitialPositionUSD - ((totalCashIn - totalCashOut) / exchangeRateValue)
            totalTir = (totalPnlAmount / (totalInitialPosition + (totalCashIn - totalCashOut)))
            return [custodyName, totalInitialPositionUSD, totalFinalPositionUSD, totalPnlAmountUSD, totalInitialPosition, totalFinalPosition, totalCashIn, totalCashOut, totalPnlAmount, totalTir]
        
        
    def convertToDFPosition(self, positionDict):
        position_DF = pd.DataFrame(columns=['Custody Name', 'Asset Name', 'Asset Type', 'isSIC', 'Position', 'Unit Cost', 'Invested Amount', 'Valuated Amount', 'Valuated Amount USD', 'Exchange Rate'])
        for row in positionDict.items():
            position = row[1]
            position_DF = position_DF.append(pd.Series([position.custody.name, position.asset.getName(), position.asset.assetType, position.asset.isSIC, position.getTotalQuantity(), position.getUnitCostOrRate(), position.getInvestedAmount(),
                  position.getValuatedAmount(), position.getValuatedAmountUSD(), position.exchangeRateValue], index=position_DF.columns), ignore_index=True)
        return position_DF
    
    def convertToDFCashMovement(self, cashMovementList):
        df = pd.DataFrame(columns=['Custody Name', 'Asset Name', 'In Out', 'Movement Date', 'Amount'])
        for cm in cashMovementList:
            df = df.append(pd.Series([cm.custody.name, cm.asset.getName(), cm.inOut, cm.movementDate, cm.amount], index=df.columns), ignore_index=True)
        return df
      
    def setReferenceData(self, positionDict, date):
        dbconnector = DBConnector()
        session = dbconnector.getNewSession()
        today = datetime.now().date()
        exchangeRateToUse = None
        if today == date:
            setLastMarketData = True
            exchangeRateToUse=MainCache.usdMXN
        else:
            setLastMarketData = False 
            workingDate = getLastWorkingDay(date) 
            exchangeRateID = "USD/MXN"
            #Try to find the exchangeRate in DB
            exchangeRateValue = ExchangeRateDao().getExchangeRateValueByDate(exchangeRateID=exchangeRateID, date=workingDate, raiseNoResultFound=True)
            if(exchangeRateValue is None):
                #Try to find the exchangeRate in EXCEL
                exchangeRateValue = PricingInterfaceExcel().getExchangeRateByDate('USD','MXN', workingDate)
                if (exchangeRateValue is None):
                    raise Exception("exchangeRateValue not found: " + str(workingDate))
                exchangeRate=GenericDao().getOneResult(objectClazz=ExchangeRate, condition=(ExchangeRate.name == exchangeRateID), session = session)
                ExchangeRateDao().addExchangeRateValue(value=exchangeRateValue, exchangeRate=exchangeRate, date=workingDate, session=session)
                exchangeRateToUse = exchangeRateValue.value
            else:
                exchangeRateToUse = exchangeRateValue.value
        #SET MARKET PRICE TO POSITIONS
        for row in positionDict.items():
            position = row[1]
            if position.asset.assetType != 'BOND':
                if(setLastMarketData):
                    position.refreshMarketData()
                else:
                    #Try to find the price in DB
                    price = PriceDao().getPriceByDate(position.getAssetName(), workingDate, raiseNoResultFound=False)
                    if price is None:
                        #Try to find the price in source
                        priceValue = PricingInterface.getMarketPriceByDate(position.getHistoricalPriceName(), position.asset.historicalPriceSource, workingDate)
                        if priceValue is None:
                            raise Exception("price not found: " + position.getHistoricalPriceName() + " " + str(workingDate))
                        price = PriceDao().addPrice(assetOID=position.asset.ID, date=workingDate, lastPrice=priceValue, session=session)
                    position.setMarketPrice(marketPrice=price.lastPrice, exchangeRateValue=exchangeRateValue.value)
            else:
                position.setExchangeRate(exchangeRateValue=exchangeRateToUse)
        session.close_all()
        return exchangeRateToUse
            
# if __name__ == '__main__':
#     PnlEngine().calculatePnl(datetime(2017, 1, 1).date(), datetime(2018, 1, 1).date())
#      PnlEngine().calculatePnl(datetime(2017, 1, 1).date(), datetime.now().date())
