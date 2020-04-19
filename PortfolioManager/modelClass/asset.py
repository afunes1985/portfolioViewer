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
    historicalPriceSource = Column('historical_price_source', String(), nullable=False)
    #defaultCustody = None
    
    def getName(self):
        if(self.originName is not None):
            return self.originName
        else:
            return self.name
            

