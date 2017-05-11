'''
Created on Mar 18, 2017

@author: afunes
'''
class Movement():
    OID = None
    assetName = None
    buySell = ''
    assetOID = None
    asset = None
    acquisitionDate = None
    quantity = 0
    grossAmount = 0
    netAmount = 0
    commissionPercentage = 0
    commissionAmount = 0
    commissionVATAmount = 0
    rate = 0
    price = 0
    tenor = 0
    def __init__(self, movementRow):
        self.OID = movementRow[0]
        self.assetName = movementRow[1]
        self.buySell = movementRow[2]
        self.acquisitionDate = movementRow[3]
        self.quantity = movementRow[4]
        self.price = movementRow[5]
        self.grossAmount = movementRow[6]
        self.netAmount = movementRow[7]
        self.commissionPercentage = movementRow[8]
        self.commissionAmount = movementRow[9]
        self.commissionVATAmount = movementRow[10]
        
    def constructMovementByType(self, assetType):
        if assetType == 'EQUITY':
            return EquityMovement()
        elif assetType == 'FUND':
            return FundMovement()
        elif assetType == 'BOND':
            return BondMovement()

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
    def __init__(self, assetRow):
            self.OID = assetRow[0]
            self.assetType = assetRow[1]
            self.name = assetRow[2]
            self.originName = assetRow[3]
            self.isSIC = assetRow[4]
            self.isOnlinePrice = assetRow[5]

