'''
Created on 21 nov. 2017

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, String

from modelClass import PersistenObject


class Tax(PersistenObject):
    __tablename__ = 'tax'
    
    #originType = originType
    #originOID = originOID
    taxAmount = Column(Float(), nullable=False)
    externalID = Column('external_id', String(), nullable=False)