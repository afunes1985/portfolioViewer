'''
Created on Mar 18, 2017

@author: afunes
'''

class Movement():
        
    def __init__(self, movementRow):
        if(movementRow is not None):
            self.setAttr(movementRow[0], movementRow[1], movementRow[2], movementRow[3], 
                         movementRow[4], movementRow[5], movementRow[6], movementRow[7], 
                         movementRow[8], movementRow[9], movementRow[10], movementRow[11], 
                         None, None, None, None)
    
    def setAttr(self, OID, assetOID, buySell, acquisitionDate, 
                    quantity, price, rate, grossAmount, 
                    netAmount, commissionPercentage, commissionAmount, commissionVATAmount, 
                    externalID, custodyOID, comment, tenor):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        self.OID = OID
        self.asset = mainCache.assetDictOID[assetOID]
        self.buySell = buySell
        self.acquisitionDate = acquisitionDate
        self.quantity = quantity
        self.price = price
        self.rate = rate
        self.grossAmount = grossAmount
        self.netAmount = netAmount
        self.commissionPercentage = commissionPercentage
        self.commissionAmount = commissionAmount
        self.commissionVATAmount = commissionVATAmount
        self.externalID = externalID
        self.custodyOID = custodyOID
        self.comment = comment
        self.tenor = tenor
    
    @staticmethod 
    def constructMovementByType(assetType):
        if assetType == 'EQUITY':
            return EquityMovement(None)
        elif assetType == 'FUND':
            return FundMovement(None)
        elif assetType == 'BOND':
            return BondMovement(None)

    def getAcquisitionDate(self):
        return self.acquisitionDate.strftime("%Y-%m-%d")
    
class BondMovement(Movement):
    rate = 0

class EquityMovement(Movement):
    price = 0

class FundMovement(Movement):
    price = 0

class Asset():
    OID = 0
    assetType = None
    name = None
    originName = None
    isSIC = 0
    isOnlinePrice = 0
    priceSource = None
    defaultCustody = None
    def __init__(self, assetRow):
        from core.cache import Singleton, MainCache
        mainCache = Singleton(MainCache)
        self.OID = assetRow[0]
        self.assetType = assetRow[1]
        self.name = assetRow[2]
        self.originName = assetRow[3]
        self.isSIC = assetRow[4]
        self.isOnlinePrice = assetRow[5]
        self.priceSource = assetRow[6]
        self.defaultCustody = mainCache.custodyDictOID[assetRow[7]]

