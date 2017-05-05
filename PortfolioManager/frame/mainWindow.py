'''
Created on May 3, 2017

@author: afunes
'''
from datetime import date

from PySide import QtGui
from PySide.QtCore import QRect
from PySide.QtGui import QTableWidgetItem

from engine.engine import Engine
from frame.gui import MainWidget, QTableWidgetItemDecimal, \
    QTableWidgetItemString, QTableWidgetItemInt, QTableWidgetItemDecimalColor
from frame.movementEditor import MovementEditor
from modelClass.constant import Constant


class MainWindow(QtGui.QMainWindow):
    _instance = None
    mainWidget = None
    row = 0
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Portfolio Viewer')
        self.resize(1200, 800)
        self.createMenu()
        self.setCentralWidget(self.createMainWidget()) 
        self.show()
         
    def createMainWidget(self):
        self.mainWidget = MainWidget()
        return self.mainWidget
        
    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&Movement")
        self.actionOpenMovementEditor = QtGui.QAction("&Add movement", self, checkable=True,
            shortcut="Ctrl+M", statusTip="Add movement",
            triggered=self.openMovementEditor)
        self.fileMenu.addAction(self.actionOpenMovementEditor)

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
        self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
        #sub total valuated amount
        subTotalValuatedAmountItem = QTableWidgetItemDecimal(Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC))
        self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,subTotalValuatedAmountItem)   
        #sub total PNL    
        subTotalPNLItem = QTableWidgetItemDecimalColor(Engine.getSubtotalPNL(positionDict, assetType, isSIC))
        self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL,subTotalPNLItem)
        #Sub Total PnLPercentage
        pnlPercentageItem = QTableWidgetItemDecimalColor(subTotalPnlPercentage)
        self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL_PERCENTAGE,pnlPercentageItem)
        #PositionPercentage
        positionPercentageItem = QTableWidgetItemDecimal(positionPercentage)
        self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
    
    def paintEntireRow(self, row):
        for r in range(self.mainWidget.tableWidget.columnCount()+1):
            emptyCell = QTableWidgetItem()
            emptyCell.setBackground(QtGui.QColor(204,204,204))
            self.mainWidget.tableWidget.setItem(row, r, emptyCell)
            
    
    def renderPositions(self, positionDict, assetType ,isSIC):   
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        totalValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, 'ALL', isSIC)
        for position in positionList:
            print('processing ' + position.getAssetName())
            position.row = self.row
            #assetName
            assetNameItem = QTableWidgetItemString(position.getAssetName())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_ASSET_NAME,assetNameItem)
            #totalQuantity
            totalQuantityItem = QTableWidgetItemInt(position.getTotalQuantity())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_QUANTITY,totalQuantityItem)
            #PPP
            pppItem = QTableWidgetItemDecimal(position.getPPP())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PPP,pppItem)
            #Market price
            marketPriceItem = QTableWidgetItemDecimal(position.getMarketPrice())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MARKET_PRICE,marketPriceItem)
            #Invested amount
            investedAmountItem = QTableWidgetItemDecimal(position.getInvestedAmount())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
            #Valuated amount
            valuatedAmountItem = QTableWidgetItemDecimal(position.getValuatedAmount())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,valuatedAmountItem)
            #Tenor
            tenorItem = QTableWidgetItemInt(position.tenor)
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_TENOR,tenorItem)
            #Maturity Date
            maturityDateItem = QTableWidgetItemString(position.getMaturityDate())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MATURITY_DATE,maturityDateItem)
            #PnL
            pnlItem = QTableWidgetItemDecimalColor(position.getPnL())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL,pnlItem)
            #PnLPercentage
            pnlPercentageItem = QTableWidgetItemDecimalColor(position.getPnLPercentage())
            self.mainWidget.tableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PNL_PERCENTAGE,pnlPercentageItem)
            #PositionPercentage
            positionPercentage = (position.getValuatedAmount() * 100) / totalValuatedAmount
            positionPercentageItem = QTableWidgetItemDecimal(positionPercentage)
            self.mainWidget.tableWidget.setItem(position.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
            self.row +=1  
        self.renderSubtotal(positionDict, assetType, isSIC)
        self.row +=1 
        
    def openMovementEditor(self):
        self.movementEditor = MovementEditor()
        self.movementEditor.setGeometry(QRect(100, 100, 400, 200))
        self.movementEditor.show()
    
    def clearTable(self):
        self.row = 0
        self.mainWidget.createTable()