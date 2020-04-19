'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.elements import and_
from sqlalchemy.sql.expression import text

from base.dbConnector import DBConnector
from modelClass.asset import Asset
from modelClass.price import Price


class PriceDao():

    def getPriceByDate(self, assetName, date,session = None):
        try:
            if (session is None): 
                dbconnector = DBConnector()
                session = dbconnector.getNewSession()
            query = session.query(Price)\
                    .join(Price.asset)\
                    .filter(and_(Asset.name == assetName, Price.date == date))
            objectResult = query.one()
        except NoResultFound as e:
            raise Exception("NoResultFound - " + str(assetName) + " " + str(date))
        return objectResult    
    
    def getLastPrice(self, assetName, session = None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        params = { 'assetName' : assetName}
        query = text("""SELECT p.last_price, p.date_
                FROM PRICE p
                INNER JOIN ASSET A ON P.ASSET_OID = A.ID
            WHERE A.NAME = :assetName                  
            order by p.DATE_ desc""")
        resulSet = session.execute(query, params)
        for row in resulSet:
            return row
