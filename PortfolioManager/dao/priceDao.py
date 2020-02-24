'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.sql.expression import text

from base.dbConnector import DBConnector

class PriceDao():

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
        return session.execute(query, params)