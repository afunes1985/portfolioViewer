'''
Created on 18 mar. 2018

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, String, Integer, Numeric

from modelClass import PersistenObject


class ExchangeRate(PersistenObject):
    __tablename__ = 'currency'
    name = Column(String(30), nullable=False)
    source = Column(String(30), nullable=False)
    exchangeRateValueList = relationship("ExchangeRateValue", back_populates="exchangeRate")

class ExchangeRateValue(PersistenObject):
    __tablename__ = 'currency_value'
    exchangeRateOID = Column("currency_id", Integer, ForeignKey('currency.ID'))
    exchangeRate = relationship("ExchangeRate", back_populates="exchangeRateValueList")
    date = Column("date_", DateTime, nullable=False)
    value = Column(Numeric(), nullable=False)