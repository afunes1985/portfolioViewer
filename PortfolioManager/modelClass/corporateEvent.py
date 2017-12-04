'''
Created on Mar 18, 2017

@author: afunes
'''

class CorporateEvent():
    OID = None
    asset = None
    paymentDate = None
    grossAmount = 0
    custody = None
    corporateEventType = None
    netAmount = 0
    comment = None
        
    def __init__(self, corporateEventRow):
        from core.cache import Singleton, MainCache
        if(corporateEventRow is not None):
            mainCache = Singleton(MainCache)
            self.setAttr(corporateEventRow[0], mainCache.custodyDictOID[corporateEventRow[1]], mainCache.corporateEventTypeOID[corporateEventRow[2]], mainCache.assetDictOID[corporateEventRow[3]], corporateEventRow[4], corporateEventRow[5], corporateEventRow[6], corporateEventRow[7])
    
    def setAttr(self, OID, custody, corporateEventType, asset, paymentDate, grossAmount, netAmount, comment):
        self.OID = OID
        self.custody = custody
        self.corporateEventType = corporateEventType
        self.asset = asset
        self.paymentDate = paymentDate
        self.grossAmount = grossAmount
        self.netAmount = netAmount
        self.comment = comment
        
class Custody():
    OID = None
    name = None
    
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1])
    
    def setAttr(self, OID, name):
        self.OID = OID
        self.name = name

class CorporateEventType():
    OID = None
    name = None
    
    def __init__(self, row):
        if(row is not None):
            self.setAttr(row[0], row[1])
    
    def setAttr(self, OID, name):
        self.OID = OID
        self.name = name