'''
Created on Feb 13, 2017

@author: afunes
'''
from dbConnector.DbConnector import DbConnector

class DaoMovement():

    def getMovementsByDate(self, fromDate, toDate):
        query = '''SELECT m.ID, 
                    a.asset_type, 
                    a.name, 
                    m.buy_sell, 
                    m.ACQUISITION_DATE, 
                    m.quantity, 
                    m.price,
                    m.rate, 
                    m.GROSS_AMOUNT, 
                    m.NET_AMOUNT, 
                    m.COMMISSION_PERCENTAGE, 
                    m.COMMISSION_AMOUNT, 
                    m.COMMISSION_IVA_AMOUNT, 
                    a.IS_SIC  
                    FROM movement as m 
                        inner join asset as a on m.asset_oid = a.id  
                    WHERE ACQUISITION_DATE BETWEEN %s AND %s ORDER BY ACQUISITION_DATE'''
        returnList = DbConnector().doQuery(query, (fromDate, toDate))
        return returnList    
        