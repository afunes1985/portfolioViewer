'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean

from modelClass import PersistenObject


class Asset(PersistenObject):
    __tablename__ = 'asset'
    assetType = Column('asset_type', String(), nullable=False)
    name = Column(String(), nullable=False)
    originName = Column('origin_name', String(), nullable=False)
    isSIC = Column('is_sic', Boolean(), nullable=False)
    isOnlinePrice = Column('is_online_price',Boolean(), nullable=False)
    priceSource = Column('price_source', String(), nullable=False)
    movementList = relationship("Movement", back_populates="asset")
    #defaultCustody = None

