from datetime import datetime
from decimal import Decimal

import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoCorporateEvent, DaoTax, DaoMovement
from engine.engine import Engine
from modelClass.corporateEvent import CorporateEvent
from modelClass.movement import Movement
from modelClass.tax import Tax

class tools():
    @staticmethod
    def getNextPointBySpace(data, startPoint, steps):
        nextStep = startPoint
        while steps != 0:
            nextStep = data.find(' ', nextStep) + 1
            steps = steps - 1
        return nextStep


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()
#df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//GBM_Import_Movement.xlsx');
#get the values for a given column
dataValues = df['DATA'].values
commentValues = df['Comment'].values
returnList = []
grossAmount = 0
isrAmount = 0
assetDictSIC = Engine.getAssetDictByOriginName()
assetDict = Engine.getAssetDict()
types = {'ABONO DIVIDENDO EMISORA EXTRANJERA' : 'DIVIDENDO', 
         'ISR 10 % POR DIVIDENDOS SIC' : 'ISR_DIVIDENDO', 
         'Compra Soc. de Inv. - Cliente' : 'FUND_BUY', 
         'Compra de Acciones.' : 'EQUITY_BUY', 
         'Venta Soc. de Inv. - Cliente' : 'FUND_SELL'}
custodyDictByName = Engine.getCustodyDictName()
assetTranslator = {'GBMF2' : 'GBMF2BF.MX'}
for index, rfRow in enumerate(dataValues):
        custodyOID = custodyDictByName['GBM'].OID
        paymentDate = None
        data = dataValues[index]
        nextPoint = 0
        paymentDate = data[nextPoint:10]
        paymentDate =  pandas.to_datetime(datetime.strptime(paymentDate, '%d/%m/%Y')).to_pydatetime()  
        nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
        externalID = data[nextPoint: data.find(' ', nextPoint)]
        nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
        for key, value in types.iteritems(): 
            result = data.find(key)
            if result != -1:
                eventType = value
                nextPoint += len(key) + 1
        if (eventType =='DIVIDENDO' and 1==2):
            assetName = data[nextPoint: data.find(' ', nextPoint)]
            asset = assetDictSIC[assetName]
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 7)
            amount = data[nextPoint: data.find(' ', nextPoint)]
            grossAmount = float(amount)
            netAmount = grossAmount
            comment = commentValues[index]
            rs = DaoCorporateEvent.getCorporateEventByExternalID(externalID)
            if len(rs) == 0:
                ce = CorporateEvent(None)
                ce.setAttr(None, asset.defaultCustody, mainCache.corporateEventTypeOID[1], asset, paymentDate, grossAmount, netAmount, comment, externalID)
                newID = DaoCorporateEvent.insert(ce)
                print(newID)
                isrAmount = 0
                amount = 0
                print("ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
        if (eventType == 'ISR_DIVIDENDO' and 1==2):
            assetName = data[nextPoint: data.find(' ', nextPoint)]
            asset = assetDictSIC[assetName]
            ce = DaoCorporateEvent().getCorporateEventByDateAndAsset(paymentDate, asset.OID)
            if (ce is not None):
                nextPoint = tools.getNextPointBySpace(data, nextPoint, 7)
                isrAmount = float(data[nextPoint: data.find(' ', nextPoint)])
                rs = DaoTax.getTaxByExternalID(externalID);
                if len(rs) == 0:
                    tax = Tax(None)
                    tax.setAttr(None, 'CORPORATE_EVENT', ce[0][0], isrAmount, externalID)
                    DaoTax.insert(tax)
                    DaoCorporateEvent.updateNetAmount(ce[0][0], float("%4.f" % (ce[0][1] - Decimal(isrAmount))))
                    print("ADD externalID " + str(externalID))
                else:
                    print("CANNOT ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
        if (eventType == 'EQUITY_BUY' and 1==2):
            assetName = data[nextPoint: data.find(' ', nextPoint)]
            asset = assetDictSIC[assetName]
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 2)
            quantity = int(data[nextPoint: data.find(' ', nextPoint)])
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            price = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            commissionAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 2)
            taxAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            netAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            comment = commentValues[index]
            grossAmount = price * quantity
            rs = DaoMovement.getMovementsByExternalID(externalID)
            if len(rs) == 0:
                m = Movement(None)
                m.setAttr( None, asset.OID, 'BUY', paymentDate, quantity, price, None, grossAmount, netAmount, 0.0025, commissionAmount, taxAmount, externalID, custodyOID, comment, None, None)
                newID = DaoMovement.insertMovement(m)
                print("ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
        if (eventType == 'FUND_BUY' and 1==2):
            assetName = data[nextPoint: data.find(' ', nextPoint)]
            asset = assetDict[assetTranslator[assetName]]
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 2)
            quantity = int(data[nextPoint: data.find(' ', nextPoint)])
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            price = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            commissionAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 2)
            taxAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            netAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            comment = commentValues[index]
            rs = DaoMovement.getMovementsByExternalID(externalID)
            if len(rs) == 0:
                m = Movement(None)
                m.setAttr( None, asset.OID, 'BUY', paymentDate, quantity, price, None, netAmount, netAmount, 0, commissionAmount, taxAmount, externalID, custodyOID, comment, None, None)
                newID = DaoMovement.insertMovement(m)
                print("ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
        if (eventType == 'FUND_SELL'):
            assetName = data[nextPoint: data.find(' ', nextPoint)]
            asset = assetDict[assetTranslator[assetName]]
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 2)
            quantity = int(data[nextPoint: data.find(' ', nextPoint)])
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            price = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            commissionAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 2)
            taxAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            nextPoint = tools.getNextPointBySpace(data, nextPoint, 1)
            netAmount = float(data[nextPoint: data.find(' ', nextPoint)].replace(',',''))
            comment = commentValues[index]
            rs = DaoMovement.getMovementsByExternalID(externalID)
            if len(rs) == 0:
                m = Movement(None)
                m.setAttr( None, asset.OID, 'SELL', paymentDate, quantity, price, None, netAmount, netAmount, 0, commissionAmount, taxAmount, externalID, custodyOID, comment, None, None)
                newID = DaoMovement.insertMovement(m)
                print("ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
            print (asset.name)
            print (quantity)    
            print (price)
            print (commissionAmount)
            print (taxAmount) 
            print (netAmount) 
            print (paymentDate)
            