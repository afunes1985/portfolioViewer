'''
Created on 4 dic. 2017

@author: afunes
'''
from _decimal import Decimal


class CorporateEventPosition():
    asset = None
    accGrossAmount = Decimal(0)
    custody = None
    #corporateEventType = None
    accNetAmount = Decimal(0)
    corporateEventList = None
    
    def __init__(self, corporateEvent):
        self.corporateEventList = []
        self.addCorporateEvent(corporateEvent)
        
        
    def addCorporateEvent(self, corporateEvent):
        self.corporateEventList.append(corporateEvent)
        self.accGrossAmount += corporateEvent.grossAmount
        self.accNetAmount += corporateEvent.netAmount
        self.custody = corporateEvent.custody
        self.asset = corporateEvent.asset
        #self.corporateEventType = corporateEvent.corporateEventType