'''
Created on Feb 12, 2017

@author: afunes
'''
import mysql.connector
from mysql.connector import errorcode

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
        
    def doQuery(self, query, params):
        cnx = self.initConnection()
        cursor = cnx.cursor()
        cursor.execute(query,params)
        resultList = list(cursor)
        self.closeConnection(cnx);
        return resultList
    
    
    

        