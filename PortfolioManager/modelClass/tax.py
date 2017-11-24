'''
Created on 21 nov. 2017

@author: afunes
'''
class Tax():
    OID = None
    originType = None
    originOID = None
    taxAmount = None
    
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1], row[2])
    
    def setAttr(self, OID, originType, originOID, taxAmount):
        self.OID = OID
        self.originType = originType
        self.originOID = originOID
        self.taxAmount = taxAmount