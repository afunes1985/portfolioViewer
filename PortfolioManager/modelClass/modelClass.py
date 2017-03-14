'''
Created on Feb 19, 2017

@author: afunes
'''
import datetime
from decimal import Decimal, InvalidOperation

from PySide import QtGui
from PySide.QtGui import QTableWidget, QTableWidgetItem, QMenuBar
import requests


class Constant:
    CONST_MOVEMENT_OID = 0
    CONST_ASSET_TYPE = 1
    CONST_ASSET_NAME = 2
    CONST_MOVEMENT_BUY_SELL = 3
    CONST_MOVEMENT_ACQUISITION_DATE = 4
    CONST_MOVEMENT_QUANTITY = 5
    CONST_MOVEMENT_PRICE = 6
    CONST_MOVEMENT_RATE = 7
    CONST_MOVEMENT_GROSS_AMOUNT = 8
    CONST_ASSET_IS_SIC = 13
    
class Position():
    assetType = ''
    assetName = ''
    ppp = 0
    rate = 0
    totalQuantity = 0
    accumulatedAmount = 0
    marketPrice = 0
    isSic = 0
    movementList = []
    acquisitionDate = 0
    
    def __init__(self, assetName, movement):
        self.assetName = assetName
        self.assetType = movement[Constant.CONST_ASSET_TYPE]
        self.isSIC = movement[Constant.CONST_ASSET_IS_SIC]
        self.acquisitionDate = movement[Constant.CONST_MOVEMENT_ACQUISITION_DATE]
        if (self.assetType == 'CETES'):
            self.addMovementCetes(movement)
        else:    
            self.addMovement(movement)
        
    def addMovement(self, movement):   
        self.movementList.append(movement)
        quantity = movement[Constant.CONST_MOVEMENT_QUANTITY]
        grossAmount = movement[Constant.CONST_MOVEMENT_GROSS_AMOUNT]
        if movement[Constant.CONST_MOVEMENT_BUY_SELL] == 'BUY':
            self.totalQuantity = self.totalQuantity + abs(quantity)#quantity
            self.accumulatedAmount = self.accumulatedAmount + abs(grossAmount)#gross amount
        else:
            self.accumulatedAmount = self.accumulatedAmount - abs(quantity) * self.getPPP()
            self.totalQuantity = self.totalQuantity - abs(quantity)#quantity
        
        if self.totalQuantity == 0:        
            self.ppp = 0
            self.accumulatedAmount = 0
        else:
            self.ppp = self.accumulatedAmount / self.totalQuantity
    
    def addMovementCetes(self, movement):
        self.movementList.append(movement)
        self.totalQuantity = movement[Constant.CONST_MOVEMENT_QUANTITY]
        self.accumulatedAmount = movement[Constant.CONST_MOVEMENT_GROSS_AMOUNT]
        self.ppp = movement[Constant.CONST_MOVEMENT_PRICE]
        self.rate = movement[Constant.CONST_MOVEMENT_RATE]
        
    def getPPP(self):
        return self.ppp
    
    def getAssetName(self):
        return self.assetName
    
    def getTotalQuantity(self):
        return self.totalQuantity;
    
    def getInvestedAmount(self):
        return self.totalQuantity * self.ppp;
    
    def getElapsedDays(self):
        elapsedDays = datetime.datetime.now() - self.acquisitionDate
        return elapsedDays.days
    
    def getValuatedAmount(self):
        if (self.assetType == 'CETES'):
            return self.accumulatedAmount * (1 + (self.getElapsedDays() * (self.rate / 360)))
        else:    
            return Decimal(self.totalQuantity) * self.marketPrice
    
    def getMovementList(self):
        return self.movementList
    
    def setMarketPrice(self, marketPrice):
        try:
            self.marketPrice = Decimal(marketPrice)
        except InvalidOperation:
            self.marketPrice = 0
        
    def getMarketPrice(self):
        return self.marketPrice
    
    def getPnL(self):
        return self.getValuatedAmount() - self.getInvestedAmount()
    
