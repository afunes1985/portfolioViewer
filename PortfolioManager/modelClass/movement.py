'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer, Numeric

from modelClass import PersistenObject


class Movement(PersistenObject):
    __tablename__ = 'movement'    
    assetOID = Column("asset_oid", Integer, ForeignKey('asset.ID'))
    asset = relationship("Asset")
    custodyOID = Column("custody_oid", Integer, ForeignKey('custody.ID'))
    custody = relationship("Custody")
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
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    tenor = Column(Integer(), nullable=False)
    maturityDate = Column('maturity_date', DateTime, nullable=False)
    #tax = tax
