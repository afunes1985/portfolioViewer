from datetime import date
import logging

import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoMovement, DaoCashMovement, DaoTax
from engine.engine import Engine
from modelClass.cashMovement import CashMovement
from modelClass.movement import Movement
from modelClass.tax import Tax


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()
#df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//Import_movement.xlsx');
#get the values for a given column
movementDateValues = df['Movement Date'].values
assetNameValues = df['Asset Name'].values
movementTypeValues = df['Movement Type'].values
directionValues = df['Direction'].values
custodyValues = df['Custody'].values
quantityValues = df['Quantity'].values
priceValues = df['Price'].values
amountValues = df['Amount'].values
commentValues = df['Comment'].values
externalIDValues = df['External ID'].values
rateValues = df['Rate'].values
tenorValues = df['Tenor'].values
serieValues = df['Serie'].values
returnList = []
assetDictByName = Engine.getAssetDict()
custodyDictByName = Engine.getCustodyDictName()
for index, rfRow in enumerate(movementDateValues):
    movementType = movementTypeValues[index]
    acquisitionDate =  pandas.to_datetime(str(movementDateValues[index])).to_pydatetime()
    amount = float(amountValues[index])
    direction = directionValues[index]
    custodyOID = custodyDictByName[custodyValues[index]].OID
    comment = commentValues[index]
    externalID = externalIDValues[index]
    serie = str(serieValues[index])
    assetName  = assetNameValues[index]
    quantity = int(quantityValues[index])
    if movementType == 'BOND' and direction == 'ISR' and assetName == 'CETES':
        try:
            totalAmount = 0
            rs = DaoTax.getTaxByExternalID(externalID + "-" + str(0))
            if len(rs) == 0:
                maturityDate = date(int('20' +serie[:2]), int(serie[2:4]), int(serie[4:6]))
                movementRs = DaoMovement.getMovementsByMaturityDate(maturityDate)
                if len(movementRs) > 0:
                    for row in movementRs:
                        totalAmount += float(row[1])
                    
                    rowNum = 0    
                    for row in movementRs:    
                        movementID = row[0]
                        grossAmount = float(row[1])
                        if movementID is not None:
                            t = Tax(None)
                            t.setAttr(None, 'MOVEMENT', movementID, round((grossAmount/totalAmount) * amount, 8) , externalID + "-" + str(rowNum))
                            newID = DaoTax.insert(t)
                            rowNum += 1
                            print("ADD externalID " + str(externalID) + " ID: " + str(newID))
                else:
                    logging.warning("CANNOT ADD externalID :" + str(externalID))
            else:
                logging.warning("Exists externalID :" + str(externalID))
        except Exception as e:
            print(e)
            print (externalID)
    #===========================================================================
    # elif movementType == 'CASH' and direction == 'IN':
    #     try:
    #         rs = DaoCashMovement.getCashMovementsByExternalID(externalID)
    #         if len(rs) == 0:
    #             m = CashMovement(None)
    #             m.setAttr(None, amount, direction, custodyOID, acquisitionDate, comment, externalID)
    #             newID = DaoCashMovement.insert(m)
    #             print("ADD externalID " + str(externalID) + " ID: " + str(newID))
    #         else:
    #             print("CANNOT ADD externalID " + str(externalID))
    #     except Exception as e:
    #         print(e)
    #         print (externalID)
    # elif movementType == 'CETES': 
    #     assetOID = assetDictByName[assetNameValues[index]].OID
    #     price = float(priceValues[index])
    #     grossAmount = float(amount)
    #     netAmount = float(amount)
    #     tenor = int(tenorValues[index])
    #     rate = round(float(rateValues[index])/100, 5)
    #     rs = DaoMovement.getMovementsByExternalID(externalID)
    #     if len(rs) == 0:
    #         m = Movement(None)
    #         m.setAttr( None, assetOID, direction, acquisitionDate, quantity, price, rate, grossAmount, netAmount, 0, 0, 0, externalID, custodyOID, comment, tenor)
    #         newID = DaoMovement.insertMovement(m)
    #         print("ADD externalID " + str(externalID))
    #     else:
    #         print("CANNOT ADD externalID " + str(externalID))
    #===========================================================================