class QTableWidgetItemString(QTableWidgetItem):
    def __init__(self, value):
        super(QTableWidgetItemString, self).__init__(value)
        self.setTextAlignment(0x0080) 
          
class QTableWidgetItemDecimal(QTableWidgetItem):
    def __init__(self, value):
        super(QTableWidgetItemDecimal, self).__init__(str('{0:.2f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080)        
    
class MainWindow(QtGui.QMainWindow):
    tableWidget = 0
    row = 0
    totalValuatedAmount = 0
    totalPNL = 0
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Porfolio Viewer')
        self.resize(900, 650)
        self.createMovementTable()
        self.createMenu()
        self.show()
         
    def createMovementTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(25)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels("Asset Name;Position;PPP;Market Price;Invested amount;Valuated amount;PNL".split(";"))
        #self.tableWidget.setSortingEnabled(True)  
        #self.tableWidget.sortItems(0)  
        self.setCentralWidget(self.tableWidget)     
        
    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&Movement")
        #=======================================================================
        # self.fileMenu.addAction(self.newAct)
        #=======================================================================

    def renderPositions(self, positionList):   
        self.subtotalPNL = 0
        self.subTotalValuatedAmount = 0
        
        for position in positionList:
            print('processing ' + position.getAssetName())
            #assetName
            assetNameItem = QTableWidgetItemString(position.getAssetName())
            self.tableWidget.setItem(self.row,0,assetNameItem)
            #totalQuantity
            totalQuantityItem = QTableWidgetItemDecimal(position.getTotalQuantity())
            self.tableWidget.setItem(self.row,1,totalQuantityItem)
            #PPP
            pppItem = QTableWidgetItemDecimal(position.getPPP())
            self.tableWidget.setItem(self.row,2,pppItem)
            #Market price
            result = requests.get('http://finance.yahoo.com/d/quotes.csv?s='+position.getAssetName() +'&f=l1')
            position.setMarketPrice(result.text)
            marketPriceItem = QTableWidgetItemDecimal(position.getMarketPrice())
            self.tableWidget.setItem(self.row,3,marketPriceItem)
            #Invested amount
            investedAmountItem = QTableWidgetItemDecimal(position.getInvestedAmount())
            self.tableWidget.setItem(self.row,4,investedAmountItem)
            #Valuated amount
            valuatedAmountItem = QTableWidgetItemDecimal(position.getValuatedAmount())
            self.tableWidget.setItem(self.row,5,valuatedAmountItem)
            self.subTotalValuatedAmount += position.getValuatedAmount()
            #PnL
            pnlItem = QTableWidgetItemDecimal(position.getPnL())
            self.tableWidget.setItem(self.row,6,pnlItem)
            self.subtotalPNL += position.getPnL()
            self.row +=1  
        #sub total valuated amount
        totalValuatedAmountItem = QTableWidgetItemDecimal(self.subTotalValuatedAmount)
        self.tableWidget.setItem(self.row,5,totalValuatedAmountItem)   
        #sub total PNL    
        totalPNLItem = QTableWidgetItemDecimal(self.subtotalPNL)
        self.tableWidget.setItem(self.row,6,totalPNLItem)
        self.row +=1 
        #Grand total
        self.totalValuatedAmount += self.subTotalValuatedAmount
        self.totalPNL += self.subtotalPNL
        
    def renderGrandTotal(self):
        #total valuated amount
        totalValuatedAmountItem = QTableWidgetItemDecimal(self.totalValuatedAmount)
        self.tableWidget.setItem(self.row,5,totalValuatedAmountItem)   
        #total PNL    
        totalPNLItem = QTableWidgetItemDecimal(self.totalPNL)
        self.tableWidget.setItem(self.row,6,totalPNLItem)