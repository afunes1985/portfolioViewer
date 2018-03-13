import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoMovement, DaoCashMovement
from engine.engine import Engine
from modelClass.cashMovement import CashMovement
from modelClass.movement import Movement


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
    if movementType == 'CASH' and direction == 'IN':
        try:
            rs = DaoCashMovement.getCashMovementsByExternalID(externalID)
            if len(rs) == 0:
                m = CashMovement(None)
                m.setAttr(None, amount, direction, custodyOID, acquisitionDate, comment, externalID)
                newID = DaoCashMovement.insert(m)
                #print(newID)
                print("ADD externalID " + str(externalID) + " ID: " + str(newID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
        except Exception as e:
            print(e)
            print (externalID)
    #===========================================================================
    # elif movementType == 'CETES': 
    #     assetOID = assetDictByName[assetNameValues[index]].OID
    #     quantity = int(quantityValues[index])
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
    #         #print(newID)
    #         print("ADD externalID " + str(externalID))
    #     else:
    #         print("CANNOT ADD externalID " + str(externalID))
    #===========================================================================
