'''
Created on Feb 13, 2017

@author: afunes
'''
from dbConnector.dbConnector import DbConnector

class DaoMovement():
    
    @staticmethod
    def getMovementsByExternalID(externalID):
        query = '''SELECT m.external_id
                    FROM movement as m 
                    WHERE m.external_id = %s'''
        resultSet = DbConnector().doQuery(query, (externalID,))
        return resultSet

    @staticmethod
    def getMovementsByMaturityDate(maturityDate):
        query = '''SELECT m.id, m.gross_amount
                    FROM movement as m 
                        left join tax as t on t.origin_oid = m.id and t.origin_type = 'MOVEMENT'
                    WHERE m.maturity_date = %s
                        and t.id is null
                    order by gross_amount desc'''
        resultSet = DbConnector().doQuery(query, (maturityDate,))
        return resultSet

    @staticmethod
    def getMovementsByDate(assetName, fromDate, toDate):
        query = '''SELECT m.ID, 
                    m.asset_oid, 
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
                    c.ID,
                    m.MATURITY_DATE,
                    IFNULL(t.tax_amount, 0)
                    FROM movement as m 
                        inner join asset as a on m.asset_oid = a.id 
                        inner join custody as c on c.ID = m.CUSTODY_OID
                        left join tax as t on t.origin_oid = m.id and t.origin_type = 'MOVEMENT'
                    WHERE ACQUISITION_DATE BETWEEN %s AND %s 
                        AND (a.NAME = %s or %s is null)
                    ORDER BY m.asset_oid,ACQUISITION_DATE'''
        resultSet = DbConnector().doQuery(query, (fromDate, toDate, assetName, assetName))
        return resultSet    
    
    @staticmethod
    def insertMovement(movement):
        insertSentence = """insert movement(asset_oid, buy_sell,acquisition_date, quantity, 
                                    price, rate, gross_amount, net_amount, 
                                    commission_percentage, commission_amount, commission_iva_amount, tenor, 
                                    maturity_date, custody_oid, external_id, comment) 
                       values (%s,%s,%s,%s,
                               %s,%s,%s,%s,
                               %s,%s,%s,%s,
                               %s,%s,%s,%s)"""
        DbConnector().doInsert(insertSentence, (movement.asset.OID, movement.buySell, movement.acquisitionDate, movement.quantity,
                                                movement.price, movement.rate, movement.grossAmount, movement.netAmount,
                                                movement.commissionPercentage, movement.commissionAmount, movement.commissionVATAmount, movement.tenor, 
                                                movement.maturityDate, movement.custodyOID, movement.externalID, movement.comment))

    
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
    
    def getAssetByName(self, assetName):
        query = """SELECT ID, NAME FROM ASSET WHERE NAME = %s"""
        resultSet = DbConnector().doQuery(query, (assetName,))
        return resultSet 
        
class DaoCustody():
    
    def getCustodyList(self):
        query = "SELECT ID, NAME FROM CUSTODY"
        resultSet = DbConnector().doQuery(query, "")
        return resultSet  
    
    def getCustodyNameList(self):
        query = "SELECT NAME FROM CUSTODY"
        resultSet = DbConnector().doQuery(query, "")
        returnList = []
        for (row) in resultSet:
            returnList.append(row[0])
        returnList.append('ALL')
        return sorted(returnList)  
    
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
        return DbConnector().doInsert(insertSentence, (corporateEvent.corporateEventType.OID,  corporateEvent.assetOID, corporateEvent.paymentDate, corporateEvent.grossAmount, corporateEvent.custody.OID, corporateEvent.netAmount, corporateEvent.comment))

class DaoTax():
    @staticmethod
    def insert(tax):
        insertSentence = """insert tax(origin_type, origin_oid, tax_amount, external_id) 
                       values (%s,%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (tax.originType,  tax.originOID, tax.taxAmount, tax.externalID))
    
    @staticmethod
    def getTaxByExternalID(externalID):
        query = '''SELECT t.external_id  
                    FROM tax as t 
                    WHERE t.external_id = %s'''
        resultSet = DbConnector().doQuery(query, (externalID,))
        return resultSet

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
    @staticmethod
    def insert(price):
        insertSentence = """insert price(asset_oid, last_price, date_) 
                       values (%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (price.assetOID, price.lastPrice, price.date))
    @staticmethod
    def getPriceByDate(assetName, date):
        query = """SELECT p.last_price, p.date_
                    FROM PRICE p
                    INNER JOIN ASSET A ON P.ASSET_OID = A.ID
                WHERE ((A.NAME = %s and a.ORIGIN_NAME IS NULL) 
                        OR (A.ORIGIN_NAME = %s))
                    AND p.DATE_ = %s"""
        resultSet = DbConnector().doQuery(query, (assetName,assetName, date))
        return resultSet 
    

