'''
Created on 29 ene. 2018

@author: afunes
'''
class ImportMovementLO():
    
    def setMovementList(self, movementList):
        self.movementList = movementList
        
    def getMovementList(self, fromDate, toDate):
        return self.movementList
    
    def setFromDate(self, fromDate):
        self.fromDate = fromDate
    
    def setToDate(self, toDate):
        self.toDate = toDate
        
    def setCustodyName(self, custodyName):
        self.custodyName = custodyName
        
        
        
