'''
Created on Jan 13, 2020

@author: afunes
'''
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import and_
from base.dbConnector import DBConnector
from modelClass.currency import ExchangeRate, ExchangeRateValue


class ExchangeRateDao():

    def getExchangeRateValueByDate(self, exchangeRateID, date, session=None, raiseNoResultFound=True):
        try:
            if (session is None): 
                dbconnector = DBConnector()
                session = dbconnector.getNewSession()
            query = session.query(ExchangeRateValue)\
                    .join(ExchangeRateValue.exchangeRate)\
                    .filter(and_(ExchangeRate.name == exchangeRateID, ExchangeRateValue.date == date))
            objectResult = query.one()
        except NoResultFound:
            if(raiseNoResultFound):
                raise Exception("NoResultFound - " + str(exchangeRateID) + " " + str(date))
            return None
        return objectResult  
    
    def addExchangeRateValue(self, value, exchangeRate, date, session):
        exchangeRateValue = ExchangeRateValue()
        exchangeRateValue.value = value
        exchangeRateValue.exchangeRate = exchangeRate
        exchangeRateValue.date = date
        session.add(exchangeRateValue)
        session.commit()
