'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from modelClass import PersistenObject

class Custody(PersistenObject):
    __tablename__ = 'custody'
    name = Column(String(), nullable=False)
    assetList = relationship("Asset", back_populates="defaultCustody")
