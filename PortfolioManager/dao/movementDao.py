'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.sql.expression import and_, union

from base.dbConnector import DBConnector
from modelClass.asset import Asset
from modelClass.movement import Movement
from modelClass.cashMovement import CashMovement


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
    
    def getMovementsForReport(self, fromDate, toDate, session = None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        queryMov = session.query(Movement)\
                .join(Movement.asset)\
                .filter(and_(Movement.acquisitionDate >= fromDate, Movement.acquisitionDate <= toDate, Movement.assetOID.isnot(None)))\
                .with_entities(Asset.name, Movement.buySell, Movement.acquisitionDate, Movement.quantity, Movement.price, Movement.grossAmount, Movement.netAmount, Movement.commissionPercentage, Movement.commissionAmount, Movement.commissionVATAmount)\
                .order_by(Movement.acquisitionDate)
#         queryCashMov = session.query(CashMovement)\
#                 .join(CashMovement.asset)\
#                 .filter(and_(Movement.acquisitionDate >= fromDate, Movement.acquisitionDate <= toDate, Movement.assetOID.isnot(None)))\
#                 .with_entities(Asset.name, Movement.buySell, Movement.acquisitionDate, Movement.quantity, Movement.price, Movement.grossAmount, Movement.commissionPercentage, Movement.commissionAmount, Movement.commissionVATAmount)\
#                 .order_by(Movement.acquisitionDate)
        
        objectResult = queryMov.all()
        return objectResult   