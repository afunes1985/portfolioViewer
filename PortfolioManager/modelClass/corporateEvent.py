'''
Created on Mar 18, 2017

@author: afunes
'''
from modelClass.constant import Constant


class CorporateEvent():
    OID = None
    asset = None
    paymentDate = None
    grossAmount = 0
    custody = None
    corporateEventType = None
    netAmount = 0
    comment = None
    externalID = None
    tax = None
        
    def __init__(self, corporateEventRow):
        from core.cache import Singleton, MainCache
        if(corporateEventRow is not None):
            mainCache = Singleton(MainCache)
            self.setAttr(corporateEventRow[0],corporateEventRow[1] , mainCache.corporateEventTypeOID[corporateEventRow[2]], corporateEventRow[3], corporateEventRow[4], corporateEventRow[5], corporateEventRow[6], corporateEventRow[7], corporateEventRow[8])
    
    def setAttr(self, OID, custodyOID, corporateEventType, assetOID, paymentDate, grossAmount, netAmount, comment, externalID):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        self.OID = OID
        self.custody = mainCache.custodyDictOID[custodyOID]
        self.corporateEventType = corporateEventType
        self.asset = mainCache.assetDictOID.get(assetOID, None)
        self.paymentDate = paymentDate
        self.grossAmount = grossAmount
        self.netAmount = netAmount
        self.comment = comment
        self.externalID = externalID
        
    def getMovementType(self):
        return Constant.CONST_CORP_EVENT_TYPE

    def getMovementSubType(self):
        return Constant.CONST_CORP_EVENT_SUB_TYPE
    
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