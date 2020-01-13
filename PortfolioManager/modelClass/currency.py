'''
Created on 18 mar. 2018

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Float

from modelClass import PersistenObject


class CurrencyValue(PersistenObject):
    __tablename__ = 'currency_value'
    #currencyOID = currencyOID
    date = Column(DateTime, nullable=False)
    value = Column(Float(), nullable=False)