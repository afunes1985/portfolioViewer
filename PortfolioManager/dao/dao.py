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
                    WHERE ACQUISITION_DATE BETWEEN %s AND %s 
                    ORDER BY ACQUISITION_DATE'''
        returnList = DbConnector().doQuery(query, (fromDate, toDate))
        return returnList    

class DaoAssetType():

    def getAssetTypes(self):
        query = '''SELECT DISTINCT ASSET_TYPE
                    FROM ASSET'''
        resultSet = DbConnector().doQuery(query, "")
        returnList = []
        for (assetType) in resultSet:
            returnList.append(assetType[0])
        return returnList  
    
    def getAssetNames(self, assetType):
        query = """SELECT DISTINCT NAME FROM ASSET WHERE ASSET_TYPE = %s"""
        resultSet = DbConnector().doQuery(query, (assetType,))
        returnList = []
        for (assetName) in resultSet:
            returnList.append(assetName[0])
        return returnList  
        