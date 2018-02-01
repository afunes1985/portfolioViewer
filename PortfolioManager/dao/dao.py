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
                    m.TENOR,
                    c.NAME  
                    FROM movement as m 
                        inner join asset as a on m.asset_oid = a.id 
                        inner join custody as c on c.ID = m.CUSTODY_OID
                    WHERE ACQUISITION_DATE BETWEEN %s AND %s 
                    ORDER BY m.asset_oid,ACQUISITION_DATE'''
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
                    ORDER BY ACQUISITION_DATE desc'''
        resultSet = DbConnector().doQuery(query, (fromDate, toDate, assetName))
        return resultSet  
    
    def insertMovement(self, movement):
        insertSentence = """insert movement(asset_oid, buy_sell,acquisition_date, quantity, 
                                    price, rate, gross_amount, net_amount, 
                                    commission_percentage, commission_amount, commission_iva_amount, tenor, custody_oid) 
                       values (%s,%s,%s,%s,
                               %s,%s,%s,%s,
                               %s,%s,%s,%s,%s)"""
        DbConnector().doInsert(insertSentence, (movement.assetOID, movement.buySell, movement.acquisitionDate, movement.quantity,
                                                movement.price, movement.rate, movement.grossAmount, movement.netAmount,
                                                movement.commissionPercentage, movement.commissionAmount, movement.commissionVATAmount, movement.tenor, movement.custody))

class DaoAsset():
    def getAssetTypes(self):
        query = '''SELECT DISTINCT ASSET_TYPE
                    FROM ASSET'''
        resultSet = DbConnector().doQuery(query, "")
        returnList = []
        for (row) in resultSet:
            returnList.append(row[0])
        return returnList  
    
    def getAssetNames(self, assetType):
        query = """SELECT ID, NAME FROM ASSET WHERE ASSET_TYPE = %s"""
        resultSet = DbConnector().doQuery(query, (assetType,))
        return resultSet  
    
    def getAssetList(self):
        query = '''SELECT ID, ASSET_TYPE, NAME, ORIGIN_NAME, IS_SIC, IS_ONLINE_PRICE, PRICE_SOURCE, DEFAULT_CUSTODY_OID FROM ASSET'''
        resultSet = DbConnector().doQuery(query, "")
        return resultSet  
        
class DaoCustody():
    def getCustodyList(self):
        query = "SELECT ID, NAME FROM CUSTODY"
        resultSet = DbConnector().doQuery(query, "")
        return resultSet  
    
    def getDefaultCustody(self, name):
        query = "SELECT C.ID FROM CUSTODY AS C INNER JOIN ASSET AS A ON A.DEFAULT_CUSTODY_OID = C.ID WHERE A.NAME = %s"
        resultSet = DbConnector().doQuery(query,(name,))
        return resultSet  
    
class DaoCorporateEvent():
    @staticmethod
    def getCorporateEventTypeList():
        query = """SELECT ID, NAME FROM CORPORATE_EVENT_TYPE"""
        resultSet = DbConnector().doQuery(query, "")
        return resultSet  

    @staticmethod
    def getCorporateEventList():
        query = """SELECT ce.id, CE.CUSTODY_OID, CE.CORPORATE_EVENT_TYPE_OID, CE.ASSET_OID,  CE.PAYMENT_DATE, CE.GROSS_AMOUNT, CE.NET_AMOUNT, COMMENT
                    FROM CORPORATE_EVENT CE                    
                order by CE.PAYMENT_DATE desc"""
        resultSet = DbConnector().doQuery(query, "")
        return resultSet  
   
    @staticmethod
    def insert(corporateEvent):
        insertSentence = """insert corporate_event(corporate_event_type_oid, asset_oid, payment_date, gross_amount, custody_oid, net_amount, comment) 
                       values (%s,%s,%s,%s,%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (corporateEvent.corporateEventType.OID,  corporateEvent.asset.OID, corporateEvent.paymentDate, corporateEvent.grossAmount, corporateEvent.custody.OID, corporateEvent.netAmount, corporateEvent.comment))

class DaoTax():
    @staticmethod
    def insert(tax):
        insertSentence = """insert tax(origin_type, origin_oid, tax_amount) 
                       values (%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (tax.originType,  tax.originOID, tax.taxAmount))

class DaoPrice():
    @staticmethod
    def getLastPrice(assetName):
        query = """SELECT p.last_price, p.date_
                    FROM PRICE p
                    INNER JOIN ASSET A ON P.ASSET_OID = A.ID
                WHERE A.NAME = %s                  
                order by p.DATE_ desc"""
        resultSet = DbConnector().doQuery(query, (assetName,))
        return resultSet 

class DaoCashMovement():
    @staticmethod
    def getCashMovement():
        query = """SELECT ID, amount, in_out, custody_oid, movement_date, comment
                        FROM cash_movement                 
                order by movement_date desc"""
        resultSet = DbConnector().doQuery(query, "")
        return resultSet   
    
    @staticmethod
    def insert(cashMovement):
        insertSentence = """insert cash_movement(amount, in_out, custody_oid, movement_date, comment) 
                       values (%s,%s,%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (cashMovement.amount, cashMovement.inOut, cashMovement.custody.OID, cashMovement.movementDate, cashMovement.comment))      
    