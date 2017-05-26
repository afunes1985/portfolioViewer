'''
Created on Feb 19, 2017

@author: afunes
'''

from datetime import date

from PySide import QtGui
from PySide.QtGui import  QTableWidget, QLabel, QDateEdit, \
    QPushButton, QSizePolicy, QWidget

from core.cache import Singleton
from engine.engine import Engine
from frame.framework import QTableWidgetItemDecimal, \
    QTableWidgetItemDecimalColor, QTableWidgetItemString, QTableWidgetItemInt, \
    QTableWidgetItemDuoDecimal, QTableWidgetItem6Decimal, QTableWidgetItemDuoInt
from modelClass.constant import Constant


class MainWidget(QtGui.QWidget):
    tableWidget = None
    movementFilterWidget = None
    row = 0
    columnList = "Asset Name;Position;Unit Cost;Market Price;Invested amount;Valuated amount;Tenor;Maturity Date;Gross PNL;Net PNL;Gross%PNL;%Portfolio;WeightedPNL%".split(";");
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.movementFilterWidget = MovementFilterWidget()
        self.layout.addWidget(self.movementFilterWidget, 1, 0)
    
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(27)
        self.tableWidget.setColumnCount(len(self.columnList) +1)
        self.tableWidget.setColumnHidden(Constant.CONST_COLUMN_POSITION_HIDDEN_ID, True)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(self.columnList)
        #self.tableWidget.setSortingEnabled(True)  
        #self.tableWidget.sortItems(0)  
        #self.setCentralWidget(self.tableWidget)  
        self.tableWidget.doubleClicked.connect(self.openMovementView)
        self.layout.addWidget(self.tableWidget, 2, 0, 2, 2)   
        
    def renderSubtotal(self, positionDict, assetType ,isSIC):  
        subTotalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        totalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, 'ALL', isSIC)
        positionPercentage = (subTotalValuatedAmount * 100) / totalValuatedAmount
        subTotalInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        subTotalPnlPercentage = (subTotalValuatedAmount / subTotalInvestedAmount -1 ) * 100
        subTotalNetPNL = Engine.getSubtotalNetPNL(positionDict, assetType, isSIC)
        subTotalWeightedPNL = subTotalPnlPercentage * positionPercentage / 100
        #=======================================================================
        # self.paintEntireRow(self.row)
        #=======================================================================
        #Invested amount
        investedAmountItem = QTableWidgetItemDecimal(subTotalInvestedAmount)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
        #sub total valuated amount
        subTotalValuatedAmountItem = QTableWidgetItemDecimal(Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC))
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,subTotalValuatedAmountItem)   
        #sub total Gross PNL    
        subTotalGrossPNLItem = QTableWidgetItemDecimalColor(Engine.getSubtotalGrossPNL(positionDict, assetType, isSIC))
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL,subTotalGrossPNLItem)
        #sub total Net PNL    
        subTotalNetPNLItem = QTableWidgetItemDecimalColor(subTotalNetPNL)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_NET_PNL,subTotalNetPNLItem)
        #subTotalGrossPnLPercentage
        subTotalGrossPnLPercentage = QTableWidgetItemDecimalColor(subTotalPnlPercentage)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL_PERCENTAGE,subTotalGrossPnLPercentage)
        #positionPercentage
        positionPercentageItem = QTableWidgetItemDecimal(positionPercentage)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
        #weightedPercentageItem
        weightedPercentageItem = QTableWidgetItemDecimal(subTotalWeightedPNL)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_WEIGHTED_PNL,weightedPercentageItem)
        #HiddenID
        hiddenIDItem = QTableWidgetItemDecimal(self.row)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_HIDDEN_ID,hiddenIDItem)

    def renderPositions(self, positionDict, assetType ,isSIC):   
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        totalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, 'ALL', isSIC)
        for position in positionList:
            print('processing ' + position.getAssetName())
            position.row = self.row
            #assetName
            assetNameItem = QTableWidgetItemString(position.getAssetName())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_ASSET_NAME,assetNameItem)
            #totalQuantity
            totalQuantityItem = QTableWidgetItemInt(position.getTotalQuantity())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_QUANTITY,totalQuantityItem)
            #PPP
            pppItem = QTableWidgetItemDecimal(position.getPPP())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PPP,pppItem)
            #Market price
            marketPriceItem = QTableWidgetItemDuoDecimal(position.getMarketPrice(), position.getMarketPriceOrig())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MARKET_PRICE,marketPriceItem)
            #Invested amount
            investedAmountItem = QTableWidgetItemDecimal(position.getInvestedAmount())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
            #Valuated amount
            valuatedAmountItem = QTableWidgetItemDuoDecimal(position.getValuatedAmount(), position.getValuatedAmountOrig())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,valuatedAmountItem)
            #Tenor
            tenorItem = QTableWidgetItemDuoInt(position.tenor, position.getElapsedDays())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_TENOR,tenorItem)
            #Maturity Date
            maturityDateItem = QTableWidgetItemString(position.getMaturityDate())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MATURITY_DATE,maturityDateItem)
            #GrossPnL
            grossPnlItem = QTableWidgetItemDecimalColor(position.getGrossPnL())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL,grossPnlItem)
            #netPnL
            netPnlItem = QTableWidgetItemDecimalColor(position.getNetPnL())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_NET_PNL,netPnlItem)
            #pnLGrossPercentage
            pnLGrossPercentageItem = QTableWidgetItemDecimalColor(position.getGrossPnLPercentage())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL_PERCENTAGE,pnLGrossPercentageItem)
            #positionPercentage
            positionPercentage = (position.getValuatedAmount() * 100) / totalValuatedAmount
            positionPercentageItem = QTableWidgetItemDecimal(positionPercentage)
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
            #weightedPercentageItem
            weightedPNL = position.getGrossPnLPercentage() * positionPercentage / 100
            weightedPercentageItem = QTableWidgetItemDecimal(weightedPNL)
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_WEIGHTED_PNL,weightedPercentageItem)
            #HiddenID
            hiddenIDItem = QTableWidgetItemDecimal(self.row)
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_HIDDEN_ID,hiddenIDItem)
            self.row +=1  
        self.renderSubtotal(positionDict, assetType, isSIC)
        self.row +=1 
        
    def openMovementView(self):
        assetName = self.tableWidget.item(self.tableWidget.currentRow(), Constant.CONST_COLUMN_POSITION_ASSET_NAME).text()
        movementList = Engine.getMovementListByAsset(assetName, (self.movementFilterWidget.dateFromDate.date()).toString("yyyy-M-dd"),(self.movementFilterWidget.dateToDate.date()).toString("yyyy-M-dd"))
        self.movementView = MovementView(movementList)
        self.movementView.show()
            
