'''
Created on 17 mar. 2018

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Float, DateTime

from modelClass import PersistenObject


class Price(PersistenObject):
    __tablename__ = 'price'
    
    #assetOID = assetOID
    lastPrice = Column(Float(), nullable=False)
    date = Column(DateTime, nullable=False)
