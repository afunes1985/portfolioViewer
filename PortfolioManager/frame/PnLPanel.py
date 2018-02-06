'''
Created on 29 ene. 2018

@author: afunes
'''
from PySide import QtGui, QtCore
from PySide.QtGui import QTableWidget

from engine.engine import Engine
from frame.PnLFilter import PnLFilter
from frame.framework import QTableWidgetItemDecimal
from modelClass.constant import Constant


class PnLPanel(QtGui.QWidget):
    
    pnLColumnList = "Initial Position;Final Position;Cash In;Weighted Cash In; Cash Out;Weighted Cash Out;PnL;Weighted PnL;TIR;Weighted TIR".split(";");
    
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.pnlFilter = PnLFilter(self)
        self.layout.addWidget(self.pnlFilter, 1, 0, QtCore.Qt.AlignTop)
        #self.layout.setAlignment(self.pnlFilter, QtCore.Qt.AlignTop)
        #self.layout.setAlignment(self.pnlFilter, QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.createPnLTable(), 1, 1, QtCore.Qt.AlignTop)
        #self.layout.setAlignment(self.pnLTableWidget, QtCore.Qt.AlignTop)
        #self.layout.setAlignment(self.pnLTableWidget, QtCore.Qt.AlignLeft)

    def createPnLTable(self):
        self.pnLTableWidget = QTableWidget()
        self.pnLTableWidget.setRowCount(6)
        self.pnLTableWidget.setColumnCount(len(self.pnLColumnList))
        self.pnLTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.pnLTableWidget.setHorizontalHeaderLabels(self.pnLColumnList)
        #self.pnLTableWidget.resizeColumnsToContents()
        self.pnLTableWidget.resizeRowsToContents()
        self.pnLTableWidget.setFixedSize(1100, 150) 
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
        #totalWeightedCashIn
        totalWeightedCashInItem = QTableWidgetItemDecimal(pnlLO.totalWeightedCashIn, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_WEIGHTED_CASH_IN,totalWeightedCashInItem)
        #totalCashOut
        totalCashOutItem = QTableWidgetItemDecimal(pnlLO.totalCashOut, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_CASH_OUT,totalCashOutItem)
        #totalWeightedCashOut
        totalWeightedCashOutItem = QTableWidgetItemDecimal(pnlLO.totalWeightedCashOut, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_WEIGHTED_CASH_OUT,totalWeightedCashOutItem)
        #pnlAmount
        pnlAmountItem = QTableWidgetItemDecimal(pnlLO.pnlAmount, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_PNL_AMOUNT,pnlAmountItem)
        #pnlWeightedAmount
        pnlWeightedAmountItem = QTableWidgetItemDecimal(pnlLO.pnlWeightedAmount, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_WEIGHTED_PNL_AMOUNT,pnlWeightedAmountItem)
        #tir
        tirItem = QTableWidgetItemDecimal(pnlLO.tir, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_TIR,tirItem)
        #weightedtir
        weightedTirItem = QTableWidgetItemDecimal(pnlLO.weightedTir, False)
        self.pnLTableWidget.setItem(0,Constant.CONST_COLUMN_PNL_WEIGHTED_TIR,weightedTirItem)
