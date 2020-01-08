'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Float, String

from modelClass import Base


class CorporateEvent(Base):
    __tablename__ = 'corporate_event'
    #asset = None
    paymentDate = Column('payment_date', DateTime, nullable=False)
    grossAmount = Column('gross_amount', Float(), nullable=False)
    #custody = None
    #corporateEventType = None
    netAmount = Column('net_amount', Float(), nullable=False)
    comment = Column(String(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)
    #tax = None
        
class Custody(Base):
    name = Column(String(), nullable=False)
    
class CorporateEventType(Base):
    name = Column(String(), nullable=False)
