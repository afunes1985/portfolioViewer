'''
Created on 29 ene. 2018

@author: afunes
'''
from PySide import QtGui
from PySide.QtGui import QTableWidget

from frame.framework import QTableWidgetItemDecimal
from modelClass.constant import Constant
from engine.engine import Engine
from frame.PnLFilter import PnLFilter


class PnLPanel(QtGui.QWidget):
    
    pnLColumnList = "Initial Position;Final Position;Cash In;Cash Out;PnL;TIR".split(";");
    
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.pnlFilter = PnLFilter(self)
        self.layout.addWidget(self.pnlFilter, 1, 0)
        self.layout.addWidget(self.createPnLTable(), 1, 1)

    def createPnLTable(self):
        self.pnLTableWidget = QTableWidget()
        self.pnLTableWidget.setRowCount(6)
        self.pnLTableWidget.setColumnCount(len(self.pnLColumnList))
        self.pnLTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.pnLTableWidget.setHorizontalHeaderLabels(self.pnLColumnList)
        self.pnLTableWidget.resizeColumnsToContents()
        self.pnLTableWidget.resizeRowsToContents()
        self.pnLTableWidget.setFixedSize(700, 150) 
        return self.pnLTableWidget 
        
    def doSubmit(self, fromDate, toDate):
        pnlLO = Engine.buildPnlLogicObject()
        self.renderPnlTable(pnlLO)
    
    def renderPnlTable(self, pnlLO):
        #initialPositionItem
        initialPositionItem = QTableWidgetItemDecimal(pnlLO.initialPosition, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_INITIAL_POSITION,initialPositionItem)
        #finalPositionItem
        finalPositionItem = QTableWidgetItemDecimal(pnlLO.finalPosition, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_FINAL_POSITION,finalPositionItem)
        #totalCashIn
        totalCashInItem = QTableWidgetItemDecimal(pnlLO.totalCashIn, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_CASH_IN,totalCashInItem)
        #totalCashOut
        totalCashOutItem = QTableWidgetItemDecimal(pnlLO.totalCashOut, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_CASH_OUT,totalCashOutItem)
        #pnlAmount
        pnlAmountItem = QTableWidgetItemDecimal(pnlLO.pnlAmount, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_PNL_AMOUNT,pnlAmountItem)
        #tir
        tirItem = QTableWidgetItemDecimal(pnlLO.tir, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_TIR,tirItem)
