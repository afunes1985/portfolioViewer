'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import and_

from base.dbConnector import DBConnector
from modelClass.currency import Currency, CurrencyValue


class CurrencyDao():

    def getCurrencyValueByDate(self, currencyName, date, session=None, raiseNoResultFound=True):
        try:
            if (session is None): 
                dbconnector = DBConnector()
                session = dbconnector.getNewSession()
            query = session.query(CurrencyValue)\
                    .join(CurrencyValue.currency)\
                    .filter(and_(Currency.name == currencyName, CurrencyValue.date == date))
            objectResult = query.one()
        except NoResultFound:
            if(raiseNoResultFound):
                raise Exception("NoResultFound - " + str(currencyName) + " " + str(date))
            return None
        return objectResult  