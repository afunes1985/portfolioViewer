'''
Created on Mar 18, 2017

@author: afunes
'''
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean


class Asset():
    assetType = Column('asset_type', String(), nullable=False)
    name = Column(String(), nullable=False)
    originName = Column(String(), nullable=False)
    isSIC = Column(Boolean(), nullable=False)
    isOnlinePrice = Column(Boolean(), nullable=False)
    priceSource = Column(String(), nullable=False)
    #defaultCustody = None

