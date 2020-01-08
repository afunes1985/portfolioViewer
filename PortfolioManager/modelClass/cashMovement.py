'''
Created on Jan 13, 2018

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, String, DateTime

from modelClass import Base


class CashMovement(Base):
    __tablename__ = 'cash_movement'
            
    amount = Column(Float(), nullable=False)
    inOut = Column('in_out', String(2), nullable=False)
    #custody_oid = mainCache.custodyDictOID[custodyOID]
    movementDate = Column('movement_date', DateTime, nullable=False)
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    #asset_oid = mainCache.assetDictOID.get(assetOID,None)
