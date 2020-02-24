'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Float, Integer, Numeric

from modelClass import PersistenObject


class Movement(PersistenObject):
    __tablename__ = 'movement'    
    assetOID = Column("asset_oid", Integer, ForeignKey('asset.ID'))
    asset = relationship("Asset", back_populates="movementList")
    custodyOID = Column("custody_oid", Integer, ForeignKey('custody.ID'))
    custody = relationship("Custody", back_populates="movementList")
    buySell = Column('buy_sell', String(), nullable=False)
    acquisitionDate = Column('acquisition_date', DateTime, nullable=False)
    quantity = Column(Integer(), nullable=False)
    price = Column(Numeric(), nullable=False)
    rate = Column(Numeric(), nullable=False)
    grossAmount = Column('gross_amount',Numeric(), nullable=False)
    netAmount = Column('net_amount', Numeric(), nullable=False)
    commissionPercentage = Column('commission_percentage', Numeric(), nullable=False)
    commissionAmount = Column('commission_amount', Numeric(), nullable=False)
    commissionVATAmount = Column('commission_iva_amount', Numeric(), nullable=False)
    #custody = mainCache.custodyDictOID[custodyOID]
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    tenor = Column(Integer(), nullable=False)
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

