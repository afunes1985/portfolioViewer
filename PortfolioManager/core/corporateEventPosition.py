'''
Created on 4 dic. 2017

@author: afunes
'''

class CorporateEventPosition():
    asset = None
    accGrossAmount = 0
    custody = None
    corporateEventType = None
    accNetAmount = 0
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
        self.corporateEventType = corporateEvent.corporateEventType