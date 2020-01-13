'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.sql.expression import and_

from base.dbConnector import DBConnector
from modelClass.movement import Movement


class MovementDao():

    def getMovementsByDate(self, fromDate, toDate, session = None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(Movement)\
                .filter(and_(Movement.acquisitionDate >= fromDate, Movement.acquisitionDate <= toDate, Movement.assetOID.isnot(None)))\
                .order_by(Movement.acquisitionDate)
        objectResult = query.all()
        return objectResult        