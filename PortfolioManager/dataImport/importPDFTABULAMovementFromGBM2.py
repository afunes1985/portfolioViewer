'''
Created on 11 jun. 2018

@author: afunes
'''





import calendar
from datetime import datetime, date
import logging

import pandas
from tabula import read_pdf

from core.cache import Singleton, MainCache
from dao.dao import DaoMovement
from engine.engine import Engine
from logicObject.ImportMovementLO import ImportMovementLO
from modelClass.cashMovement import CashMovement
from modelClass.constant import Constant
from modelClass.corporateEvent import CorporateEvent
from modelClass.movement import Movement
from modelClass.tax import Tax
from valueObject.ImporterMovementVO import ImporterMovementVO


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()


class MovementImporter():
    
    cashMovementTypeINList = ["DEPOSITO DE EFECTIVO", "INGEFVO"]
    cashMovementTypeOUTList = ["RETIRO DE EFECTIVO"]
    cashMovementTypeList = cashMovementTypeINList + cashMovementTypeOUTList
    
    MovementTypeBUYList =[ 'Compra Soc. de Inv. - Cliente',"Compra de Acciones.","Compra por Autoentrada","Compra de Acciones por Oferta Publica", "COMPSI", "COMPRA"]
    MovementTypeSELLList =[ "Venta Soc. de Inv. - Cliente","Venta de Acciones.","Venta por Autoentrada", "VTASI"]
    MovementTypeList = MovementTypeBUYList + MovementTypeSELLList
    
    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)
    
    def getMovementList(self, filePath, assetName):
        self.assetDict = Engine.getAssetDict()
        self.assetTranslator = Engine.getAssetTranslatorDict()
        imLO = ImportMovementLO()
        fileName = filePath[filePath.rfind("/", 0, len(filePath))+1: len(filePath)]
        custodyName = fileName[0:fileName.find("_")]
        if (custodyName == 'GBM'):
            imLO.setMovementList(self.getMovementListFromGBM(filePath, fileName, imLO, assetName))
        elif (custodyName == 'CETESDIRECTO'):
            imLO.setMovementList(self.getMovementListFromCETESDIRECTO(filePath, fileName, imLO, assetName))
        imLO.setCustodyName(custodyName)
        return imLO
    
    def getMovementListFromCETESDIRECTO(self, filePath, fileName, imLO, filterAssetName):
        json_data = self.getRawDataFromCETESDIRECTO(filePath)
        if (len(json_data) != 0):
            custody = Engine.getCustodyDictName()['CETESDIRECTO']
            movementList = []
            isAfterBegin = False
            isFromToDateNOTSetter = True
            for index, row in enumerate(json_data):
                paymentDate = self.getColumnValueFromList(row, 0)
                if ("Saldo inicial"  == paymentDate):
                    isAfterBegin = True
                elif (isAfterBegin):
                    paymentDate = pandas.to_datetime(datetime.strptime(paymentDate[paymentDate.find(" ", 0)+1:len(paymentDate)], '%d/%m/%y')).to_pydatetime()
                    if (isFromToDateNOTSetter):
                        isFromToDateNOTSetter = False
                        imLO.setFromDate(paymentDate.replace(day=1))
                        imLO.setToDate(paymentDate.replace(day = calendar.monthrange(paymentDate.year, paymentDate.month)[1]))
                    importerMovementVO = ImporterMovementVO()
                    importerMovementVO.setPaymentDate(paymentDate)
                    importerMovementVO.setExternalID(self.getColumnValueFromList(row, 1))
                    importerMovementVO.setOriginMovementType(self.getColumnValueFromList(row, 2))
                    assetName = self.getColumnValueFromList(row, 3)
                    assetNameSerie = self.getColumnValueFromList(row, 4)
                    importerMovementVO.assetNameSerie = assetNameSerie
                    importerMovementVO.setAssetName(assetName)
                    importerMovementVO.setQuantity(self.replaceComma(self.getColumnValueFromList(row, 5)))
                    price = self.getColumnValueFromList(row, 6)
                    importerMovementVO.setPrice(self.replaceComma(price[0: price.find(" ", 0)]))
                    importerMovementVO.setRate(self.replaceComma(self.getColumnValueFromList(row, 7)))
                    cargo = self.replaceComma(self.getColumnValueFromList(row, 8))
                    abono = self.replaceComma(self.getColumnValueFromList(row, 9))
                    if (cargo == 0):
                        importerMovementVO.setNetAmount(abono)
                        importerMovementVO.setGrossAmount(abono)
                    elif (abono  == 0):
                        importerMovementVO.setNetAmount(cargo)
                        importerMovementVO.setGrossAmount(cargo)
                    importerMovementVO.setCustody(custody)
                    importerMovementVO.setComment("UPLOAD " + str(importerMovementVO.getPaymentDate())[0:7])
                    importerMovementVO.logObject()
                    self.convertToPersistent(importerMovementVO)
                    if (importerMovementVO.persistentObject is not None
                            and (filterAssetName == importerMovementVO.persistentObject.asset.name or filterAssetName == 'ALL')):
                        movementList.append(importerMovementVO.persistentObject)
            return movementList

                
    def getMovementListFromGBM(self, filePath, fileName, imLO, assetName):
        json_data = self.getRawDataFromGBM(filePath)
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
    
    def replaceComma(self, value):
        if (value != ""):
            return float(float(value.replace(',','')))
    
    def getRawDataFromGBM(self, filePath):
        for page in range(4, 6):
            json_data = read_pdf(filePath, 'json', 'latin_1', pages=page)
            if (len(json_data) != 0):
                key = json_data[0]['data'][0][2]['text']
                if ("DESCRIPCI"  == key[0:9]):
                    return json_data[0]['data']
                
    def getRawDataFromCETESDIRECTO(self, filePath):
        for page in range(2, 3):
            json_data = read_pdf(filePath, 'json', 'latin_1', pages=page)
            if (len(json_data) != 0):
                for row in range(0, len(json_data[0]['data'])):
                    key = json_data[0]['data'][row][0]['text']
                    #print(key)
                    if ("Saldo inicial"  == key):
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
    
    def getColumnValueFromList(self, row, indColumn):
        columnValue = row[indColumn]['text']
        return columnValue

    def convertToPersistent(self, importerMovementVO):
        if any(importerMovementVO.originMovementType in s for s in self.cashMovementTypeList):
            importerMovementVO.persistentObject = CashMovement(None)
            assetOID = self.getAssetbyName(importerMovementVO.assetName)
            importerMovementVO.persistentObject.setAttr(None, importerMovementVO.netAmount, self.getInOrOut(importerMovementVO.originMovementType), importerMovementVO.custody.OID, importerMovementVO.paymentDate, importerMovementVO.comment, importerMovementVO.externalID, assetOID)
        elif any(importerMovementVO.originMovementType in s for s in self.MovementTypeList):    
            importerMovementVO.persistentObject = Movement(None)
            assetOID = self.getAssetbyName(importerMovementVO.assetName)
            importerMovementVO.persistentObject.setAttr( None, assetOID, self.getBuyOrSell(importerMovementVO.originMovementType), importerMovementVO.paymentDate, 
                                                            importerMovementVO.quantity, importerMovementVO.price, importerMovementVO.getRate(), importerMovementVO.grossAmount , 
                                                            importerMovementVO.netAmount, self.getCommissionPercentage(importerMovementVO.originMovementType), importerMovementVO.commission, 
                                                            importerMovementVO.commissionVAT, importerMovementVO.externalID, importerMovementVO.custody.OID, importerMovementVO.comment, 
                                                            importerMovementVO.getTenor(), importerMovementVO.getMaturityDate())
        elif (importerMovementVO.originMovementType == "ISR"):
            maturityDate = date(int('20' +importerMovementVO.assetNameSerie[:2]), int(importerMovementVO.assetNameSerie[2:4]), int(importerMovementVO.assetNameSerie[4:6]))
            totalAmount = 0
            movementRs = DaoMovement.getMovementsByMaturityDate(maturityDate)
#             if len(movementRs) > 0:
#                     for row in movementRs:
#                         totalAmount += float(row[1])
#                     rowNum = 0    
#                     for row in movementRs:    
#                         movementID = row[0]
#                         grossAmount = float(row[1])
#                         if movementID is not None:
#                             t = Tax(None)
#                             t.setAttr(None, 'MOVEMENT', movementID, round((grossAmount/totalAmount) * amount, 8) , externalID + "-" + str(rowNum))
#                             rowNum += 1
#                             print("ADD externalID " + str(externalID) + " ID: " + str(newID))
        else:
            logging.warning(importerMovementVO.originMovementType)
                
    def getInOrOut(self, movementType):
        if any(movementType in s for s in self.cashMovementTypeOUTList):
            return Constant.CONST_OUT
        elif any(movementType in s for s in self.cashMovementTypeINList):
            return Constant.CONST_IN
        else:
            return 'NOT CATEGORY'
        
    def getBuyOrSell(self, movementType):
        if any(movementType in s for s in self.MovementTypeBUYList):
            return Constant.CONST_BUY
        elif any(movementType in s for s in self.MovementTypeSELLList):
            return Constant.CONST_SELL
        else:
            return 'NOT CATEGORY'

