'''
Created on Jan 8, 2020

@author: afunes
'''
from dao.dao import DaoMovement

class MovementEngine():
    
    def getMovementsByDate(self, assetName, fromDate, toDate):
        return DaoMovement().getMovementsByDate(assetName, fromDate, toDate)