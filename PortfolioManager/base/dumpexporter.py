'''
Created on 22 ago. 2018

@author: afunes
'''
import os
import time


class DumpExporter():
    
    def exportDump(self, dbHost, dbUser, dbUserPass, dbName ):
        fileName = time.strftime("%Y%m%d") + "_" + "dump_"+ dbName 
        BACKUP_PATH = 'C:\\Users\\afunes\\iCloudDrive\\PortfolioViewer\\dumps\\'
         
        dumpcmd = """"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe\"""" + " -h " + dbHost + " -u " + dbUser + " -p" + dbUserPass + " " + dbName +  " > " + BACKUP_PATH + fileName + ".sql"
        os.system(dumpcmd)
        print(dumpcmd)
        print ("Backup script completed " + fileName)
    
    def exportAllDump(self):
        self.exportDump('localhost', 'root', 'root', 'portfolio')
        self.exportDump('localhost', 'root', 'root', 'fundamentalanalytics')