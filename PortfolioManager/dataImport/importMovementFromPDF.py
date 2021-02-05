'''
Created on 11 jun. 2018

@author: afunes
'''
import calendar
from datetime import datetime, date
from decimal import Decimal
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
    cashMovementTypeOUTList = ["RETIRO DE EFECTIVO", "EGREFVO"]
    cashMovementTypeList = cashMovementTypeINList + cashMovementTypeOUTList
    
    movementTypeBUYCOMList = ["Compra de Acciones.","Compra por Autoentrada"]
    movementTypeSELLCOMList = ["Venta de Acciones.","Venta por Autoentrada"]
    movementTypeCOMList = movementTypeBUYCOMList + movementTypeSELLCOMList
    movementTypeBUYList =[ 'Compra Soc. de Inv. - Cliente',"Compra de Acciones por Oferta Publica", "COMPSI", "COMPRA"] + movementTypeBUYCOMList
    movementTypeSELLList =[ "Venta Soc. de Inv. - Cliente", "VTASI"] + movementTypeSELLCOMList
    movementTypeList = movementTypeBUYList + movementTypeSELLList
    
    corporateEventTypeList =[ "Abono Efectivo Dividendo, Cust. Normal","ABONO DIVIDENDO EMISORA EXTRANJERA"]
    
    corporateEventTAXTypeList = ["ISR 10 % POR DIVIDENDOS SIC"]
    
    nonMovementTypeList = corporateEventTAXTypeList
    
    headerCetes = {"Folio": None, "Descrip": None, "Emisora": None, "Serie": None, "tulos": None, "Precio": None, "Plazo": None, "Tasa": None, "Cargo": None, "Abono": None}
    
    def getMovementList(self, filePath, assetName):
        self.assetDict = Engine.getAssetDict()
        self.assetTranslator = Engine.getAssetTranslatorDict()
        imLO = ImportMovementLO()
        fileName = filePath[filePath.rfind("/", 0, len(filePath))+1: len(filePath)]
        custodyName = fileName[0:fileName.find("_")]
        custody = Engine.getCustodyDictName()[custodyName]
        if (custody.name == 'GBM'):
            imLO.setMovementList(self.getMovementListFromGBM(filePath, fileName, imLO, assetName, custody))
        elif (custody.name == 'CETESDIRECTO'):
            imLO.setMovementList(self.getMovementListFromCETESDIRECTO(filePath, fileName, imLO, assetName, custody))
        imLO.setCustodyName(custodyName)
        return imLO
    
    def getMovementListFromCETESDIRECTO(self, filePath, fileName, imLO, filterAssetName, custody):
        json_data = self.getRawDataFromCETESDIRECTO(filePath)
        if (len(json_data) != 0):
            self.movementList = []
            isReadyToReadMov = False
            isReadyToReadFirstMov = False
            isFromToDateNOTSetter = True
            for index, row in enumerate(json_data):
                for i in range(len(row)):
                    cellValue = self.getColumnValueFromList(row, i)
                    for headerKey in self.headerCetes.keys():
                        if (cellValue.find(headerKey) != -1):
                            self.headerCetes[headerKey] = i
