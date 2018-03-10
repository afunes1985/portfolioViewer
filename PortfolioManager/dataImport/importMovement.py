import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoCashMovement
from engine.engine import Engine
from modelClass.movement import Movement


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()
#df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//Import_movement.xlsx');
#get the values for a given column
movementDateValues = df['Movement Date'].values
buySellValues = df['Buy Sell'].values
custodyValues = df['Custody'].values
quantityValues = df['Quantity'].values
priceValues = df['Price'].values
amountValues = df['Amount'].values
commentValues = df['Comment'].values
externalIDValues = df['External ID'].values
returnList = []
for index, rfRow in enumerate(movementDateValues):
        movementDate =  pandas.to_datetime(str(movementDateValues[index])).to_pydatetime()  
        buySell = buySellValues[index]
        custody = Engine.getCustodyDictName()[custodyValues[index]]
        amount = float(amountValues[index])
        comment = commentValues[index]
        
        m = Movement(None)
        m.setAttr(None, amount, inOut, custody.OID, movementDate, comment)
        newID = DaoCashMovement.insert(cm)
        #print(newID)
        print("movementDate " + str(movementDate))
        print("inOut " + str(inOut))
        print("custodyOID " + str(custody.OID))
        print("amount " + str(amount))
        print("comment " + str(comment))

