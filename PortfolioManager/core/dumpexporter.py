'''
Created on 22 ago. 2018

@author: afunes
'''
import os
import time


class DumpExporter():
    
    @staticmethod
    def exportDump(dbHost, dbUser, dbUserPass, dbName ):
        fileName = time.strftime("%Y%m%d") + "_" + "dump_"+ dbName 
        BACKUP_PATH = 'C:\\Users\\afunes\\iCloudDrive\\PortfolioViewer\\dumps\\'
         
        dumpcmd = """"C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysqldump.exe\"""" + " -h " + dbHost + " -u " + dbUser + " -p" + dbUserPass + " " + dbName +  " > " + BACKUP_PATH + fileName + ".sql"
        os.system(dumpcmd)
        print(dumpcmd)
        print ("Backup script completed " + fileName)


DumpExporter.exportDump('localhost', 'root', 'root', 'portfolio')
DumpExporter.exportDump('localhost', 'root', 'root', 'fundamenalanalytics')