#                             break
                for value in self.headerCetes.values():
                    if value is None:
                        isReadyToReadFirstMov = False
                        break
                    isReadyToReadFirstMov = True
                    
                if(isReadyToReadFirstMov):
                    for i in range(2):
                        cellValue = self.getColumnValueFromList(row, i)
                        try:
                            paymentDate = pandas.to_datetime(datetime.strptime(cellValue[cellValue.find(" ", 0)+1:len(cellValue)], '%d/%m/%y')).to_pydatetime()
                            isReadyToReadMov = True
                        except Exception:
                            if(not isReadyToReadMov):
                                isReadyToReadMov = False
                        
                    if (isReadyToReadMov):
                        if (isFromToDateNOTSetter):
                            isFromToDateNOTSetter = False
                            imLO.setFromDate(paymentDate.replace(day=1))
                            imLO.setToDate(paymentDate.replace(day = calendar.monthrange(paymentDate.year, paymentDate.month)[1]))
                        importerMovementVO = ImporterMovementVO()
                        importerMovementVO.setPaymentDate(paymentDate)
                        externalID = self.getColumnValueFromList(row, self.headerCetes["Folio"])
                        importerMovementVO.setExternalID(externalID[0:12].strip())
                        description = self.getColumnValueFromList(row, self.headerCetes["Descrip"])
                        importerMovementVO.setOriginMovementType(description[12:len(description)].strip())
                        assetName = self.getColumnValueFromList(row, self.headerCetes["Emisora"])
                        assetNameSerie = self.getColumnValueFromList(row, self.headerCetes["Serie"])
                        importerMovementVO.setAssetSerie(assetNameSerie)
                        importerMovementVO.setAssetName(assetName)
                        importerMovementVO.setQuantity(self.replaceComma(self.getColumnValueFromList(row, self.headerCetes["tulos"])))
                        price = self.getColumnValueFromList(row, self.headerCetes["Precio"])
                        importerMovementVO.setPrice(self.replaceComma(price[0: price.find(" ", 0)]))
                        importerMovementVO.setRate(self.replaceComma(self.getColumnValueFromList(row, self.headerCetes["Tasa"])))
                        cargo = self.replaceComma(self.getColumnValueFromList(row, self.headerCetes["Cargo"]))
                        abono = self.replaceComma(self.getColumnValueFromList(row, self.headerCetes["Abono"]))
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
                        self.appendToMovementList(importerMovementVO, filterAssetName)
            return self.movementList

                
    def getMovementListFromGBM(self, filePath, fileName, imLO, filterAssetName, custody):
        json_data = self.getRawDataFromGBM(filePath)
        if (json_data is not None and len(json_data) != 0):
            date =  fileName.replace(".pdf", '')
            date = date.replace("GBM_","")
            fromDate = date + "-" + "01"
            fromDate =  pandas.to_datetime(datetime.strptime(fromDate, '%y-%m-%d')).to_pydatetime() 
            imLO.setFromDate(fromDate)
            imLO.setToDate(fromDate.replace(day = calendar.monthrange(fromDate.year, fromDate.month)[1]))
            self.movementList = []
            for index, key in enumerate(json_data):
                if index > 2:
                    dateAndExternalID = self.getColumnValueFromList(key, 0)
                    if dateAndExternalID != "":
                        paymentDate = dateAndExternalID[0: 2]
                        externalID = dateAndExternalID[dateAndExternalID.find(' ', 0)+1: len(dateAndExternalID)]
                        print (externalID)
                        paymentDate = date + "-" + paymentDate
                        paymentDate =  pandas.to_datetime(datetime.strptime(paymentDate, '%y-%m-%d')).to_pydatetime() 
                        print (paymentDate)
                        quantity = self.replaceComma(self.getColumnValueFromList(key, 4))
                        price = self.replaceComma(self.getColumnValueFromList(key, 5))
                        commission = self.replaceComma(self.getColumnValueFromList(key, 7))
                        commissionVAT = self.replaceComma(self.getColumnValueFromList(key, 9))
                        grossAmount = float(str('{0:.6f}'.format(float(price*quantity))))
                        importerMovementVO = ImporterMovementVO()
                        importerMovementVO.setPaymentDate(paymentDate)
                        importerMovementVO.setExternalID(externalID)
                        importerMovementVO.setOriginMovementType(self.getColumnValueFromList(key, 2))
                        importerMovementVO.setAssetName(self.getColumnValueFromList(key, 3))
                        importerMovementVO.setNetAmount(self.replaceComma(self.getColumnValueFromList(key, 10)))
                        importerMovementVO.setCustody(custody)
                        importerMovementVO.setQuantity(quantity)
                        importerMovementVO.setPrice(price)
                        importerMovementVO.setCommission(commission)
                        importerMovementVO.setCommissionVAT(commissionVAT)
                        importerMovementVO.setGrossAmount(grossAmount)
                        importerMovementVO.setComment("UPLOAD " + str(importerMovementVO.getPaymentDate())[0:7])
                        self.convertToPersistent(importerMovementVO)
                        self.appendToMovementList(importerMovementVO, filterAssetName)
            return self.movementList 
    
    def appendToMovementList(self, importerMovementVO, filterAssetName):
        if((filterAssetName == 'ALL' or filterAssetName == importerMovementVO.assetName or filterAssetName == importerMovementVO.persistentObject.asset.name)
                            and not (importerMovementVO.originMovementType in self.nonMovementTypeList)):
            if (importerMovementVO.persistentObject is not None):
                self.movementList.append(importerMovementVO.persistentObject)
            else:
                self.movementList.extend(importerMovementVO.persistentObjectList)
    

    def convertToPersistent(self, importerMovementVO):
        if (importerMovementVO.originMovementType in self.cashMovementTypeList):
            importerMovementVO.persistentObject = CashMovement(None)
            assetOID = self.getAssetbyName(importerMovementVO)
            importerMovementVO.persistentObject.setAttr("NEW", importerMovementVO.netAmount, self.getInOrOut(importerMovementVO.originMovementType), importerMovementVO.custody.OID, importerMovementVO.paymentDate, importerMovementVO.comment, importerMovementVO.externalID, assetOID)
        elif (importerMovementVO.originMovementType in self.movementTypeList):    
            importerMovementVO.persistentObject = Movement(None)
            assetOID = self.getAssetbyName(importerMovementVO)
            importerMovementVO.persistentObject.setAttr( "NEW", assetOID, self.getBuyOrSell(importerMovementVO.originMovementType), importerMovementVO.paymentDate, 
                                                            importerMovementVO.quantity, importerMovementVO.price, importerMovementVO.getRate(), importerMovementVO.grossAmount , 
                                                            importerMovementVO.netAmount, self.getCommissionPercentage(importerMovementVO.originMovementType), importerMovementVO.commission, importerMovementVO.commissionVAT, 
                                                            importerMovementVO.getTenor(), importerMovementVO.custody.OID, importerMovementVO.getMaturityDate(), importerMovementVO.externalID,
                                                            importerMovementVO.comment )
        elif (importerMovementVO.originMovementType in self.corporateEventTypeList): 
            importerMovementVO.persistentObject = CorporateEvent(None)
            assetOID = self.getAssetbyName(importerMovementVO)
            importerMovementVO.persistentObject.setAttr("NEW", importerMovementVO.custody.OID, mainCache.corporateEventTypeOID[1], assetOID, importerMovementVO.paymentDate, importerMovementVO.netAmount, importerMovementVO.netAmount, importerMovementVO.comment, importerMovementVO.externalID)
        elif (importerMovementVO.originMovementType == "ISR"):
            maturityDate = date(int('20' +importerMovementVO.assetSerie[:2]), int(importerMovementVO.assetSerie[2:4]), int(importerMovementVO.assetSerie[4:6]))
            totalAmount = 0
            movementRs = DaoMovement.getMovementsByMaturityDate(maturityDate)
            if len(movementRs) > 0:
                    for row in movementRs:
                        totalAmount += Decimal(row[1])
                    rowNum = 0    
                    for row in movementRs:    
                        movementID = row[0]
                        movement = Engine.getMovementByOID(movementID)
                        if movementID is not None:
                            tax = Tax(None)
                            tax.setAttr("NEW", 'MOVEMENT', movementID, round((movement.grossAmount/totalAmount) * Decimal(importerMovementVO.netAmount), 8) , importerMovementVO.externalID + "-" + str(rowNum))
                            movement.tax = tax
                            rowNum += 1
                            importerMovementVO.persistentObjectList.append(movement)
        elif(importerMovementVO.originMovementType in self.corporateEventTAXTypeList):
            try:
                oldPersisteObject = self.movementList[len(self.movementList)-1]
            except IndexError:
                return 
            assetOID = self.getAssetbyName(importerMovementVO)
            if (assetOID == oldPersisteObject.asset.OID):
                tax = Tax(None)
                tax.setAttr("NEW", 'CORPORATE_EVENT', None, importerMovementVO.netAmount, importerMovementVO.externalID)
                oldPersisteObject.tax = tax
                oldPersisteObject.netAmount =  float("%6.f" % (oldPersisteObject.grossAmount - importerMovementVO.netAmount))
        else:
            logging.warning(importerMovementVO.originMovementType)
     
     
