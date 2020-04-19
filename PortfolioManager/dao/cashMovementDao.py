'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.sql.expression import and_

from base.dbConnector import DBConnector
from modelClass.cashMovement import CashMovement

class CashMovementDao():

    def getCashMovementsByDate(self, fromDate, toDate, session = None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(CashMovement)\
                .filter(and_(CashMovement.movementDate >= fromDate, CashMovement.movementDate <= toDate))\
                .order_by(CashMovement.movementDate)
        objectResult = query.all()
        return objectResult        