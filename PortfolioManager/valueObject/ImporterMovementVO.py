'''
Created on 29 ene. 2018

@author: afunes
'''
import datetime


class ImporterMovementVO():
    
    def __init__(self):
        self.paymentDate = None
        self.externalID = None
        self.assetName = None
        self.quantity = None
        self.price = None
        self.rate = 0
        self.netAmount =  None
        self.grossAmount =  None
        self.comment = None
        self.commission = 0
        self.commissionVAT = 0
        self.originMovementType = None
        self.custody = None
        self.tenor = None
        self.persistentObject = None

    def setPaymentDate(self, paymentDate):
        self.paymentDate = paymentDate
    
    def setExternalID(self, externalID):
        self.externalID = externalID
        
    def setAssetName(self, assetName):
        self.assetName = assetName

    def setQuantity(self, quantity):
        self.quantity = quantity
        
    def setPrice(self, price):
        self.price = price
        
    def setRate(self, rate):
        self.rate = rate
        
    def setNetAmount(self, netAmount):
        self.netAmount = netAmount
        
    def setGrossAmount(self, grossAmount):
        self.grossAmount = grossAmount
        
    def setComment(self, comment):
        self.comment = comment
    
    def setCommission(self, commission):
        self.commission = commission
        
    def setCommissionVAT(self, commissionVAT):
        self.commissionVAT = commissionVAT
        
    def setOriginMovementType(self, originMovementType):
        self.originMovementType = originMovementType

    def setCustody(self, custody):
        self.custody = custody
    
    def getPaymentDate(self):
        return self.paymentDate
    
    def getExternalID(self):
        return self.externalID
        
    def getAssetName(self):
        return self.assetName

    def getQuantity(self):
        return self.quantity
        
    def getPrice(self):
        return self.price
        
    def getRate(self):
        if (self.rate != 0):
            return self.rate / 100
        return None
        
    def getNetAmount(self):
        return self.netAmount
        
    def getGrossAmount(self):
        return self.grossAmount
        
    def getComment(self):
        return self. comment
    
    def getCommission(self):
        return self. commission
        
    def getCommissionVAT(self):
        return self. commissionVAT
        
    def getOriginMovementType(self):
        return self.originMovementType

    def getTenor(self):
        if (self.assetName == "CETES"):
            return 28
        
    def getMaturityDate(self):
        if (self.assetName == "CETES"):
            return self.paymentDate + datetime.timedelta(days = int(self.getTenor()))

    def logObject(self):
        print (self.__dict__)
        
    