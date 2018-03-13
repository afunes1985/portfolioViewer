import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoMovement
from engine.engine import Engine
from modelClass.movement import Movement


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()
#df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//Import_movement.xlsx');
#get the values for a given column
movementDateValues = df['Movement Date'].values
assetNameValues = df['Asset Name'].values
buySellValues = df['Buy Sell'].values
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
    if assetNameValues[index] == 'CETES' and buySellValues[index] == 'BUY':
        assetOID = assetDictByName[assetNameValues[index]].OID
        buySell = buySellValues[index]
        acquisitionDate =  pandas.to_datetime(str(movementDateValues[index])).to_pydatetime()  
        quantity = int(quantityValues[index])
        price = float(priceValues[index])
        rate = round(float(rateValues[index])/100, 5)
        amount = float(amountValues[index])
        grossAmount = float(amount)
        netAmount = float(amount)
        custodyOID = custodyDictByName[custodyValues[index]].OID
        comment = commentValues[index]
        externalID = externalIDValues[index]
        tenor = int(tenorValues[index])
        rs = DaoMovement.getMovementsByExternalID(externalID)
        try:
            if len(rs) == 0:
                m = Movement(None)
                m.setAttr( None, assetOID, buySell, acquisitionDate, quantity, price, rate, grossAmount, netAmount, 0, 0, 0, externalID, custodyOID, comment, tenor)
                newID = DaoMovement.insertMovement(m)
                #print(newID)
                print("ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
        except Exception as e:
            print(e)
            print (price)