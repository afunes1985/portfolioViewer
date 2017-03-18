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
    commissionIVAAmount = 0

class BondMovement(Movement):
    rate = 0

class EquityMovement(Movement):
    price = 0

class FundMovement(Movement):
    price = 0