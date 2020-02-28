'''
Created on Feb 26, 2020

@author: afunes
'''
from base.dbConnector import DBConnector
from modelClass.corporateEvent import CorporateEvent


class CorporateEventDao():

    def getCorporateEventList(self, session=None):
        if (session is None): 
            dbconnector = DBConnector()
            session = dbconnector.getNewSession()
        query = session.query(CorporateEvent)\
                .order_by(CorporateEvent.paymentDate)
        objectResult = query.all()
        return objectResult  