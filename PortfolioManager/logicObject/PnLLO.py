'''
Created on 29 ene. 2018

@author: afunes
'''
from datetime import date, datetime
from decimal import Decimal
import logging

from core.function import Function
from dao.dao import DaoPrice, DaoCurrency
from core.constant import Constant
from valueObject.PnLVO import PnLVO


class PnLLO():
    
    def setCashMovement(self, cashMovementList):
        self.cashMovementList = cashMovementList
    
    def setPnlVOlist(self, pnlVOList):
        self.pnlVOList = pnlVOList
    
    def getTotalCash(self, inOut, custodyOID):
        totalCash = 0
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == inOut and (cashMovement.custody.OID == custodyOID or custodyOID is None):
                totalCash += cashMovement.amount
        return totalCash
    
    def getTotalWeightedCash(self, inOut, custodyOID, fromDate, toDate):
        totalWeightedCash = 0
        #fromDate = datetime.combine(fromDate, datetime.min.time())
        difFromTo = abs(toDate-fromDate).days
        for cashMovement in self.cashMovementList:
            if cashMovement.inOut == inOut and (cashMovement.custody.OID == custodyOID or custodyOID is None):
                totalWeightedCash += cashMovement.amount * Decimal(((float(difFromTo) - abs(cashMovement.movementDate-fromDate).days)) /difFromTo)  
        return totalWeightedCash
       
    def getTotalCashIn(self, custodyOID):
        return self.getTotalCash("IN", custodyOID)
    
    def getTotalCashOut(self, custodyOID):
        return self.getTotalCash("OUT", custodyOID)
    
    def getTotalWeightedCashIn(self, custodyOID, fromDate, toDate):
        return self.getTotalWeightedCash("IN", custodyOID, fromDate, toDate)
    
    def getTotalWeightedCashOut(self, custodyOID, fromDate, toDate):
        return self.getTotalWeightedCash("OUT", custodyOID, fromDate, toDate)
    
    def calculatePnL(self, fromDate, toDate):
        self.setReferenceData(fromDate, toDate)
        pnlCalculationList = []
        pnlCalculationList.append(self.calculateConsolidatedPnl(fromDate, toDate))
        self.calculateCustodyPnL(pnlCalculationList, fromDate, toDate)
        return pnlCalculationList
        
    def calculateConsolidatedPnl(self, fromDate, toDate): 
        return self.calculatePnl(None, fromDate, toDate)
        
    def calculatePnl(self, custodyOID, fromDate, toDate):
        from core.cache import Singleton, MainCache
        from engine.engine import Engine
        mainCache = Singleton(MainCache)
        pnlVO = PnLVO() 
        custody = mainCache.custodyDictOID.get(custodyOID)
        if (custody is None):
            pnlVO.itemName = "Total"
        else:
            pnlVO.itemName = custody.name
            
        pnlVO.totalCashIn = self.getTotalCashIn(custodyOID)
        pnlVO.totalCashOut = self.getTotalCashOut(custodyOID)
        pnlVO.totalWeightedCashIn =  0 #self.getTotalWeightedCashIn(custodyOID, fromDate, toDate)
        pnlVO.totalWeightedCashOut = 0  #self.getTotalWeightedCashOut(custodyOID, fromDate, toDate)
        pnlVO.finalPosition = Engine.getSubTotalValuatedAmountByCustodyOID(self.finalPositionDict[Constant.CONST_POSITION_DICT], custodyOID)
        pnlVO.initialPosition = Engine.getSubTotalValuatedAmountByCustodyOID(self.startPositionDict[Constant.CONST_POSITION_DICT], custodyOID)
        pnlVO.pnlAmount =  pnlVO.finalPosition - pnlVO.initialPosition - (pnlVO.totalCashIn - pnlVO.totalCashOut)
        pnlVO.pnlWeightedAmount =  0 #pnlVO.finalPosition - pnlVO.initialPosition - (pnlVO.totalWeightedCashIn - pnlVO.totalWeightedCashOut)
        pnlVO.tir = (pnlVO.pnlAmount / (pnlVO.initialPosition + (pnlVO.totalCashIn - pnlVO.totalCashOut)))*100
        pnlVO.weightedTir = 0 #(pnlVO.pnlAmount / (pnlVO.initialPosition + (pnlVO.totalWeightedCashIn - pnlVO.totalWeightedCashOut)))*100
        return pnlVO
        
    def calculateCustodyPnL(self, pnlCalculationList, fromDate, toDate):
        from engine.engine import Engine
        custodyDictOID = Engine.getCustodyDictOID()
        for custodyOID in custodyDictOID.iterkeys():
            pnlCalculationList.append(self.calculatePnl(custodyOID, fromDate, toDate))
    
    def setPositionDict(self, fromDate, toDate, setLastMarketData):
        from engine.engine import Engine
        today = datetime.now().date()
        self.startPositionDict = Engine.buildPositions(date(1900, 1, 1), fromDate, False)
        if len(self.startPositionDict) == 0:
            logging.warning("Empty start position dict")
        self.finalPositionDict = Engine.buildPositions(date(1900, 1, 1), toDate, setLastMarketData)
        if len(self.finalPositionDict) == 0:
            logging.warning("Empty final position dict")
    
    def setReferenceData(self, fromDate, toDate):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        #build positions
        today = datetime.now().date()
        if today == toDate:
            setLastMarketData = True
        else:
            setLastMarketData = False    
        self.setPositionDict(fromDate, toDate, setLastMarketData)
        self.startWorkingDay = Function.getLastWorkingDay(fromDate)
        startUsdMxn = DaoCurrency.getCurrencyValueByDate("USD/MXN", self.startWorkingDay)
        if len(startUsdMxn) == 0:
                logging.warning("start USDMXN not found: " + str(self.startWorkingDay))
        if setLastMarketData:
            finalUsdMxn = mainCache.usdMXN
        else:
            self.finalWorkingDay = Function.getLastWorkingDay(toDate)
            currencyRS = DaoCurrency.getCurrencyValueByDate("USD/MXN", self.finalWorkingDay)
            if len(currencyRS) == 0:
                logging.warning("final USDMXN not found: " + str(self.finalWorkingDay))
            finalUsdMxn =  currencyRS[0][0]
        for position in (self.startPositionDict[Constant.CONST_POSITION_DICT]).itervalues():
            if position.asset.assetType != 'BOND':
                price = DaoPrice.getPriceByDate(position.getMainName(), self.startWorkingDay)
                if len(price) == 0:
                    logging.warning("price not found: " + position.getMainName() + " " + str(self.startWorkingDay))    
                position.setSpecificMarketData(price[0][0], startUsdMxn[0][0])
        if not setLastMarketData: 
            for position in (self.finalPositionDict[Constant.CONST_POSITION_DICT]).itervalues():
                if position.asset.assetType != 'BOND':
                    price = DaoPrice.getPriceByDate(position.getMainName(), self.finalWorkingDay)
                    if len(price) == 0:
                        logging.warning("price not found: " + position.getMainName() + " " + str(self.finalWorkingDay)) 
                    position.setSpecificMarketData(price[0][0], finalUsdMxn)
        
