'''
Created on 5 jun. 2017

@author: afunes
'''
from PySide import QtGui
from PySide.QtGui import QWidget, QTableWidget

from frame.framework import QTableWidgetItemString, QTableWidgetItem6Decimal, \
    QTableWidgetItemInt
from modelClass.constant import Constant


class MovementView(QWidget):
    positionTableWidget = None
    row = 0
    columnList = "Asset Name;Buy Sell;Acquisition Date;Quantity;Price;Gross Amount;Net Amount;Comm %;Comm Amount; Comm VAT Amount".split(";")
    def __init__(self, movementList):
        QWidget.__init__(self)
        self.layout = QtGui.QGridLayout(self)
        self.positionTableWidget = QTableWidget()
        self.resize(1200, 400)
        self.positionTableWidget.setRowCount(15)
        self.positionTableWidget.setColumnCount(len(self.columnList))
        self.positionTableWidget.setHorizontalHeaderLabels(self.columnList)
        self.positionTableWidget.resizeColumnsToContents()
        self.positionTableWidget.resizeRowsToContents()
        self.layout.addWidget(self.positionTableWidget, 1, 0)   
        for (movement) in movementList:
            self.renderMovements(movement)
        
    def renderMovements(self, movement):
        #assetName
        assetNameItem = QTableWidgetItemString(movement.assetName, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_ASSET_NAME,assetNameItem)
        #buysell
        buySellItem = QTableWidgetItemString(movement.buySell, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_BUYSELL,buySellItem)
        #acquisitionDate
        acquisitionDateItem = QTableWidgetItemString(movement.getAcquisitionDate(), False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_ACQUISITION_DATE,acquisitionDateItem)
        #quantity
        quantityItem = QTableWidgetItemInt(movement.quantity, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_QUANTITY,quantityItem)
        #price
        priceItem = QTableWidgetItem6Decimal(movement.price, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_PRICE,priceItem)
        #grossAmount
        grossAmountItem = QTableWidgetItem6Decimal(movement.grossAmount, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_GROSS_AMOUNT,grossAmountItem)
        #netAmount
        netAmountItem = QTableWidgetItem6Decimal(movement.netAmount, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_NET_AMOUNT,netAmountItem)
        #commissionPercentage
        commissionPercentageItem = QTableWidgetItem6Decimal(movement.commissionPercentage, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_COMMISSION_PERCENTAGE,commissionPercentageItem)
        #commissionAmount
        commissionAmountItem = QTableWidgetItem6Decimal(movement.commissionAmount, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_COMMISSION_AMOUNT,commissionAmountItem)
        #commissionVATAmount
        commissionVATAmountItem = QTableWidgetItem6Decimal(movement.commissionVATAmount, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_MOVEMENT_COMMISSION_VAT_AMOUNT,commissionVATAmountItem)
        self.row +=1 