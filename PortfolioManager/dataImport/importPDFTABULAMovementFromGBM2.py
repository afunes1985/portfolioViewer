'''
Created on 11 jun. 2018

@author: afunes
'''





import calendar
from datetime import datetime

import pandas
from tabula import read_pdf

from core.cache import Singleton, MainCache
from engine.engine import Engine
from logicObject.ImportMovementLO import ImportMovementLO
from modelClass.cashMovement import CashMovement
from modelClass.corporateEvent import CorporateEvent
from modelClass.movement import Movement
from modelClass.constant import Constant


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
        imLO = ImportMovementLO()
        fileName = filePath[filePath.rfind("/", 0, len(filePath))+1: len(filePath)]
        custodyName = fileName[0:fileName.find("_")]
        self.assetTranslator = Engine.getAssetTranslatorDict()
        if (custodyName == 'GBM'):
            imLO.setMovementList(self.getMovementListFromGBM(filePath, fileName, imLO))
        imLO.setCustodyName(custodyName)
        return imLO
    
    def getMovementListFromGBM(self, filePath, fileName, imLO):
        json_data = read_pdf(filePath, 'json', 'latin_1', pages=4)
        print (json_data[0]['data'])
        date =  fileName.replace(".pdf", '')
        date = date.replace("GBM_","")
        fromDate = date + "-" + "01"
        fromDate =  pandas.to_datetime(datetime.strptime(fromDate, '%y-%m-%d')).to_pydatetime() 
        imLO.setFromDate(fromDate)
        imLO.setToDate(fromDate.replace(day = calendar.monthrange(fromDate.year, fromDate.month)[1]))
        custodyOID = Engine.getCustodyDictName()['GBM'].OID
        assetDict = Engine.getAssetDict()
        movementList = []
        for index, key in enumerate(json_data[0]['data']):
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
                print (comment)
                netAmount = self.replaceComma(key[10]['text'])
                if(movementType == 'DEPOSITO DE EFECTIVO'):
                    m = CashMovement(None)
                    m.setAttr(None, float(netAmount), 'IN', custodyOID, paymentDate, comment, externalID)
                    movementList.append(m)  
                elif(movementType == 'Abono Efectivo Dividendo, Cust. Normal'):
                    assetName = key[3]['text']
                    asset = assetDict[self.assetTranslator.get(assetName, assetName)]
                    ce = CorporateEvent(None)
                    ce.setAttr(None, custodyOID, mainCache.corporateEventTypeOID[1], asset, paymentDate, float(netAmount), float(netAmount), comment, externalID)
                    movementList.append(ce)
                elif(movementType == 'Compra Soc. de Inv. - Cliente'
                        or movementType == "Compra de Acciones."
                        or movementType == "Venta Soc. de Inv. - Cliente"
                        or movementType ==  "Venta de Acciones."):
                    assetName = key[3]['text']
                    asset = assetDict[self.assetTranslator.get(assetName, assetName)]
                    print (assetName)
                    quantity = self.replaceComma(key[4]['text'])
                    print (quantity)
                    price = self.replaceComma(key[5]['text'])
                    print (price)
                    commission = self.replaceComma(key[7]['text'])
                    print (commission)
                    commissionVAT = self.replaceComma(key[9]['text'])
                    print (commissionVAT)
                    grossAmount = float(str('{0:.6f}'.format(float(price*quantity))))
                    m = Movement(None)
                    m.setAttr( None, asset.OID, self.getBuyOrSell(movementType), paymentDate, float(quantity), float(price), None, grossAmount , float(netAmount), self.getCommissionPercentage(movementType), float(commission), float(commissionVAT), externalID, custodyOID, comment, None, None)
                    movementList.append(m)
                else:
                    assetName = key[3]['text']
                    asset = assetDict[self.assetTranslator.get(assetName, assetName)]
                    print (assetName)
                    quantity = self.replaceComma(key[4]['text'])
                    print (quantity)
                    price = self.replaceComma(key[5]['text'])
                    print (price)
                    commission = self.replaceComma(key[7]['text'])
                    print (commission)
                    commissionVAT = self.replaceComma(key[9]['text'])
                    print (commissionVAT)
                    grossAmount = float(str('{0:.6f}'.format(float(price*quantity))))
                    m = Movement(None)
                    m.setAttr( None, asset.OID, 'NOT CATEGORY', paymentDate, float(quantity), float(price), None, grossAmount, float(netAmount), self.getCommissionPercentage(movementType), float(commission), float(commissionVAT), externalID, custodyOID, "NOT CATEGORY", None, None)
                    movementList.append(m)
        return movementList 
    
    def getCommissionPercentage(self, movementType):
        if(movementType == "Compra de Acciones."
            or movementType ==  "Venta de Acciones."):
            return Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE
        else:
            return 0
    
    def getBuyOrSell(self, movementType):
        if(movementType == 'Compra Soc. de Inv. - Cliente'
           or movementType == "Compra de Acciones."):
            return Constant.CONST_BUY
        elif(movementType == 'Venta Soc. de Inv. - Cliente'
             or movementType ==  "Venta de Acciones."):
            return Constant.CONST_SELL
        else:
            return 'NOT CATEGORY'

    def replaceComma(self, value):
        return float(float(value.replace(',','')))