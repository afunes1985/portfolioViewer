'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float, String, Integer, Numeric

from modelClass import PersistenObject


class CorporateEvent(PersistenObject):
    __tablename__ = 'corporate_event'
    assetOID = Column("asset_oid", Integer, ForeignKey('asset.ID'))
    asset = relationship("Asset")
    paymentDate = Column('payment_date', DateTime, nullable=False)
    grossAmount = Column('gross_amount', Numeric(), nullable=False)
    custodyOID = Column("custody_oid", Integer, ForeignKey('custody.ID'))
    custody = relationship("Custody")
    #corporateEventType = None
    netAmount = Column('net_amount', Numeric(), nullable=False)
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    #tax = None
        
class CorporateEventType(PersistenObject):
    __tablename__ = 'corporate_event_type'
    name = Column(String(), nullable=False)
