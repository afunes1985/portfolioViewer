'''
Created on 22 ago. 2018

@author: afunes
'''
import os
import time
fileName = "Dump" + time.strftime("%Y%m%d")
 
DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = 'root'
DB_NAME = 'portfolio'
BACKUP_PATH = 'C:\\Users\\afunes\\iCloudDrive\\PortfolioViewer\\dumps\\'
 
dumpcmd = """"C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysqldump.exe\"""" + " -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME +  " > " + BACKUP_PATH + fileName + ".sql"
os.system(dumpcmd)
print(dumpcmd)
print ("Backup script completed")
