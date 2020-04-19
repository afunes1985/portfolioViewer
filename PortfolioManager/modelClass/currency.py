'''
Created on 18 mar. 2018

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, String, Integer, Numeric

from modelClass import PersistenObject


class Currency(PersistenObject):
    __tablename__ = 'currency'
    name = Column(String(30), nullable=False)
    source = Column(String(30), nullable=False)
    currencyValueList = relationship("CurrencyValue", back_populates="currency")

class CurrencyValue(PersistenObject):
    __tablename__ = 'currency_value'
    currencyOID = Column("currency_id", Integer, ForeignKey('currency.ID'))
    currency = relationship("Currency", back_populates="currencyValueList")
    date = Column("date_", DateTime, nullable=False)
    value = Column(Numeric(), nullable=False)