'''
Created on Jan 13, 2018

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, Integer, Numeric

from modelClass import PersistenObject


class CashMovement(PersistenObject):
    __tablename__ = 'cash_movement'
    amount = Column(Numeric(), nullable=False)
    inOut = Column('in_out', String(2), nullable=False)
    custodyOID = Column("custody_oid", Integer, ForeignKey('custody.ID'))
    custody = relationship("Custody")
    movementDate = Column('movement_date', DateTime, nullable=False)
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    assetOID = Column("asset_oid", Integer, ForeignKey('asset.ID'))
    asset = relationship("Asset")
