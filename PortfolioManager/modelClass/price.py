'''
Created on 17 mar. 2018

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Numeric, Integer

from modelClass import PersistenObject


class Price(PersistenObject):
    __tablename__ = 'price'
    assetOID = Column("asset_oid", Integer, ForeignKey('asset.ID'))
    asset = relationship("Asset")
    lastPrice = Column("last_price", Numeric(), nullable=False)
    date = Column("date_", DateTime, nullable=False)