class MovementFilterWidget(QtGui.QWidget):
    def __init__(self):      
        super(MovementFilterWidget, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        #lblFromDate
        self.lblFromDate = QLabel("From Date")
        self.lblFromDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.lblFromDate, 1, 0)
        #dateFromDate
        self.dateFromDate = QDateEdit(self)
        self.dateFromDate.setDisplayFormat("dd-MM-yyyy")
        self.dateFromDate.setDate(date(2001, 7, 14))
        self.dateFromDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.dateFromDate, 1, 1)
        #lblToDate
        self.lblToDate = QLabel("To Date")
        self.lblToDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.lblToDate, 2, 0)
        #dateToDate
        self.dateToDate = QDateEdit(self)
        self.dateToDate.setDisplayFormat("dd-MM-yyyy")
        self.dateToDate.setDate(date(2020, 7, 14))
        self.dateToDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.dateToDate, 2, 1)
        #btnSubmit
        self.btnSubmit = QPushButton("Submit", self)
        self.btnSubmit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.btnSubmit)
        self.setFixedSize(190, 100) 
        self.initListener() 
    
    def initListener(self):
        self.btnSubmit.clicked.connect(self.doSubmit)
    
    def doSubmit(self):
        from core.mainEngine import MainEngine
        mainWindow = Singleton(MainEngine)
        mainWindow.refreshAll((self.dateFromDate.date()).toString("yyyy-M-dd"),(self.dateToDate.date()).toString("yyyy-M-dd"))
        
class MovementView(QWidget):
    tableWidget = None
    row = 0
    columnList = "Asset Name;Buy Sell;Acquisition Date;Quantity;Price;Gross Amount;Net Amount;Comm %;Comm Amount; Comm VAT Amount".split(";")
    def __init__(self, movementList):
        QWidget.__init__(self)
        self.layout = QtGui.QGridLayout(self)
        self.tableWidget = QTableWidget()
        self.resize(1200, 400)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(len(self.columnList)+1)
        self.tableWidget.setHorizontalHeaderLabels(self.columnList)
        self.layout.addWidget(self.tableWidget, 1, 0)   
        for (movement) in movementList:
            self.renderMovements(movement)
        
    def renderMovements(self, movement):
        #assetName
        assetNameItem = QTableWidgetItemString(movement.assetName)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_ASSET_NAME,assetNameItem)
        #buysell
        buySellItem = QTableWidgetItemString(movement.buySell)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_BUYSELL,buySellItem)
        #acquisitionDate
        acquisitionDateItem = QTableWidgetItemString(movement.getAcquisitionDate())
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_ACQUISITION_DATE,acquisitionDateItem)
        #quantity
        quantityItem = QTableWidgetItem6Decimal(movement.quantity)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_QUANTITY,quantityItem)
        #price
        priceItem = QTableWidgetItem6Decimal(movement.price)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_PRICE,priceItem)
        #grossAmount
        grossAmountItem = QTableWidgetItem6Decimal(movement.grossAmount)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_GROSS_AMOUNT,grossAmountItem)
        #netAmount
        netAmountItem = QTableWidgetItem6Decimal(movement.netAmount)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_NET_AMOUNT,netAmountItem)
        #commissionPercentage
        commissionPercentageItem = QTableWidgetItem6Decimal(movement.commissionPercentage)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_COMMISSION_PERCENTAGE,commissionPercentageItem)
        #commissionAmount
        commissionAmountItem = QTableWidgetItem6Decimal(movement.commissionAmount)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_COMMISSION_AMOUNT,commissionAmountItem)
        #commissionVATAmount
        commissionVATAmountItem = QTableWidgetItem6Decimal(movement.commissionVATAmount)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_COMMISSION_VAT_AMOUNT,commissionVATAmountItem)
        self.row +=1 