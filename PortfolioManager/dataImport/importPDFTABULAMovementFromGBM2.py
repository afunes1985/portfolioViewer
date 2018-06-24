'''
Created on 11 jun. 2018

@author: afunes
'''





import calendar
from datetime import datetime
from decimal import Decimal
import logging

import pandas
from tabula import read_pdf

from core.cache import Singleton, MainCache
from dao.dao import DaoTax, DaoCorporateEvent
from engine.engine import Engine
from logicObject.ImportMovementLO import ImportMovementLO
from modelClass.cashMovement import CashMovement
from modelClass.constant import Constant
from modelClass.corporateEvent import CorporateEvent
from modelClass.movement import Movement
from modelClass.tax import Tax


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()


class MovementImporter():
    
    types = {'ABONO DIVIDENDO EMISORA EXTRANJERA' : 'DIVIDENDO', 
                 'ISR 10 % POR DIVIDENDOS SIC' : 'ISR_DIVIDENDO', 
                 'Compra Soc. de Inv. - Cliente' : 'FUND_BUY', 
                 'Compra de Acciones.' : 'EQUITY_BUY', 
                 'Venta Soc. de Inv. - Cliente' : 'FUND_SELL',
                 'DEPOSITO DE EFECTIVO' : 'CASH'}
    
    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)
    
    def getMovementList(self, filePath):
        self.assetDict = Engine.getAssetDict()
        self.assetTranslator = Engine.getAssetTranslatorDict()
        imLO = ImportMovementLO()
        fileName = filePath[filePath.rfind("/", 0, len(filePath))+1: len(filePath)]
        custodyName = fileName[0:fileName.find("_")]
        if (custodyName == 'GBM'):
            imLO.setMovementList(self.getMovementListFromGBM(filePath, fileName, imLO))
        imLO.setCustodyName(custodyName)
        return imLO
    
    def getMovementListFromGBM(self, filePath, fileName, imLO):
        json_data = self.getMovementData(filePath)
        if (len(json_data) != 0):
            print(json_data)
            custodyOID = Engine.getCustodyDictName()['GBM'].OID
            date =  fileName.replace(".pdf", '')
            date = date.replace("GBM_","")
            fromDate = date + "-" + "01"
            fromDate =  pandas.to_datetime(datetime.strptime(fromDate, '%y-%m-%d')).to_pydatetime() 
            imLO.setFromDate(fromDate)
            imLO.setToDate(fromDate.replace(day = calendar.monthrange(fromDate.year, fromDate.month)[1]))
            movementList = []
            for index, key in enumerate(json_data):
                if index > 2:
                    dateAndExternalID = key[0]['text']
                    paymentDate = dateAndExternalID[0: 2]
                    externalID = dateAndExternalID[dateAndExternalID.find(' ', 0)+1: len(dateAndExternalID)]
                    print (externalID)
                    paymentDate = date + "-" + paymentDate
                    paymentDate =  pandas.to_datetime(datetime.strptime(paymentDate, '%y-%m-%d')).to_pydatetime() 
                    print (paymentDate)
                    movementType = key[2]['text']
                    print (movementType)
                    comment = "UPLOAD 20" + date
                    netAmount = self.replaceComma(key[10]['text'])
                    assetName = key[3]['text']
                    assetOID = self.getAssetbyName(assetName)
                    print (assetName)
                    if(movementType == 'DEPOSITO DE EFECTIVO'
                       or movementType == "RETIRO DE EFECTIVO"):
                        m = CashMovement(None)
                        m.setAttr(None, float(netAmount), self.getInOrOut(movementType), custodyOID, paymentDate, comment, externalID)
                        movementList.append(m)  
                    elif(movementType == 'Abono Efectivo Dividendo, Cust. Normal'
                         or movementType == 'ABONO DIVIDENDO EMISORA EXTRANJERA'):
                        ce = CorporateEvent(None)
                        ce.setAttr(None, custodyOID, mainCache.corporateEventTypeOID[1], assetOID, paymentDate, float(netAmount), float(netAmount), comment, externalID)
                        movementList.append(ce)
                    elif(movementType == 'Compra Soc. de Inv. - Cliente'
                            or movementType == "Compra de Acciones."
                            or movementType == "Venta Soc. de Inv. - Cliente"
                            or movementType ==  "Venta de Acciones."
                            or movementType == "Venta por Autoentrada"
                            or movementType == "Compra por Autoentrada"
                            or movementType == "Compra de Acciones por Oferta Publica"):
                        quantity = self.replaceComma(key[4]['text'])
                        price = self.replaceComma(key[5]['text'])
                        commission = self.replaceComma(key[7]['text'])
                        commissionVAT = self.replaceComma(key[9]['text'])
                        grossAmount = float(str('{0:.6f}'.format(float(price*quantity))))
                        m = Movement(None)
                        m.setAttr( None, assetOID, self.getBuyOrSell(movementType), paymentDate, float(quantity), float(price), None, grossAmount , float(netAmount), self.getCommissionPercentage(movementType), float(commission), float(commissionVAT), externalID, custodyOID, comment, None, None)
                        movementList.append(m)
                    elif(movementType == "ISR 10 % POR DIVIDENDOS SIC"):
                        ce = movementList[len(movementList)-1]
                        if(isinstance(ce, CorporateEvent)):
                            isrAmount = netAmount
                            tax = Tax(None)
                            tax.setAttr(None, 'CORPORATE_EVENT', None, isrAmount, externalID)
                            ce.netAmount =  float("%6.f" % (ce.grossAmount - isrAmount))
                            ce.tax = tax
                            #movementList.remove(ce)
                            #movementList.append(ce)
                    else:
                        quantity = self.replaceComma(key[4]['text'])
                        price = self.replaceComma(key[5]['text'])
                        commission = self.replaceComma(key[7]['text'])
                        commissionVAT = self.replaceComma(key[9]['text'])
                        grossAmount = float(str('{0:.6f}'.format(float(price*quantity))))
                        m = Movement(None)
                        m.setAttr( None, assetOID, 'NOT CATEGORY', paymentDate, float(quantity), float(price), None, grossAmount, float(netAmount), self.getCommissionPercentage(movementType), float(commission), float(commissionVAT), externalID, custodyOID, "NOT CATEGORY", None, None)
                        movementList.append(m)
            return movementList 
    
    def getCommissionPercentage(self, movementType):
        if(movementType == "Compra de Acciones."
            or movementType ==  "Venta de Acciones."
            or movementType == "Venta por Autoentrada"):
            return Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE
        else:
            return 0
    
    def getBuyOrSell(self, movementType):
        if(movementType == 'Compra Soc. de Inv. - Cliente'
           or movementType == "Compra de Acciones."
           or movementType == "Compra por Autoentrada"
           or movementType == "Compra de Acciones por Oferta Publica"):
            return Constant.CONST_BUY
        elif(movementType == 'Venta Soc. de Inv. - Cliente'
             or movementType ==  "Venta de Acciones."
             or movementType == "Venta por Autoentrada"):
            return Constant.CONST_SELL
        else:
            return 'NOT CATEGORY'
        
    def getInOrOut(self, movementType):
        if (movementType == "RETIRO DE EFECTIVO"):
            return Constant.CONST_OUT
        elif (movementType =='DEPOSITO DE EFECTIVO'):
            return Constant.CONST_IN
        else:
            return 'NOT CATEGORY'

    def replaceComma(self, value):
        return float(float(value.replace(',','')))
    
    def getMovementData(self, filePath):
        for page in range(4, 6):
            json_data = read_pdf(filePath, 'json', 'latin_1', pages=page)
            if (len(json_data) != 0):
                key = json_data[0]['data'][0][2]['text']
                if ("DESCRIPCI"  == key[0:9]):
                    return json_data[0]['data']
            
    def getAssetbyName(self, assetName):
        if(assetName == "Efec *"):
            return None
        else:
            asset = self.assetDict.get(self.assetTranslator.get(assetName, assetName), None)
            if (asset is None):
                logging.warning(assetName)
            else:
                return asset.OID
              
