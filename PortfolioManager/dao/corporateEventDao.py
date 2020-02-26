'''
Created on Feb 26, 2020

@author: afunes
'''
class CorporateEventDao():

    def getCorporateEventList(self):
            query = """SELECT ce.id, CE.CUSTODY_OID, CE.CORPORATE_EVENT_TYPE_OID, CE.ASSET_OID,  CE.PAYMENT_DATE, CE.GROSS_AMOUNT, CE.NET_AMOUNT, COMMENT, CE.EXTERNAL_ID
                        FROM CORPORATE_EVENT CE                    
                    order by CE.PAYMENT_DATE desc"""
            resultSet = DbConnector().doQuery(query, "")
            return resultSet  