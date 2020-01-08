'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, DateTime, Float

from modelClass import Base


class Movement(Base):
        
    #asset = mainCache.assetDictOID.get(assetOID,None)
    buySell = Column('buy_sell', String(), nullable=False)
    acquisitionDate = Column(DateTime, nullable=False)
    quantity = Column(Float(), nullable=False)
    price = Column(Float(), nullable=False)
    rate = Column(Float(), nullable=False)
    grossAmount = Column('gross_amount',Float(), nullable=False)
    netAmount = Column('net_amount', Float(), nullable=False)
    commissionPercentage = Column(Float(), nullable=False)
    commissionAmount = Column(Float(), nullable=False)
    commissionVATAmount = Column(Float(), nullable=False)
    #custody = mainCache.custodyDictOID[custodyOID]
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    tenor = Column(Float(), nullable=False)
    maturityDate = Column('maturity_date', DateTime, nullable=False)
    #tax = tax
    
#     @staticmethod 
#     def constructMovementByType(assetType):
#         if assetType == 'EQUITY':
#             return EquityMovement(None)
#         elif assetType == 'FUND':
#             return FundMovement(None)
#         elif assetType == 'BOND':
#             return BondMovement(None)
# 
#     def getAcquisitionDate(self):
#         return acquisitionDate.strftime("%Y-%m-%d")
#     
#     def getMovementType(self):
#         return Constant.CONST_MOVEMENT_TYPE
#     
#     def getMovementSubType(self):
#         return Constant.CONST_MOVEMENT_SUB_TYPE
    
# class BondMovement(Movement):
#     rate = 0
# 
# class EquityMovement(Movement):
#     price = 0
# 
# class FundMovement(Movement):
#     price = 0