####################################################################### TOOLS #################################################################################################     
     

    def getColumnValueFromList(self, row, indColumn):
        columnValue = row[indColumn]['text']
        return columnValue
     
                
    def getInOrOut(self, movementType):
        if any(movementType in s for s in self.cashMovementTypeOUTList):
            return Constant.CONST_OUT
        elif any(movementType in s for s in self.cashMovementTypeINList):
            return Constant.CONST_IN
        else:
            return 'NOT CATEGORY'
        
    def getBuyOrSell(self, movementType):
        if any(movementType in s for s in self.movementTypeBUYList):
            return Constant.CONST_BUY
        elif any(movementType in s for s in self.movementTypeSELLList):
            return Constant.CONST_SELL
        else:
            return 'NOT CATEGORY'

    def getCommissionPercentage(self, movementType):
        if(any(movementType in s for s in self.movementTypeCOMList)):
            return Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE
        else:
            return 0
    
    def replaceComma(self, value):
        if (value != ""):
            return Decimal(str('{0:.6f}'.format(float(float(value.replace(',',''))))))
    
    def getRawDataFromGBM(self, filePath):
        for page in range(4, 6):
            json_data = read_pdf(filePath, 'json', 'latin_1', pages=page)
            if (len(json_data) != 0):
                key = json_data[0]['data'][0][2]['text']
                if ("DESCRIPCI"  == key[0:9]):
                    return json_data[0]['data']
                
    def getRawDataFromCETESDIRECTO(self, filePath):
        for page in range(1, 3):
            json_data = read_pdf(filePath, 'json', 'latin_1', pages=page)
            if (len(json_data) != 0):
                for row in range(0, len(json_data[0]['data'])):
                    key = json_data[0]['data'][row][0]['text']
                    if (key.find("Fecha de") != -1):
                        return json_data[0]['data']
                
    def getAssetbyName(self, importerMovementVO):
        asset = self.assetDict.get(self.assetTranslator.get(importerMovementVO.assetName, importerMovementVO.assetName), None)
        if (asset is None):
            asset = self.assetDict.get(self.assetTranslator.get(importerMovementVO.getAssetNamePlusSerie(), None), None)
            if(asset is None):
                logging.warning("ASSET NOT FOUND " + importerMovementVO.assetName)
                return None
        return asset.OID

    def last_day_of_month(self, any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)
