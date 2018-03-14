'''
Created on 29 ene. 2018

@author: afunes
'''
from datetime import datetime
from decimal import Decimal

from PySide import QtGui, QtCore
from PySide.QtGui import QTableWidget

from engine.engine import Engine
from frame.ReportMovementFilter import ReportMovementFilter
from frame.framework import QTableWidgetItemDecimal, QTableWidgetItemString, \
    QTableWidgetItemInt, QTableWidgetItem6Decimal
from modelClass.constant import Constant


class ReportMovementPanel(QtGui.QWidget):
    
    columnList = "EVENT_ID;EVENT_TYPE; EVENT_SUB_TYPE; EVENT_DIRECTION; ASSET_NAME; EVENT_DATE; QUANTITY; PRICE; RATE; GROSS_AMOUNT; NET_AMOUNT; COMMISSION_PERCENTAGE; COMMISSION_AMOUNT; COMMISSION_IVA_AMOUNT; TENOR; CUSTODY_NAME; TAX_ID; TAX_AMOUNT; COMMENT; EXTERNAL_ID".split(";");
    
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
        for listItem in tableList:
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_ID)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_TYPE)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_SUB_TYPE)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_DIRECTION)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_ASSET_NAME)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EVENT_DATE)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_QUANTITY)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_PRICE)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_RATE)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_GROSS_AMOUNT)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_NET_AMOUNT)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_PERCENTAGE)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_AMOUNT)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMISSION_IVA_AMOUNT)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_TENOR)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_CUSTODY_NAME)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_TAX_ID)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_TAX_AMOUNT)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_COMMENT)
            self.addItemtoTable(listItem,row,Constant.CONST_COLUMN_REPORT_MOVEMENT_EXTERNAL_ID)
            row += 1
            
    def addItemtoTable(self, listItem, row, column):
        if isinstance(listItem[column], basestring):
            Item = QTableWidgetItemString(listItem[column], False)
        elif isinstance(listItem[column], datetime):
            Item = QTableWidgetItemString(listItem[column].strftime("%Y-%m-%d"), False)
        elif isinstance(listItem[column], (int, long)):
            Item = QTableWidgetItemInt(listItem[column], False)
        elif isinstance(listItem[column], (float, Decimal)):
            if float(listItem[column]).is_integer():
                Item = QTableWidgetItemInt(listItem[column], False)
            else:
                Item = QTableWidgetItem6Decimal(listItem[column], False)
        elif listItem[column] is None:
            Item = QTableWidgetItemString(listItem[column], False)
        self.table.setItem(row,column,Item)