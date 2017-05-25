'''
Created on Feb 13, 2017

@author: afunes
'''
from dbConnector.dbConnector import DbConnector

class DaoMovement():

    @staticmethod
    def getMovementsByDate(fromDate, toDate):
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
                    m.TENOR  
                    FROM movement as m 
                        inner join asset as a on m.asset_oid = a.id  
                    WHERE ACQUISITION_DATE BETWEEN %s AND %s 
                        AND (TENOR is null OR ADDDATE(ACQUISITION_DATE,TENOR) > curdate())
                    ORDER BY ACQUISITION_DATE'''
        resultSet = DbConnector().doQuery(query, (fromDate, toDate))
        return resultSet    
    
    @staticmethod
    def getMovementsByAsset(assetName, fromDate, toDate):
        query = '''SELECT m.ID, 
                    a.name, 
                    m.buy_sell, 
                    m.ACQUISITION_DATE, 
                    m.quantity, 
                    m.price,
                    m.GROSS_AMOUNT, 
                    m.NET_AMOUNT, 
                    m.COMMISSION_PERCENTAGE, 
                    m.COMMISSION_AMOUNT, 
                    m.COMMISSION_IVA_AMOUNT, 
                    m.TENOR  
                    FROM movement as m 
                        inner join asset as a on m.asset_oid = a.id  
                    WHERE ACQUISITION_DATE BETWEEN %s AND %s 
                        AND a.NAME = %s
                    ORDER BY ACQUISITION_DATE'''
        resultSet = DbConnector().doQuery(query, (fromDate, toDate, assetName))
        return resultSet  
    
    def insertMovement(self, movement):
        insertSentence = """insert movement(asset_oid, buy_sell,acquisition_date, quantity, 
                                    price, rate, gross_amount, net_amount, 
                                    commission_percentage, commission_amount, commission_iva_amount, tenor) 
                       values (%s,%s,%s,%s,
                               %s,%s,%s,%s,
                               %s,%s,%s,%s)"""
        DbConnector().doInsert(insertSentence, (movement.assetOID, movement.buySell, movement.acquisitionDate, movement.quantity,
                                                movement.price, movement.rate, movement.grossAmount, movement.netAmount,
                                                movement.commissionPercentage, movement.commissionAmount, movement.commissionVATAmount, movement.tenor))

class DaoAsset():

    def getAssetTypes(self):
        query = '''SELECT DISTINCT ASSET_TYPE
                    FROM ASSET'''
        resultSet = DbConnector().doQuery(query, "")
        returnList = []
        for (assetType) in resultSet:
            returnList.append(assetType[0])
        return returnList  
    
    def getAssetNames(self, assetType):
        query = """SELECT ID, NAME FROM ASSET WHERE ASSET_TYPE = %s"""
        resultSet = DbConnector().doQuery(query, (assetType,))
        return resultSet  
    
    def getAssetList(self):
        query = '''SELECT ID, ASSET_TYPE, NAME, ORIGIN_NAME, IS_SIC, IS_ONLINE_PRICE FROM ASSET'''
        resultSet = DbConnector().doQuery(query, "")
        return resultSet  
        