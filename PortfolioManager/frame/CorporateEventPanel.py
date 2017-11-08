'''
Created on Feb 19, 2017

@author: afunes
'''

from PySide import QtGui
from PySide.QtGui import QTableWidget, QTableWidgetItem

from engine.engine import Engine
from frame.MovementFilterWidget import MovementFilterWidget
from frame.framework import QTableWidgetItemDecimal, \
    QTableWidgetItemDecimalColor, QTableWidgetItemString, QTableWidgetItemInt, \
    QTableWidgetItemDuoDecimal, QTableWidgetItemDuoInt, \
    QTableWidgetItemStringPlusMinus
from modelClass.constant import Constant


class CorporateEventPanel(QtGui.QWidget):
    tableCorporateEvent = None
    rowCorporateEvent = 0
    columnListCorporateEvent = "Custody;Asset;Event Type;Payment Date;Gross Amount".split(";");
    
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.clearTables()
        
    def clearTables(self):    
        self.row = 0
        self.createCorpEventTable()
        
    def createCorpEventTable(self):
        self.tableCorporateEvent = QTableWidget()
        self.tableCorporateEvent.setRowCount(27)
        self.tableCorporateEvent.setColumnCount(len(self.columnListCorporateEvent) +1)
        self.tableCorporateEvent.setColumnHidden(Constant.CONST_COLUMN_POSITION_HIDDEN_ID, True)
        self.tableCorporateEvent.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableCorporateEvent.setHorizontalHeaderLabels(self.columnListCorporateEvent)
        #self.positionTableWidget.setSortingEnabled(True)  
        #self.positionTableWidget.sortItems(0)  
        self.tableCorporateEvent.resizeColumnsToContents()
        self.tableCorporateEvent.resizeRowsToContents()
        self.layout.addWidget(self.tableCorporateEvent, 2, 0, 3, 3)   
        
    def renderCorpEvent(self, corpEventList):   
        for corpEventRow in corpEventList:
                corpEventRow.row = self.row
                #custodyName
                custodyNameItem = QTableWidgetItemString(corpEventRow.custodyName, False)
                self.tableCorporateEvent.setItem(self.row,Constant.CONST_COLUMN_CE_CUSTODY_NAME,custodyNameItem)
                #corporateEventTypeName
                totalQuantityItem = QTableWidgetItemString(corpEventRow.corporateEventTypeName, False)
                self.tableCorporateEvent.setItem(self.row,Constant.CONST_COLUMN_CE_CORP_EVENT_TYPE,totalQuantityItem)
                #assetName
                unitCostItem = QTableWidgetItemString(corpEventRow.assetName, False)
                self.tableCorporateEvent.setItem(self.row,Constant.CONST_COLUMN_CE_ASSET_NAME,unitCostItem)
                #paymentDate
                marketPriceItem = QTableWidgetItem(corpEventRow.paymentDate)
                self.tableCorporateEvent.setItem(self.row,Constant.CONST_COLUMN_CE_PAYMENT_DATE,marketPriceItem)
                #grossAmount
                changePercentageItem = QTableWidgetItemString(corpEventRow.grossAmount, False)
                self.tableCorporateEvent.setItem(self.row,Constant.CONST_COLUMN_CE_GROSS_AMOUNT,changePercentageItem)
                #HiddenID
                hiddenIDItem = QTableWidgetItemDecimal(self.rowCorporateEvent, False)
                self.tableCorporateEvent.setItem(self.row,Constant.CONST_COLUMN_CE_HIDDEN_ID,hiddenIDItem)
                self.row +=1  
