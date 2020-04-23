'''
Created on Jan 8, 2020

@author: afunes
'''
from dao.movementDao import MovementDao
import pandas as pd

class MovementEngine():
    
    def getMovementsByDate(self, fromDate, toDate):
        return MovementDao().getMovementsByDate(fromDate, toDate)
    
    def getMovementsForReport(self, fromDate, toDate):
        movement_DF = pd.DataFrame(columns=['Asset Name','Buy Sell','Acquisition Date','Quantity','Price','Gross Amount','Net Amount','Comm %','Comm Amount','Comm VAT Amount'])
        rs = MovementDao().getMovementsForReport(fromDate, toDate)
        for row in rs:
            movement_DF = movement_DF.append(pd.Series([row.name, row.buySell, row.acquisitionDate.strftime("%Y-%m-%d"), row.quantity, row.price, row.grossAmount, row.netAmount, row.commissionPercentage, row.commissionAmount, row.commissionVATAmount], index=movement_DF.columns), ignore_index=True)
        return movement_DF