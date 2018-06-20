'''
Created on Feb 12, 2017

@author: afunes
'''
from mysql.connector import errorcode
import mysql.connector
from datetime import date


class DbConnector():

    def initConnection(self):        
        try:
            config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'database': 'portfolio',
            'raise_on_warnings': True,
            }
            cnx = mysql.connector.connect(**config)
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                
    def closeConnection(self, cnx):    
        cnx.close()
    
    def doInsert(self, sentence, params):
        cnx = self.initConnection()
        cursor = cnx.cursor()
        cursor.execute(sentence,params)
        cursor.fetchone()
        lastRowID = cursor.lastrowid
        cnx.commit()
        self.closeConnection(cnx)
        return lastRowID
       
    def doDelete(self, sentence, params):
        cnx = self.initConnection()
        cursor = cnx.cursor()
        cursor.execute(sentence,params)
        cursor.fetchone()
        lastRowID = cursor.lastrowid
        cnx.commit()
        self.closeConnection(cnx)
        return lastRowID
    
    def convertParams(self, params):
        paramToReturn = []
        for index, param in enumerate(params):
            if isinstance(param, date):
                paramToReturn.append(param.toString("yyyy-M-dd"))
            else:
                paramToReturn.append(param)
        return paramToReturn

 
    def doQuery(self, query, params):
        cnx = self.initConnection()
        cursor = cnx.cursor()
        #convertedParams = self.convertParams(params)
        cursor.execute(query,params)
        resultList = list(cursor)
        self.closeConnection(cnx);
        return resultList
    
    
    

        