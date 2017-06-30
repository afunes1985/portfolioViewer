'''
Created on Mar 18, 2017

@author: afunes
'''
class CorporateEvent():
    OID = None
    assetName = None
    assetOID = None
    asset = None
    paymentDate = None
    grossAmount = 0
    custody = None
    corporateEventTypeOID = None
        
    def __init__(self, corporateEventRow):
        if(corporateEventRow is not None):
            self.OID = corporateEventRow[0]
            self.assetName = corporateEventRow[1]
            self.paymentDate = corporateEventRow[2]
            self.grossAmount = corporateEventRow[3]
    
    def getPaymentDate(self):
        return self.acquisitionDate.strftime("%Y-%m-%d")
