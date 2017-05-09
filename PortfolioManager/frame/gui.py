'''
Created on Feb 19, 2017

@author: afunes
'''

from datetime import date

from PySide import QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem, QTableWidget, QLabel, QDateEdit, \
    QPushButton, QSizePolicy

from core.cache import Singleton
from engine.engine import Engine
from modelClass.constant import Constant


class QTableWidgetItemString(QTableWidgetItem):
    def __init__(self, value):
        super(self.__class__, self).__init__(value)
        self.setTextAlignment(0x0080) 
          
class QTableWidgetItemDecimal(QTableWidgetItem):
    def __init__(self, value):
        super(self.__class__, self).__init__(str('{0:.2f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080)        

class QTableWidgetItemDuoDecimal(QTableWidgetItem):
    def __init__(self, value1, value2):
        if(value2 == 0):
            value = str('{0:.2f}'.format(value1))
        else:    
            value = str('{0:.2f}'.format(value1)) + '(' + str('{0:.2f}'.format(value2)) + ')'
        super(self.__class__, self).__init__(str(value))
        self.setTextAlignment(0x0002 | 0x0080)

class QTableWidgetItemDecimalColor(QTableWidgetItem):
    def __init__(self, value):
        super(self.__class__, self).__init__(str('{0:.2f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080) 
        if(value < 0):  
            self.setBackground(QtGui.QColor(255,000,51))
        else:
            self.setBackground(QtGui.QColor(102,204,51))

class QTableWidgetItemInt(QTableWidgetItem):
    def __init__(self, value):
        super(self.__class__, self).__init__(str('{0:.0f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080) 

class MainWidget(QtGui.QWidget):
    tableWidget = None
    row = 0
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.layout.addWidget(MovementFilterWidget(), 1, 0)
    
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(25)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setColumnHidden(Constant.CONST_COLUMN_POSITION_HIDDEN_ID, True)
        self.tableWidget.setHorizontalHeaderLabels("Asset Name;Position;PPP;Market Price;Invested amount;Valuated amount;Tenor;Maturity Date;PNL;%PNL;%Portfolio".split(";"))
        #self.tableWidget.setSortingEnabled(True)  
        #self.tableWidget.sortItems(0)  
        #self.setCentralWidget(self.tableWidget)  
        self.layout.addWidget(self.tableWidget, 2, 0, 2, 2)   
        
    def renderSubtotal(self, positionDict, assetType ,isSIC):  
        subTotalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        totalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, 'ALL', isSIC)
        positionPercentage = (subTotalValuatedAmount * 100) / totalValuatedAmount
        subTotalInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        subTotalPnlPercentage = (subTotalValuatedAmount / subTotalInvestedAmount -1 ) * 100
        #=======================================================================
        # self.paintEntireRow(self.row)
        #=======================================================================
        #Invested amount
        investedAmountItem = QTableWidgetItemDecimal(subTotalInvestedAmount)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
        #sub total valuated amount
        subTotalValuatedAmountItem = QTableWidgetItemDecimal(Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC))
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,subTotalValuatedAmountItem)   
        #sub total PNL    
        subTotalPNLItem = QTableWidgetItemDecimalColor(Engine.getSubtotalPNL(positionDict, assetType, isSIC))
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL,subTotalPNLItem)
        #Sub Total PnLPercentage
        pnlPercentageItem = QTableWidgetItemDecimalColor(subTotalPnlPercentage)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL_PERCENTAGE,pnlPercentageItem)
        #PositionPercentage
        positionPercentageItem = QTableWidgetItemDecimal(positionPercentage)
        self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
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
            tenorItem = QTableWidgetItemInt(position.tenor)
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_TENOR,tenorItem)
            #Maturity Date
            maturityDateItem = QTableWidgetItemString(position.getMaturityDate())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MATURITY_DATE,maturityDateItem)
            #PnL
            pnlItem = QTableWidgetItemDecimalColor(position.getPnL())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL,pnlItem)
            #PnLPercentage
            pnlPercentageItem = QTableWidgetItemDecimalColor(position.getPnLPercentage())
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL_PERCENTAGE,pnlPercentageItem)
            #PositionPercentage
            positionPercentage = (position.getValuatedAmount() * 100) / totalValuatedAmount
            positionPercentageItem = QTableWidgetItemDecimal(positionPercentage)
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
            #HiddenID
            hiddenIDItem = QTableWidgetItemDecimal(self.row)
            self.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_HIDDEN_ID,hiddenIDItem)
            self.row +=1  
        self.renderSubtotal(positionDict, assetType, isSIC)
        self.row +=1 
        
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
