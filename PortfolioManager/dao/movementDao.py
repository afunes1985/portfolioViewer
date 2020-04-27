'''
Created on Jan 13, 2020

@author: afunes
'''
import sqlalchemy
from sqlalchemy.sql.expression import and_, union, text

from base.dbConnector import DBConnector
from modelClass.asset import Asset
from modelClass.cashMovement import CashMovement
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
    
    def getMovementsForReport(self, fromDate, toDate, session = None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        queryMov = session.query(Movement)\
                .join(Movement.asset)\
                .filter(and_(Movement.acquisitionDate >= fromDate, Movement.acquisitionDate <= toDate, Movement.assetOID.isnot(None)))\
                .with_entities(Asset.name, Movement.buySell, Movement.acquisitionDate, Movement.quantity, Movement.price, Movement.grossAmount, Movement.netAmount, Movement.commissionPercentage, Movement.commissionAmount, Movement.commissionVATAmount)
        queryCashMov = session.query(CashMovement)\
                .join(CashMovement.asset)\
                .filter(and_(CashMovement.movementDate >= fromDate, CashMovement.movementDate <= toDate))\
                .with_entities(Asset.name, CashMovement.inOut, CashMovement.movementDate.label("acquisitionDate"),  sqlalchemy.null(), sqlalchemy.null(), sqlalchemy.null(), CashMovement.amount, sqlalchemy.null(), sqlalchemy.null(), sqlalchemy.null())
        query = queryMov.union(queryCashMov)
        print(query)
        objectResult = query.order_by(text('movement_acquisition_date')).all()
        return objectResult   