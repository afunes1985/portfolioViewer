'''
Created on Mar 9, 2017

@author: afunes
'''
from datetime import datetime
import threading

from dao.dao import DaoMovement, DaoAsset, DaoCorporateEvent, DaoCustody, \
    DaoCashMovement, DaoReportMovement, DaoTax
from logicObject.PnLLO import PnLLO
from logicObject.ReportMovementLO import ReportMovementLO
from modelClass import constant
from modelClass.cashMovement import CashMovement
from modelClass.constant import Constant
from modelClass.corporateEvent import CorporateEvent, Custody, \
    CorporateEventType
from modelClass.corporateEventPosition import CorporateEventPosition
from modelClass.movement import Asset, Movement
from modelClass.position import Position    
from modelClass.summaryItem import SummaryItem
from modelClass.tax import Tax


class Engine:
    
    @staticmethod
    def buildSummaryByCustody(positionDict, oldPositionDict, corporateEventPositionDict):
        summaryDict = {}
        #Positions
        for (positionKey, position) in positionDict.iteritems():
            summaryKey = position.custody.name + position.asset.assetType
            summaryItem = summaryDict.get(summaryKey)
            if (summaryItem == None):
                summaryItem = SummaryItem(position)
                summaryDict[summaryKey] = summaryItem
            else:
                summaryItem.sumPosition(position)
        #Old positions 
        for (positionKey, oldPosition) in oldPositionDict.iteritems():
            summaryKey = oldPosition.custody.name + oldPosition.asset.assetType
            summaryItem = summaryDict.get(summaryKey)
            if (summaryItem == None):
                summaryItem = SummaryItem(oldPosition) #arreglar porque cuando no hay posicion de bonos suma en el summary
                summaryDict[summaryKey] = summaryItem
                summaryItem.addRealizedPnl(oldPosition.realizedPnl)
            else:
                summaryItem.addRealizedPnl(oldPosition.realizedPnl)
        #Corporate event        
        for (positionKey, corporateEventPosition) in corporateEventPositionDict.iteritems():
            summaryKey = corporateEventPosition.custody.name + corporateEventPosition.asset.assetType
            summaryItem = summaryDict.get(summaryKey)
            summaryItem.addRealizedPnl(corporateEventPosition.accNetAmount)
        #Sub Total
        subTotalSummary = {}
        for (sumKey, summaryItem) in summaryDict.iteritems():
            summaryKey = summaryItem.custodyName+"Z"
            subTotalSummaryItem = subTotalSummary.get(summaryKey)
            if (subTotalSummaryItem is None):
                subTotalSummaryItem = SummaryItem(summaryItem)
                subTotalSummary[summaryKey] = subTotalSummaryItem
            else:
                subTotalSummaryItem.sumSubTotal(summaryItem)
        #Grand total
        grandTotalSummaryItem = SummaryItem(None)
        for (summaryKey, summaryItem) in summaryDict.iteritems():
            grandTotalSummaryItem.sumSubTotal(summaryItem)
        summaryDict["TOTAL"] = grandTotalSummaryItem  
        #Merge
        summaryDict.update(subTotalSummary)
        sorted(summaryDict)
        
        return summaryDict         
    
    @staticmethod
    def getAccRealizedPnl(positionDict):
        accRealizedPnl = 0
        for key, position in positionDict.items():
            accRealizedPnl += position.getNetPnL()
        return accRealizedPnl       
                
    @staticmethod
    def getSubTotalInvestedAmount(positionDict, assetType ,isSIC):
        subTotalInvestedAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalInvestedAmount += position.getInvestedAmount()
        return subTotalInvestedAmount
    
    @staticmethod
    def getSubTotalValuatedAmount2(positionDict, assetType):
        return Engine.getSubTotalValuatedAmount(positionDict, assetType ,None)
    
    @staticmethod
    def getAccPositionPercentage(positionDict, assetType, isSIC):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accPositionPercentage = (accValuatedAmount * 100) / mainCache.totalValuatedAmount
        return accPositionPercentage
    
    @staticmethod
    def getAccGrossPnlPercentage(positionDict, assetType, isSIC):
        accGrossPnlPercentage = 0
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        if (accInvestedAmount != 0):
            accGrossPnlPercentage = (accValuatedAmount / accInvestedAmount -1 ) * 100
        return accGrossPnlPercentage
    
    @staticmethod
    def getAccWeightedPNL(positionDict, assetType, isSIC):
        accGrossPnlPercentage = Engine.getAccGrossPnlPercentage(positionDict, assetType, isSIC)
        accPositionPercentage = Engine.getAccPositionPercentage(positionDict, assetType, isSIC)
        accWeightedPNL = accGrossPnlPercentage * accPositionPercentage / 100
        return accWeightedPNL
    
    @staticmethod
    def getAccNetPnlPercentage(positionDict, assetType, isSIC):
        subTotalNetPnlPercentage = 0
        accBuyCommissionAmount = Engine.getAccBuyCommissionAmount(positionDict, assetType, isSIC)
        accBuyVATCommissionAmount = Engine.getAccBuyCommissionVATAmount(positionDict, assetType, isSIC)
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        if (accInvestedAmount != 0):
            subTotalNetPnlPercentage = (accValuatedAmount / (accInvestedAmount + accBuyCommissionAmount + accBuyVATCommissionAmount) -1 ) * 100
        return subTotalNetPnlPercentage
    
    @staticmethod
    def getTotalValuatedAmount():
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        return mainCache.totalValuatedAmount
    
    @staticmethod
    def getSubTotalValuatedAmount(positionDict, assetType ,isSIC):
        subTotalValuatedAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            subTotalValuatedAmount += position.getValuatedAmount()
        return subTotalValuatedAmount
    
    @staticmethod
    def getSubTotalValuatedAmountByCustodyOID(positionDict, custodyOID):
        subTotalValuatedAmount = 0
        positionList = Engine.getPositionByCustodyOID(positionDict, custodyOID)
        for position in positionList:
            subTotalValuatedAmount += position.getValuatedAmount()
        return subTotalValuatedAmount
    
    @staticmethod
    def getAccBuyCommissionAmount(positionDict, assetType ,isSIC):
        accBuyCommissionAmount = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                accBuyCommissionAmount += position.accumulatedBuyCommission
        return accBuyCommissionAmount
    
    @staticmethod
    def getAccBuyCommissionVATAmount(positionDict, assetType ,isSIC):
        accuBuyVATCommission = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                accuBuyVATCommission += position.accumulatedBuyVATCommission
        return accuBuyVATCommission
    
    @staticmethod
    def getAccRealizedPnL(positionDict, assetType ,isSIC):
        accRealizedPnl = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            accRealizedPnl += position.realizedPnl
        return accRealizedPnl
    
    @staticmethod
    def getPositionByAssetType(positionDict, assetType ,isSIC):
        positionList = []
        for key, position in positionDict.items():
            if assetType == 'ALL' or (position.asset.assetType == assetType and position.asset.isSIC == isSIC):
                positionList.append(position)
        return positionList
    
    @staticmethod
    def getPositionByCustodyOID(positionDict, custodyOID):
        positionList = []
        for key, position in positionDict.items():
            if position.custody.OID == custodyOID or custodyOID is None:
                positionList.append(position)
        return positionList
    
    @staticmethod
    def getSubtotalGrossPNL(positionDict, assetType ,isSIC):
        subTotalGrossPNL = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                subTotalGrossPNL += position.getGrossPnL()
        return subTotalGrossPNL
    
    @staticmethod
    def getAccNetPNL(positionDict, assetType ,isSIC):
        subTotalNetPNL = 0
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            if position.totalQuantity != 0:
                subTotalNetPNL += position.getNetPnL()
        return subTotalNetPNL
    
    @staticmethod
    def getPortfolioPercentage(positionDict, valuatedAmount):
        totalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, 'ALL', 0)
        return (valuatedAmount * 100) / totalValuatedAmount
        
    @staticmethod
    def getAssetDict():
        assetRS = DaoAsset().getAssetList()
        assetDict = {}
        for (assetRow) in assetRS:
            asset = Asset(assetRow)
            assetDict[asset.name] = asset
        return assetDict 
     
    @staticmethod
    def getAssetDictByOriginName():
        assetRS = DaoAsset().getAssetList()
        assetDict = {}
        for (assetRow) in assetRS:
            asset = Asset(assetRow)
            assetDict[asset.originName] = asset
        return assetDict 

    @staticmethod
    def getAssetDictOID():
        assetRS = DaoAsset().getAssetList()
        assetDict = {}
        for (assetRow) in assetRS:
            asset = Asset(assetRow)
            assetDict[asset.OID] = asset
        return assetDict  
        
    @staticmethod
    def getCustodyDictName():
        rs = DaoCustody().getCustodyList()
        returnDict = {}
        for (row) in rs:
            obj = Custody(row)
            returnDict[obj.name] = obj
        return returnDict
    
    @staticmethod
    def getCustodyDictOID():
        rs = DaoCustody().getCustodyList()
        returnDict = {}
        for (row) in rs:
            obj = Custody(row)
            returnDict[obj.OID] = obj
        return returnDict      
    
    @staticmethod
    def getTaxByOriginID(originType, originOID):
        rs = DaoTax.getTaxByOriginID(originType, originOID)
        for (taxRow) in rs:
            tax = Tax(taxRow)
            return tax
    
    @staticmethod
    def getMovementsByDate(assetName, fromDate, toDate):
        movementList = []
        movementRS = DaoMovement.getMovementsByDate(assetName, fromDate, toDate)
        for (movementRow) in movementRS:
            movement = Movement(movementRow)
            tax = Engine.getTaxByOriginID(movement.getMovementType(), movement.OID)
            movement.tax = tax
            movementList.append(movement)
        return movementList
    
    @staticmethod
    def buildPositions(fromDate, toDate, setLastMarketData):
        movementList = Engine.getMovementsByDate(None, fromDate, toDate)
        positionDict = {}
        oldPositionDict = {}
        threads = []
        today = datetime.now().date()
        for (movement) in movementList:
            position = None
            asset = movement.asset
            assetName = asset.name
            if(asset.assetType == 'BOND'):
                assetName = assetName + str(movement.OID)
            position =  positionDict.get(assetName, None)
            if position == None:
                position = Position(asset, movement)
                positionDict[assetName] = position
            else:           
                position.addMovement(movement)
            #pasa la posicion al viejo diccionario de posiciones si no tiene mas posición o esta vencida
            if (position.asset.assetType == 'BOND'
                 and ((position.isMatured and today == toDate)
                    or (position.maturityDate.date() < toDate and today != toDate))
                or position.totalQuantity == 0):
                oldPosition =  oldPositionDict.get(assetName, None)
                if oldPosition == None:
                    oldPositionDict[assetName] = position
                else:
                    oldPosition.addPositionToOldPosition(position)#TODO TESTEAR
                positionDict.pop(assetName, None)
        if setLastMarketData:         
            for key, position2 in positionDict.items():
                t = threading.Thread(target=position2.refreshMarketData)
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()
        
        returnDict = {}
        returnDict[Constant.CONST_POSITION_DICT] = positionDict
        returnDict[Constant.CONST_OLD_POSITION_DICT] = oldPositionDict
        return returnDict

    
    @staticmethod
    def getMovementListByAsset(assetName, fromDate, toDate):
        movementRS = DaoMovement.getMovementsByDate(assetName, fromDate, toDate)
        movementList = []
        for (movementRow) in movementRS:
            movement = Movement(movementRow)
            movementList.append(movement)
        return movementList
   
    @staticmethod
    def getMovementByOID(movementOID):
        movementRS = DaoMovement.getMovementByOID(movementOID)
        for (movementRow) in movementRS:
            movement = Movement(movementRow)
            return movement
    @staticmethod
    def buildCorporateEventPosition():
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        resultDict = {}
        resultSet = DaoCorporateEvent.getCorporateEventList()
        for (row) in resultSet:
            o = CorporateEvent(row)
            corporateEventPosition = resultDict.get(o.asset.name, None)
            if corporateEventPosition == None:
                resultDict[o.asset.name] = CorporateEventPosition(o)
            else:
                corporateEventPosition.addCorporateEvent(o)
        mainCache.corporateEventPositionDictAsset = resultDict
    
    @staticmethod
    def getCorporateEventTypeDictOID():
        rs = DaoCorporateEvent().getCorporateEventTypeList()
        returnDict = {}
        for (row) in rs:
            obj = CorporateEventType(row)
            returnDict[obj.OID] = obj
        return returnDict
    
    @staticmethod
    def getCashMovementList(fromDate, toDate):
        rs = DaoCashMovement().getCashMovement(fromDate, toDate)
        returnList = []
        for (row) in rs:
            obj = CashMovement(row)
            returnList.append(obj)
        return returnList
       
    @staticmethod
    def buildPnlLogicObject(fromDate, toDate): 
        pnlLO = PnLLO()
        pnlLO.setCashMovement(Engine.getCashMovementList(fromDate, toDate))
        pnlLO.setPnlVOlist(pnlLO.calculatePnL(fromDate, toDate))
        return pnlLO
        
    @staticmethod
    def getReportMovementList(fromDate, toDate, movementType, assetName, custodyName): 
        reportMovementLO = ReportMovementLO()
        reportMovementLO.setMovementList(DaoReportMovement.getMovements(fromDate, toDate, movementType, assetName, custodyName))
        return reportMovementLO
    
    @staticmethod
    def getAssetTranslatorDict():
        rs = DaoAsset().getAssetTranslatorList()
        returnDict = {}
        for (row) in rs:
            returnDict[row[0]] = row[1]
        return returnDict
    
        
        
        
        
        
