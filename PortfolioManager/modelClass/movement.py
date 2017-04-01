'''
Created on Mar 18, 2017

@author: afunes
'''
class Movement():
    buySell = ''
    assetOID = 0
    acquisitionDate = ''
    quantity = 0
    grossAmount = 0
    netAmount = 0
    commissionPercentage = 0
    commissionAmount = 0
    commissionVATAmount = 0
    rate = 0
    price = 0
    tenor = 0
    def constructMovementByType(self, assetType):
        if assetType == 'EQUITY':
            return EquityMovement()
        elif assetType == 'FUND':
            return FundMovement()
        elif assetType == 'BOND':
            return BondMovement()

class BondMovement(Movement):
    rate = 0

class EquityMovement(Movement):
    price = 0

class FundMovement(Movement):
    price = 0

class Asset():
    OID = 0
    assetType = ''
    name = ''
    isSIC = 0
    isOnlinePrice = 0