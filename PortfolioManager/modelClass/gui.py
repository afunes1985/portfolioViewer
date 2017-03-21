'''
Created on Feb 19, 2017

@author: afunes
'''
import datetime

from PySide import QtGui, QtCore
from PySide.QtCore import QRect, SIGNAL
from PySide.QtGui import QTableWidget, QTableWidgetItem, QWidget, \
    QLineEdit, QIntValidator, QLabel, QComboBox, QPushButton, \
    QDateEdit, QDoubleValidator
import requests

from dao.dao import DaoAssetType, DaoMovement
from modelClass.constant import Constant
from modelClass.movement import Movement


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
        #lblAssetName
        self.lblAssetName = QLabel("Asset Name")
        self.layout.addWidget(self.lblAssetName, 1, 0)
        #cmdAssetName
        self.cmdAssetName = QComboBox(self)
        self.layout.addWidget(self.cmdAssetName, 1, 1)
        #lblAssetType
        self.lblAssetType = QLabel("Asset Type")
        self.layout.addWidget(self.lblAssetType, 0, 0)
        #cmdAssetType
        self.cmdAssetType = QComboBox(self)
        self.connect(self.cmdAssetType, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.configEditorByAssetType) 
        self.cmdAssetType.addItems(DaoAssetType().getAssetTypes())
        self.layout.addWidget(self.cmdAssetType, 0, 1)
        #lblBuySell
        self.lblBuySell = QLabel("Buy Sell")
        self.layout.addWidget(self.lblBuySell, 2, 0)
        #cmdBuySell
        self.cmdBuySell = QComboBox(self)
        self.cmdBuySell.addItem("BUY")
        self.cmdBuySell.addItem("SELL")
        self.connect(self.cmdBuySell, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.calculateNetAmount) 
        self.layout.addWidget(self.cmdBuySell, 2, 1)
        #lblAcquisitionDate
        self.lblAcquisitionDate = QLabel("Acquisition Date")
        self.layout.addWidget(self.lblAcquisitionDate, 3, 0)
        #cmdAcquisitionDate
        self.dateAcquisitionDate = QDateEdit(self)
        self.dateAcquisitionDate.setDisplayFormat("dd-MM-yyyy")
        self.dateAcquisitionDate.setDate(datetime.datetime.now())
        self.layout.addWidget(self.dateAcquisitionDate, 3, 1)
        #lblQuantity
        self.lblQuantity = QLabel("Quantity")
        self.layout.addWidget(self.lblQuantity, 4, 0)
        #txtQuantity
        self.txtQuantity = QLineEdit(self)
        self.txtQuantity.connect(self.txtQuantity,SIGNAL("textChanged(QString)"),self.calculateGrossAmount) 
        self.txtQuantity.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtQuantity, 4, 1)
        #lblPrice
        self.lblPrice = QLabel("Price")
        self.layout.addWidget(self.lblPrice, 5, 0)
        #txtPrice
        self.txtPrice = QLineEdit(self)
        self.txtPrice.setValidator(QDoubleValidator(0, 999999999, 2, self))
        self.txtPrice.connect(self.txtPrice,SIGNAL("textChanged(QString)"),self.calculateGrossAmount) 
        self.layout.addWidget(self.txtPrice, 5, 1)
        #lblRate
        self.lblRate = QLabel("Rate")
        self.layout.addWidget(self.lblRate, 6, 0)
        #txtRate
        self.txtRate = QLineEdit(self)
        self.txtRate.setValidator(QDoubleValidator(0, 999999999, 4, self))
        self.txtRate.setEnabled(0)
        self.layout.addWidget(self.txtRate, 6, 1)
        #lblGrossAmount
        self.lblGrossAmount = QLabel("Gross Amount")
        self.layout.addWidget(self.lblGrossAmount, 7, 0)
        #txtGrossAmount
        self.txtGrossAmount = QLineEdit(self)
        self.txtGrossAmount.setEnabled(0)
        self.txtGrossAmount.setValidator(QDoubleValidator(0, 99999999999, 2, self))
        self.layout.addWidget(self.txtGrossAmount, 7, 1)
        #lblNetAmount
        self.lblNetAmount = QLabel("Net Amount")
        self.layout.addWidget(self.lblNetAmount, 8, 0)
        #txtNetAmount
        self.txtNetAmount = QLineEdit(self)
        self.txtNetAmount.setEnabled(0)
        self.txtNetAmount.setValidator(QDoubleValidator(0, 99999999999, 2, self))
        self.layout.addWidget(self.txtNetAmount, 8, 1)
        #lblCommissionPercentage
        self.lblCommissionPercentage = QLabel("Commission Percentage")
        self.layout.addWidget(self.lblCommissionPercentage, 9, 0)
        #txtCommissionPercentage
        self.txtCommissionPercentage = QLineEdit(self)
        self.txtCommissionPercentage.setValidator(QDoubleValidator(0, 9999999, 4, self))
        self.txtCommissionPercentage.connect(self.txtCommissionPercentage,SIGNAL("textChanged(QString)"),self.calculateCommission) 
        self.layout.addWidget(self.txtCommissionPercentage, 9, 1)
        #lblCommissionAmount
        self.lblCommissionAmount = QLabel("Commission Amount")
        self.layout.addWidget(self.lblCommissionAmount, 10, 0)
        #txtCommissionAmmount
        self.txtCommissionAmount = QLineEdit(self)
        self.txtCommissionAmount.setEnabled(0)
        self.txtCommissionAmount.setValidator(QDoubleValidator(0, 9999999, 4, self))
        self.layout.addWidget(self.txtCommissionAmount, 10, 1)
        #lblCommissionAmount
        self.lblCommissionVATAmount = QLabel("Commission VAT Amount")
        self.layout.addWidget(self.lblCommissionVATAmount, 11, 0)
        #txtCommissionAmmount
        self.txtCommissionVATAmount = QLineEdit(self)
        self.txtCommissionVATAmount.setEnabled(0)
        self.txtCommissionVATAmount.setValidator(QDoubleValidator(0, 9999999, 4, self))
        self.layout.addWidget(self.txtCommissionVATAmount, 11, 1)
        #lblTenor
        self.lblTenor = QLabel("Tenor")
        self.layout.addWidget(self.lblTenor, 12, 0)
        #txtTenor
        self.txtTenor = QLineEdit(self)
        self.txtTenor.setEnabled(0)
        self.txtTenor.setValidator(QDoubleValidator(0, 9999999, 4, self))
        self.layout.addWidget(self.txtTenor, 12, 1)
        #btnAdd
        self.btnAdd = QPushButton("Add", self)
        self.btnAdd.clicked.connect(self.addMovement)
        self.layout.addWidget(self.btnAdd)
        #btnClear
        self.btnClear = QPushButton("Clear", self)
        self.btnClear.clicked.connect(self.clearEditor)
        self.layout.addWidget(self.btnClear)
        #clearEditor
        self.clearEditor()
    
    def addMovement(self):
        movement = Movement().constructMovementByType(self.cmdAssetType.currentText())
        movement.buySell = self.cmdBuySell.currentText()
        movement.assetOID = self.cmdAssetName.itemData(self.cmdAssetName.currentIndex())
        movement.acquisitionDate = (self.dateAcquisitionDate.date()).toString("yyyy-M-dd")
        movement.quantity = self.txtQuantity.text()
        if self.cmdAssetType.currentText() == 'BOND':
            movement.rate = self.txtRate.text();
        else:  
            movement.price = self.txtPrice.text()
        movement.grossAmount = self.txtGrossAmount.text()
        movement.netAmount = self.txtNetAmount.text()
        movement.commissionPercentage = self.txtCommissionPercentage.text()
        movement.commissionAmount = self.txtCommissionAmount.text()
        movement.commissionIVAAmount = self.txtCommissionVATAmount.text()
        DaoMovement().insertMovement(movement)
        self.clearEditor()
    
    def clearEditor(self):
        #self.cmdAssetType.set
        self.txtQuantity.setText("0")
        self.txtPrice.setText("0")
        self.txtGrossAmount.setText("0")
        self.txtNetAmount.setText("0")
        self.txtRate.setText("0")
        self.txtCommissionPercentage.setText("0")
        self.dateAcquisitionDate.setDate(datetime.datetime.now())
        
    def configEditorByAssetType(self):
        self.cmdAssetName.clear()
        #loadAssetNames
        assetNameList = DaoAssetType().getAssetNames(self.cmdAssetType.currentText())
        for (assetName) in assetNameList:
            self.cmdAssetName.addItem(assetName[1], assetName[0]) 
        #setPriceOrRate    
        if self.cmdAssetType.currentText() == 'EQUITY' or self.cmdAssetType.currentText() == 'FUND':
            self.txtPrice.setEnabled(1)
            self.txtRate.setEnabled(0)
            self.txtRate.setText("0")
            self.txtTenor.setEnabled(0)
            self.txtTenor.setText("")
        else:
            self.txtPrice.setEnabled(0)
            self.txtRate.setEnabled(1)
            self.txtPrice.setText(str(0))
            self.txtTenor.setEnabled(1)
        #configDefaultCommission
        if self.cmdAssetType.currentText() == 'EQUITY':
            self.txtCommissionPercentage.setText(str(Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE))
        else:
            self.txtCommissionPercentage.setText(str(Constant.CONST_DEF_OTHER_COMMISSION_PERCENTAGE))
        
    
    def calculateCommission(self):
        commissionPercentage = self.txtCommissionPercentage.text()
        grossAmount = self.txtGrossAmount.text() 
        if commissionPercentage >= 0:
            commissionAmount = float(grossAmount) * float(commissionPercentage)
            self.txtCommissionAmount.setText(str(commissionAmount))
            commissionVATAmount = commissionAmount * Constant.CONST_IVA_PERCENTAGE
            self.txtCommissionVATAmount.setText(str(commissionVATAmount))
            self.calculateNetAmount()
        
    
    def calculateNetAmount(self):
        buySell = self.cmdBuySell.currentText()
        grossAmount = float(self.txtGrossAmount.text()) 
        commissionAmount = float(self.txtCommissionAmount.text())
        commissionVATAmount = float(self.txtCommissionVATAmount.text())
        if buySell == 'BUY':
            netAmount = grossAmount + commissionVATAmount + commissionAmount
        else:
            netAmount = grossAmount - commissionVATAmount - commissionAmount    
        self.txtNetAmount.setText(str(netAmount))
        
    def calculateGrossAmount(self):
        quantity = self.txtQuantity.text()
        price = self.txtPrice.text()
        if quantity is not None and price is not None:
            self.txtGrossAmount.setText(str(float(quantity) * float(price)))
            self.calculateCommission()
        