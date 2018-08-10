'''
Created on 7 ago. 2018

@author: afunes
'''
class FAItem():
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1], row[2])
    
    def setAttr(self, OID, section, name):
        self.OID = OID
        self.section = section
        self.itemName = name