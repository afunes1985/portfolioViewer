import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoCashMovement
from engine.engine import Engine
from modelClass.cashMovement import CashMovement


mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()
#df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//Import_cash_movement.xlsx');
#get the values for a given column
movementDateValues = df['Movement Date'].values
inOutValues = df['In Out'].values
custodyValues = df['Custody'].values
amountValues = df['Amount'].values
commentValues = df['Comment'].values
returnList = []
for index, rfRow in enumerate(movementDateValues):
        movementDate =  pandas.to_datetime(str(movementDateValues[index])).to_pydatetime()  
        inOut = inOutValues[index]
        custody = Engine.getCustodyDictName()[custodyValues[index]]
        amount = float(amountValues[index])
        comment = commentValues[index]
        
        cm = CashMovement(None)
        cm.setAttr(None, amount, inOut, custody.OID, movementDate, comment)
        newID = DaoCashMovement.insert(cm)
        #print(newID)
        print("movementDate " + str(movementDate))
        print("inOut " + str(inOut))
        print("custodyOID " + str(custody.OID))
        print("amount " + str(amount))
        print("comment " + str(comment))

