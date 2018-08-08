'''
Created on 7 ago. 2018

@author: afunes
'''
class Company():
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1], row[2])
    
    def setAttr(self, OID, companyID, name):
        self.OID = OID
        self.companyID = companyID
        self.name = name