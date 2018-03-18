'''
Created on 17 mar. 2018

@author: afunes
'''
class Price():
    
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1], row[2], row[3])
    
    def setAttr(self, OID, assetOID, lastPrice, date):
        self.OID = OID
        self.assetOID = assetOID
        self.lastPrice = lastPrice
        self.date = date
