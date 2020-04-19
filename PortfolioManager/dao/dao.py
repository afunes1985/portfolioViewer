'''
Created on 20 ago. 2018

@author: afunes
'''
from sqlalchemy.orm.exc import NoResultFound

from base.dbConnector import DBConnector

class GenericDao():
    
    def getFirstResult(self, objectClazz, condition, session=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
    
        objectResult = session.query(objectClazz)\
        .filter(condition)\
        .first()
        return objectResult
    
    def getOneResult(self, objectClazz, condition=(1 == 1), session=None, raiseNoResultFound=True):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        try:
            objectResult = session.query(objectClazz)\
            .filter(condition)\
            .one()
        except NoResultFound as e:
            if(raiseNoResultFound):
                raise e
            return None
        return objectResult
    
    def getAllResult(self, objectClazz, condition=(1 == 1), session=None, limit=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        objectResult = session.query(objectClazz)\
        .filter(condition)\
        .limit(limit)\
        .all()
        return objectResult
