'''
Created on 18 mar. 2018

@author: afunes
'''

class CurrencyValue():
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1], row[2], row[3])
    
    def setAttr(self, OID, currencyOID, date, value):
        self.OID = OID
        self.currencyOID = currencyOID
        self.date = date
        self.value = value