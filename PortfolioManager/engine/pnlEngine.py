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
from dao.currencyDao import CurrencyDao
from dao.dao import GenericDao
from dao.priceDao import PriceDao
from engine.positionEngine import PositionEngine
from modelClass.currency import CurrencyValue, Currency
from modelClass.price import Price
import pandas as pd
from pricingAPI.PricingInterface import PricingInterfaceExcel, PricingInterface
from tools.tools import getLastWorkingDay


Initializer()
MainCache.refreshReferenceData()


class PnlEngine():
    
    def calculatePnl(self, fromDate, toDate):
        initDate = datetime(2001, 1, 1).date()
        initialPositionDict = PositionEngine().buildPositions(fromDate=initDate, toDate=fromDate, setLastMarketData=False)
        if len(initialPositionDict) == 0:
            logging.warning("Empty initial position dict")
        finalPositionDict = PositionEngine().buildPositions(fromDate=initDate, toDate=toDate, setLastMarketData=False)
        if len(finalPositionDict) == 0:
            logging.warning("Empty final position dict")
        # set reference data
        self.setReferenceData(positionDict=initialPositionDict[Constant.CONST_POSITION_DICT], date=fromDate)
        self.setReferenceData(positionDict=finalPositionDict[Constant.CONST_POSITION_DICT], date=toDate)
        # Convert to DF
        initialPosition_DF = self.convertToDFPosition(initialPositionDict[Constant.CONST_POSITION_DICT])
        finalPosition_DF = self.convertToDFPosition(finalPositionDict[Constant.CONST_POSITION_DICT])
        # cash movements
        cashMovementList = CashMovementDao().getCashMovementsByDate(fromDate, toDate)
        cashMovementDF = self.convertToDFCashMovement(cashMovementList)
        cashInMovementDF = cashMovementDF.loc[(cashMovementDF['In Out'] == 'IN')]
        cashOutMovementDF = cashMovementDF.loc[(cashMovementDF['In Out'] == 'OUT')]
        # set position summary DF
        position_SummaryDF = pd.DataFrame(columns=['Custody Name', 'Initial Position USD', 'Final Position USD', 'Initial Position', 'Final Position', 'Cash In', 'Cash Out', 'PnL', 'TIR'])
        position_SummaryDF = position_SummaryDF.append(pd.Series(self.getSerieForSummary(cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, 'CETESDIRECTO'), index=position_SummaryDF.columns), ignore_index=True)
        position_SummaryDF = position_SummaryDF.append(pd.Series(self.getSerieForSummary(cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, 'GBM'), index=position_SummaryDF.columns), ignore_index=True)
        position_SummaryDF = position_SummaryDF.append(pd.Series(self.getSerieForSummary(cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF), index=position_SummaryDF.columns), ignore_index=True)
        return position_SummaryDF
        
    def getSerieForSummary(self, cashInMovementDF, cashOutMovementDF, initialPosition_DF, finalPosition_DF, custodyName=None):
        if custodyName is None:
            totalCashIn = cashInMovementDF['Amount'].sum()
            totalCashOut = cashOutMovementDF['Amount'].sum()
            totalInitialPosition = initialPosition_DF['Valuated Amount'].sum()
            totalInitialPositionUSD = initialPosition_DF['Valuated Amount USD'].sum()
            totalFinalPosition = finalPosition_DF['Valuated Amount'].sum()
            totalFinalPositionUSD = finalPosition_DF['Valuated Amount USD'].sum()
            totalPnlAmount =  totalFinalPosition - totalInitialPosition - (totalCashIn - totalCashOut)
            totalTir = (totalPnlAmount / (totalInitialPosition + (totalCashIn - totalCashOut)))
            return ["Total", totalInitialPositionUSD, totalFinalPositionUSD, totalInitialPosition, totalFinalPosition, totalCashIn, totalCashOut, totalPnlAmount, totalTir]
        else:
            totalCashIn = cashInMovementDF.loc[(cashInMovementDF['Custody Name'] == custodyName)]['Amount'].sum()
            totalCashOut = cashOutMovementDF.loc[(cashOutMovementDF['Custody Name'] == custodyName)]['Amount'].sum()
            totalInitialPosition = initialPosition_DF.loc[(initialPosition_DF['Custody Name'] == custodyName)]['Valuated Amount'].sum()
            totalFinalPosition = finalPosition_DF.loc[(finalPosition_DF['Custody Name'] == custodyName)]['Valuated Amount'].sum()
            totalInitialPositionUSD = initialPosition_DF.loc[(initialPosition_DF['Custody Name'] == custodyName)]['Valuated Amount USD'].sum()
            totalFinalPositionUSD = finalPosition_DF.loc[(finalPosition_DF['Custody Name'] == custodyName)]['Valuated Amount USD'].sum()
            totalPnlAmount =  totalFinalPosition - totalInitialPosition - (totalCashIn - totalCashOut)
            totalTir = (totalPnlAmount / (totalInitialPosition + (totalCashIn - totalCashOut)))
            return [custodyName, totalInitialPositionUSD, totalFinalPositionUSD, totalInitialPosition, totalFinalPosition, totalCashIn, totalCashOut, totalPnlAmount, totalTir]
        
        
    def convertToDFPosition(self, positionDict):
        position_DF = pd.DataFrame(columns=['Custody Name', 'Asset Name', 'Asset Type', 'isSIC', 'Position', 'Unit Cost', 'Invested Amount', 'Valuated Amount', 'Valuated Amount USD'])
        for row in positionDict.items():
            position = row[1]
            position_DF = position_DF.append(pd.Series([position.custody.name, position.asset.getName(), position.asset.assetType, position.asset.isSIC, position.getTotalQuantity(), position.getUnitCostOrRate(), position.getInvestedAmount(),
                  position.getValuatedAmount(), position.getValuatedAmountUSD()], index=position_DF.columns), ignore_index=True)
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
        if today == date:
            setLastMarketData = True
        else:
            setLastMarketData = False 
            workingDate = getLastWorkingDay(date) 
            currencyName = "USD/MXN"
            currencyValue = CurrencyDao().getCurrencyValueByDate(currencyName=currencyName, date=workingDate, raiseNoResultFound=False)
            if(currencyValue is None):
                exchangeRateValue = PricingInterfaceExcel().getExchangeRateByDate('USD','MXN', workingDate)
                if (exchangeRateValue is None):
                    raise Exception("exchangeRateValue found: " + str(workingDate))
                currencyValue = CurrencyValue()
                currencyValue.value = exchangeRateValue
                currencyValue.currency = GenericDao().getOneResult(objectClazz=Currency, condition=(Currency.name == currencyName), session = session)
                currencyValue.date = workingDate
                session.add(currencyValue)
                session.commit()
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
                        priceValue = PricingInterface.getMarketPriceByDate(position.getMainName(), position.asset.historicalPriceSource, workingDate)
                        if priceValue is None:
                            raise Exception("price not found: " + position.getMainName() + " " + str(workingDate))
                        PriceDao().addPrice(assetOID=position.asset.ID, date=workingDate, lastPrice=priceValue, session=session)
                    position.setMarketPrice(marketPrice=price.lastPrice, exchangeRateValue=currencyValue.value)
            else:
                #set exchange rate for BOND
                if(not setLastMarketData):
                    position.setExchangeRate(exchangeRateValue=currencyValue.value)
                else:
                    position.setExchangeRate(exchangeRateValue=MainCache.usdMXN)
        session.close_all()
            
# if __name__ == '__main__':
#     PnlEngine().calculatePnl(datetime(2017, 1, 1).date(), datetime(2018, 1, 1).date())
#      PnlEngine().calculatePnl(datetime(2017, 1, 1).date(), datetime.now().date())