class DaoCashMovement():
    @staticmethod
    def getCashMovement(fromDate, toDate):
        query = """SELECT ID, amount, in_out, custody_oid, movement_date, comment
                        FROM cash_movement 
                    WHERE movement_date BETWEEN %s AND %s  
                    order by movement_date desc"""
        resultSet = DbConnector().doQuery(query, (fromDate, toDate))
        return resultSet   
    
    @staticmethod
    def insert(cashMovement):
        insertSentence = """insert cash_movement(amount, in_out, custody_oid, movement_date, comment, external_id) 
                       values (%s,%s,%s,%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (cashMovement.amount, cashMovement.inOut, cashMovement.custody.OID, cashMovement.movementDate, cashMovement.comment, cashMovement.externalID))    
    
    @staticmethod
    def getCashMovementsByExternalID(externalID):
        query = '''SELECT cm.external_id  
                    FROM cash_movement as cm 
                    WHERE cm.external_id = %s'''
        resultSet = DbConnector().doQuery(query, (externalID,))
        return resultSet
    
class DaoReportMovement():  
    @staticmethod
    def getMovements(fromDate, toDate, movementType, assetName, custodyName):
        paramns = {'fromdate' : fromDate,
                   'toDate': toDate,
                   'movementType': movementType,
                   'assetName' : assetName,
                   'custodyName': custodyName}
        query = '''SELECT 
                    m.ID as EVENT_ID,
                    'MOVEMENT' as EVENT_TYPE,
                    'TRX' AS EVENT_SUB_TYPE,
                    BUY_SELL as EVENT_DIRECTION,
                    a.name as ASSET_NAME,
                    ACQUISITION_DATE AS EVENT_DATE,
                    QUANTITY AS QUANTITY,
                    PRICE AS PRICE,
                    RATE AS RATE,
                    GROSS_AMOUNT AS GROSS_AMOUNT,
                    NET_AMOUNT AS NET_AMOUNT,
                    COMMISSION_PERCENTAGE AS COMMISSION_PERCENTAGE,
                    COMMISSION_AMOUNT AS COMMISSION_AMOUNT,
                    COMMISSION_IVA_AMOUNT AS COMMISSION_IVA_AMOUNT,
                    TENOR AS TENOR,
                    c.name AS CUSTODY_NAME,
                    t.ID AS TAX_ID,
                    t.TAX_AMOUNT as TAX_AMOUNT,
                    COMMENT AS COMMENT,
                    m.EXTERNAL_ID AS EXTERNAL_ID
                FROM movement m
                    left join asset as a on m.asset_oid = a.id 
                    left join custody as c on c.id = m.custody_oid 
                    left join tax as t on t.origin_oid = m.id and t.origin_type = 'MOVEMENT'
                WHERE ACQUISITION_DATE BETWEEN %(fromdate)s AND %(toDate)s 
                    AND (a.asset_type = %(movementType)s or %(movementType)s = 'ALL') 
                    AND (a.name = %(assetName)s or %(assetName)s = 'ALL')
                    AND (c.name = %(custodyName)s or %(custodyName)s = 'ALL')
                UNION ALL
                SELECT 
                    ce.ID as EVENT_ID,
                    'CORP EVENT' as EVENT_TYPE,
                    cet.name AS EVENT_SUB_TYPE,
                    null as EVENT_DIRECTION,
                    a.name as ASSET_NAME,
                    payment_date AS EVENT_DATE,
                    NULL AS QUANTITY,
                    NULL AS PRICE,
                    NULL AS RATE,
                    gross_amount AS GROSS_AMOUNT,
                    NET_AMOUNT AS NET_AMOUNT,
                    0 AS COMMISSION_PERCENTAGE,
                    0 AS COMMISSION_AMOUNT,
                    0 AS COMMISSION_IVA_AMOUNT,
                    NULL AS TENOR,
                    c.name AS CUSTODY_NAME,
                    t.ID AS TAX_ID,
                    t.TAX_AMOUNT as TAX_AMOUNT,
                    COMMENT AS COMMENT,
                    ce.EXTERNAL_ID AS EXTERNAL_ID
                FROM corporate_event ce
                    left join asset as a on ce.asset_oid = a.id
                    left join custody as c on c.id = ce.custody_oid 
                    left join corporate_event_type as cet on cet.id = ce.corporate_event_type_oid
                    left join tax as t on t.origin_oid = ce.id and t.origin_type = 'CORPORATE_EVENT'
                WHERE payment_date BETWEEN %(fromdate)s AND %(toDate)s  
                    AND (a.asset_type = %(movementType)s or %(movementType)s = 'ALL') 
                    AND (a.name = %(assetName)s or %(assetName)s = 'ALL')
                    AND (c.name = %(custodyName)s or %(custodyName)s = 'ALL')
                UNION ALL
                SELECT 
                    cm.ID as EVENT_ID,
                    'MOVEMENT' as EVENT_TYPE,
                    'CASH' AS EVENT_SUB_TYPE,
                    in_out as EVENT_DIRECTION,
                    'MXN' as ASSET_NAME,
                    movement_date AS EVENT_DATE,
                    NULL AS QUANTITY,
                    NULL AS PRICE,
                    NULL AS RATE,
                    amount AS GROSS_AMOUNT,
                    amount AS NET_AMOUNT,
                    0 AS COMMISSION_PERCENTAGE,
                    0 AS COMMISSION_AMOUNT,
                    0 AS COMMISSION_IVA_AMOUNT,
                    NULL AS TENOR,
                    c.name AS CUSTODY_NAME,
                    null AS TAX_ID,
                    null as TAX_AMOUNT,
                    COMMENT AS COMMENT,
                    EXTERNAL_ID AS EXTERNAL_ID
                FROM cash_movement CM
                    left join custody as c on c.id = CM.custody_oid
                WHERE movement_date BETWEEN %(fromdate)s AND %(toDate)s  
                    AND ('CASH' = %(movementType)s or %(movementType)s = 'ALL')
                    AND ('CASH' = %(assetName)s or %(assetName)s = 'ALL')
                    AND (c.name = %(custodyName)s or %(custodyName)s = 'ALL') '''
        resultSet = DbConnector().doQuery(query, paramns)
        return resultSet  
        
    @staticmethod
    def getMovementType():
        query = '''SELECT DISTINCT ASSET_TYPE
                FROM ASSET'''
        resultSet = DbConnector().doQuery(query, "")
        returnList = []
        for (row) in resultSet:
            returnList.append(row[0])
        returnList.append('CASH')
        returnList.append('ALL')
        return sorted(returnList)   
    
    @staticmethod
    def getAssetNames():
        query = """SELECT DISTINCT NAME FROM ASSET"""
        resultSet = DbConnector().doQuery(query, "")
        returnList = []
        for (row) in resultSet:
            returnList.append(row[0])
        returnList.append('MXN')
        returnList.append('ALL')
        return sorted(returnList)
    
class DaoCurrency():
    @staticmethod
    def insertCurrencyValue(currencyValue):
        insertSentence = """insert currency_value(currency_id, date_, value) 
                       values (%s,%s,%s)"""
        return DbConnector().doInsert(insertSentence, (currencyValue.currencyOID,currencyValue.date,currencyValue.value))
    @staticmethod
    def getCurrencyValueByDate(currencyName, date):
        query = """SELECT cv.value, cv.date_
                    FROM CURRENCY_VALUE cv
                    INNER JOIN CURRENCY C ON C.ID = CV.CURRENCY_ID
                WHERE C.NAME = %s
                    AND cv.DATE_ = %s"""
        resultSet = DbConnector().doQuery(query, (currencyName, date))
        return resultSet 
    
    @staticmethod
    def getCurrencyByName(currencyName):
        query = """SELECT c.id
                    FROM CURRENCY C
                    WHERE C.NAME = %s"""
        resultSet = DbConnector().doQuery(query, (currencyName,))
        return resultSet 