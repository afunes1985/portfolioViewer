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
    custodyName = None
    corporateEventTypeName = None
        
    def __init__(self, corporateEventRow):
        if(corporateEventRow is not None):
            self.OID = corporateEventRow[0]
            self.custodyName = corporateEventRow[1]
            self.corporateEventTypeName = corporateEventRow[2]
            self.assetName = corporateEventRow[3]
            self.paymentDate = corporateEventRow[4]
            self.grossAmount = corporateEventRow[5]
    
    def getPaymentDate(self):
        return self.acquisitionDate.strftime("%Y-%m-%d")
