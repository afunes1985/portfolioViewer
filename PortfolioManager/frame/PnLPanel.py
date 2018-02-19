'''
Created on 29 ene. 2018

@author: afunes
'''
from PySide import QtGui, QtCore
from PySide.QtGui import QTableWidget

from engine.engine import Engine
from frame.PnLFilter import PnLFilter
from frame.framework import QTableWidgetItemDecimal, QTableWidgetItemString
from modelClass.constant import Constant


class PnLPanel(QtGui.QWidget):
    
    pnLColumnList = "Custody Name;Initial Position;Final Position;Cash In;Weighted Cash In; Cash Out;Weighted Cash Out;PnL;Weighted PnL;TIR;Weighted TIR".split(";");
    
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
        pnlLO = Engine.buildPnlLogicObject(fromDate, toDate)
        self.renderPnlTable(pnlLO.pnlVOList)
    
    def renderPnlTable(self, pnlCalculationList):
        row = 0
        for pnlVO in pnlCalculationList:
            #ItemNameItem
            ItemNameItem = QTableWidgetItemString(pnlVO.itemName, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_ITEM_NAME,ItemNameItem)
            #initialPositionItem
            initialPositionItem = QTableWidgetItemDecimal(pnlVO.initialPosition, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_INITIAL_POSITION,initialPositionItem)
            #finalPositionItem
            finalPositionItem = QTableWidgetItemDecimal(pnlVO.finalPosition, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_FINAL_POSITION,finalPositionItem)
            #totalCashIn
            totalCashInItem = QTableWidgetItemDecimal(pnlVO.totalCashIn, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_CASH_IN,totalCashInItem)
            #totalWeightedCashIn
            totalWeightedCashInItem = QTableWidgetItemDecimal(pnlVO.totalWeightedCashIn, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_WEIGHTED_CASH_IN,totalWeightedCashInItem)
            #totalCashOut
            totalCashOutItem = QTableWidgetItemDecimal(pnlVO.totalCashOut, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_CASH_OUT,totalCashOutItem)
            #totalWeightedCashOut
            totalWeightedCashOutItem = QTableWidgetItemDecimal(pnlVO.totalWeightedCashOut, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_WEIGHTED_CASH_OUT,totalWeightedCashOutItem)
            #pnlAmount
            pnlAmountItem = QTableWidgetItemDecimal(pnlVO.pnlAmount, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_PNL_AMOUNT,pnlAmountItem)
            #pnlWeightedAmount
            pnlWeightedAmountItem = QTableWidgetItemDecimal(pnlVO.pnlWeightedAmount, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_WEIGHTED_PNL_AMOUNT,pnlWeightedAmountItem)
            #tir
            tirItem = QTableWidgetItemDecimal(pnlVO.tir, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_TIR,tirItem)
            #weightedtir
            weightedTirItem = QTableWidgetItemDecimal(pnlVO.weightedTir, False)
            self.pnLTableWidget.setItem(row,Constant.CONST_COLUMN_PNL_WEIGHTED_TIR,weightedTirItem)
            row += 1