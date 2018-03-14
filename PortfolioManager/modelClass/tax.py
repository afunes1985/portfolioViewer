'''
Created on 21 nov. 2017

@author: afunes
'''
class Tax():
    
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1], row[2], None)
    
    def setAttr(self, OID, originType, originOID, taxAmount, externalID):
        self.OID = OID
        self.originType = originType
        self.originOID = originOID
        self.taxAmount = taxAmount
        self.externalID = externalID