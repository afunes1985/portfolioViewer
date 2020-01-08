'''
Created on 29 ene. 2018

@author: afunes
'''

from PySide import QtGui, QtCore
from PySide.QtGui import QTableWidget

from engine.engine import Engine
from frame.ReportMovementFilter import ReportMovementFilter
from frame.framework import PanelWithTable
from core.constant import Constant


class ReportMovementPanel(PanelWithTable):
    
    columnList = "EVENT_ID;EVENT_TYPE; EVENT_SUB_TYPE; EVENT_DIRECTION; ASSET_NAME; EVENT_DATE; QUANTITY; PRICE; RATE; GROSS_AMOUNT; NET_AMOUNT; COMMISSION_PERCENTAGE; COMMISSION_AMOUNT; COMMISSION_IVA_AMOUNT; TENOR; MATURITY_DATE; CUSTODY_NAME; TAX_ID; TAX_AMOUNT; COMMENT; EXTERNAL_ID".split(";");
    
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.reportMovementFilter = ReportMovementFilter(self)
        self.layout.addWidget(self.reportMovementFilter, 1, 0, QtCore.Qt.AlignTop)
        self.layout.addWidget(self.createTable(), 1, 1, QtCore.Qt.AlignTop)

    def createTable(self):
        self.table = QTableWidget()
        self.table.setRowCount(1000)
        self.table.setColumnCount(len(self.columnList))
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(self.columnList)
        #self.pnLTableWidget.resizeColumnsToContents()
        self.table.sortItems(Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_DATE)
        self.table.resizeRowsToContents()
        self.table.setFixedSize(1100, 900) 
        return self.table 
        
    def doSubmit(self, fromDate, toDate, movementType, assetName, custodyName):
        reportMovementLO = Engine.getReportMovementList(fromDate, toDate, movementType, assetName, custodyName)
        self.table.setSortingEnabled(False) 
        self.table.clearContents()
        self.table.setRowCount(len(reportMovementLO.movementList))
        self.renderTable(reportMovementLO.movementList)
        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents() 
    
    def renderTable(self, tableList):
        row = 0
        isBold = False
        for listItem in tableList:
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_ID, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_TYPE, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_SUB_TYPE, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_DIRECTION, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_ASSET_NAME, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_DATE, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_QUANTITY, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_PRICE, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_RATE, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_GROSS_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_NET_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_PERCENTAGE, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_IVA_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_TENOR, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_CUSTODY_NAME, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_TAX_ID, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_TAX_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMENT, isBold)
            self.addItemtoTable(self.table,listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EXTERNAL_ID, isBold)
            row += 1
            
