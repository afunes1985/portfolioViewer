'''
Created on Feb 19, 2017

@author: afunes
'''
import datetime
from decimal import Decimal, InvalidOperation

from PySide import QtGui, QtCore
from PySide.QtCore import QRect
from PySide.QtGui import QTableWidget, QTableWidgetItem, QWidget, \
    QLineEdit, QIntValidator, QLabel, QComboBox, QPushButton
import requests

from dao.dao import DaoAssetType
from modelClass.movement import EquityMovement

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
        self.actionOpenMovementEditor = QtGui.QAction("&Add movement", self, checkable=True,
            shortcut="Ctrl+M", statusTip="Add movement",
            triggered=self.openMovementEditor)
        self.fileMenu.addAction(self.actionOpenMovementEditor)

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
        
    def openMovementEditor(self):
        self.movementEditor = MovementEditor()
        self.movementEditor.setGeometry(QRect(100, 100, 400, 200))
        self.movementEditor.show()
        
class MovementEditor(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QtGui.QGridLayout(self)
        #lblAssetType
        self.lblAssetType = QLabel("Asset Type")
        self.layout.addWidget(self.lblAssetType, 0, 0)
        #cmdAssetType
        self.cmdAssetType = QComboBox(self)
        self.cmdAssetType.addItems(DaoAssetType().getAssetTypes())
        self.connect(self.cmdAssetType, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.loadCmdAssetName) 
        self.layout.addWidget(self.cmdAssetType, 0, 1)
        #lblAssetName
        self.lblAssetName = QLabel("Asset Name")
        self.layout.addWidget(self.lblAssetName, 1, 0)
        #cmdAssetName
        self.cmdAssetName = QComboBox(self)
        self.layout.addWidget(self.cmdAssetName, 1, 1)
        #lblBuySell
        self.lblBuySell = QLabel("Buy Sell")
        self.layout.addWidget(self.lblBuySell, 2, 0)
        #cmdBuySell
        self.cmdBuySell = QComboBox(self)
        self.cmdBuySell.addItem("BUY")
        self.cmdBuySell.addItem("SELL")
        self.layout.addWidget(self.cmdBuySell, 2, 1)
        #lblQuantity
        self.lblQuantity = QLabel("Quantity")
        self.layout.addWidget(self.lblQuantity, 3, 0)
        #txtQuantity
        self.txtQuantity = QLineEdit(self)
        self.txtQuantity.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtQuantity, 3, 1)
        #lblPrice
        self.lblPrice = QLabel("Price")
        self.layout.addWidget(self.lblPrice, 4, 0)
        #txtPrice
        self.txtPrice = QLineEdit(self)
        self.txtPrice.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtPrice, 4, 1)
        #lblRate
        self.lblRate = QLabel("Rate")
        self.layout.addWidget(self.lblRate, 5, 0)
        #txtRate
        self.txtRate = QLineEdit(self)
        self.txtRate.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtRate, 5, 1)
        #lblGrossAmount
        self.lblGrossAmount = QLabel("Gross Amount")
        self.layout.addWidget(self.lblGrossAmount, 6, 0)
        #txtGrossAmount
        self.txtGrossAmount = QLineEdit(self)
        self.txtGrossAmount.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtGrossAmount, 6, 1)
        #lblNetAmount
        self.lblNetAmount = QLabel("Net Amount")
        self.layout.addWidget(self.lblNetAmount, 7, 0)
        #txtNetAmount
        self.txtNetAmount = QLineEdit(self)
        self.txtNetAmount.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtNetAmount, 7, 1)
        #lblCommissionPercentage
        self.lblCommissionPercentage = QLabel("Commission Percentage")
        self.layout.addWidget(self.lblCommissionPercentage, 8, 0)
        #txtCommissionPercentage
        self.txtCommissionPercentage = QLineEdit(self)
        self.txtCommissionPercentage.setValidator(QIntValidator(0, 10000, self))
        self.layout.addWidget(self.txtCommissionPercentage, 8, 1)
        #btnAdd
        self.btnAdd = QPushButton("Add", self)
        self.layout.addWidget(self.btnAdd)
        self.actAddMovement = QtGui.QAction("&Add movement", self, checkable=True,
            shortcut="Ctrl+A", statusTip="Add movement",
            triggered=self.addMovement)
        self.btnAdd.addAction(self.actAddMovement)
        #btnClear
        self.btnClear = QPushButton("Clear", self)
        self.layout.addWidget(self.btnClear)
    
    def addMovement(self):
        movement = EquityMovement()
        #movement.assetOID = txt
        
        
    def loadCmdAssetName(self):
        self.cmdAssetName.clear()
        self.cmdAssetName.addItems(DaoAssetType().getAssetNames(self.cmdAssetType.currentText()))  
        