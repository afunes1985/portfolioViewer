'''
Created on Apr 30, 2020

@author: afunes
'''
from base.dbConnector import DBConnector
from modelClass.asset import Asset
from modelClass.custody import Custody


class AssetDao():
    
    def getAssetTypeList(self, session=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(Asset)\
            .with_entities(Asset.assetType.distinct())
        objectResult = query.all()
        return objectResult 
    
    def getAssetList(self, assetType, session=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(Asset)\
                .filter(Asset.assetType == assetType)
        objectResult = query.all()
        return objectResult   

    def getCustodyList(self, session=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(Custody)
        objectResult = query.all()
        return objectResult  
    
    def getCustodyByAssetID(self, assetID, session=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(Custody)\
                .join(Custody.assetList)\
                .filter(Asset.ID == assetID)
        objectResult = query.one()
        return objectResult   

        