'''
Created on 15 jun. 2018

@author: afunes
'''
from PySide import QtGui, QtCore
from PySide.QtGui import QTableWidget, QPushButton, QSizePolicy

from dao.dao import DaoMovement, DaoCorporateEvent, DaoCashMovement
from dataImport.importPDFTABULAMovementFromGBM2 import MovementImporter
from engine.engine import Engine
from frame.ImportMovementFilter import ImportMovementFilter
from frame.framework import PanelWithTable, QTableWidgetItemDecimal
from modelClass.cashMovement import CashMovement
from modelClass.constant import Constant
from modelClass.corporateEvent import CorporateEvent
from modelClass.movement import Movement


class ImportMovementPanel(PanelWithTable):
    
    columnList = "EVENT_ID;EVENT_TYPE; EVENT_SUB_TYPE; EVENT_DIRECTION; ASSET_NAME; EVENT_DATE; QUANTITY; PRICE; RATE; GROSS_AMOUNT; NET_AMOUNT; COMMISSION_PERCENTAGE; COMMISSION_AMOUNT; COMMISSION_IVA_AMOUNT; TENOR; CUSTODY_NAME; TAX_ID; TAX_AMOUNT; COMMENT; EXTERNAL_ID".split(";");
    
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.importMovementFilter = ImportMovementFilter(self)
        self.layout.addWidget(self.importMovementFilter, 1, 0, QtCore.Qt.AlignTop)
        self.layout.addWidget(self.createTable(), 1, 1, QtCore.Qt.AlignTop)
        self.btnImport = QPushButton("Import", self)
        self.btnImport.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.btnImport)
        self.btnDelete = QPushButton("Delete", self)
        self.btnDelete.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.btnDelete)
        self.initListener()
    
    def initListener(self):
        self.btnImport.clicked.connect(self.doImport)
        self.btnDelete.clicked.connect(self.doDelete)
        
    def createTable(self):
        self.table = QTableWidget()
        self.table.setRowCount(1000)
        self.table.setColumnCount(len(self.columnList)+1)
        self.table.setColumnHidden(Constant.CONST_COLUMN_IMPORT_MOVEMENT_HIDDEN_ID, True)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(self.columnList)
        #self.pnLTableWidget.resizeColumnsToContents()
        self.table.sortItems(Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE)
        self.table.resizeRowsToContents()
        self.table.setFixedSize(1100, 900) 
        return self.table 
    
    def doSubmit(self, filePath):
        self.imLO = MovementImporter().getMovementList(filePath) 
        self.table.setSortingEnabled(False) 
        self.table.clearContents()
        countRowTable = len(self.imLO.movementList)
        self.table.setRowCount(countRowTable)
        self.renderTableForObject(self.imLO.movementList)
        imLO2 = Engine.getReportMovementList(self.imLO.fromDate, self.imLO.toDate, 'ALL', 'ALL', self.imLO.custodyName)
        countRowTable += len(imLO2.movementList)
        self.table.setRowCount(countRowTable)
        self.renderTableForRS(imLO2.movementList)
        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents() 
    
    def renderTableForObject(self, tableList):
        self.row = 0
        isBold = False
        color = QtGui.QColor(204, 255, 153)
        for movement in tableList:
            self.addItemtoTable2(self.table,None,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID, isBold, color)
            self.addItemtoTable2(self.table,movement.externalID,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EXTERNAL_ID, isBold, color)
            self.addItemtoTable2(self.table,movement.comment,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMENT, isBold, color)
            self.addItemtoTable2(self.table,movement.custody.name,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_CUSTODY_NAME, isBold, color)
            if(isinstance(movement, Movement)):
                self.addItemtoTable2(self.table,"MOVEMENT",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE, isBold, color)
                self.addItemtoTable2(self.table,"TRX",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE, isBold, color)
                self.addItemtoTable2(self.table,movement.buySell,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DIRECTION, isBold, color)
                self.addItemtoTable2(self.table,movement.asset.name,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME, isBold, color)
                self.addItemtoTable2(self.table,movement.acquisitionDate,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE, isBold, color)
                self.addItemtoTable2(self.table,movement.quantity,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_QUANTITY, isBold, color)
                self.addItemtoTable2(self.table,movement.price,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_PRICE, isBold, color)
                self.addItemtoTable2(self.table,movement.rate,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_RATE, isBold, color)
                self.addItemtoTable2(self.table,movement.grossAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.netAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.commissionPercentage,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_PERCENTAGE, isBold, color)
                self.addItemtoTable2(self.table,movement.commissionAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.commissionVATAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_IVA_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.tenor,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TENOR, isBold, color)
                #self.addItemtoTable2(self.table,movement,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID, isBold, color)    
#             self.addItemtoTable2(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_AMOUNT, isBold, color)
            elif(isinstance(movement, CorporateEvent)):
                self.addItemtoTable2(self.table,"CORP EVENT",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE, isBold, color)
                self.addItemtoTable2(self.table,"CASH DIVIDEND",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE, isBold, color)
                self.addItemtoTable2(self.table,movement.asset.name,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME, isBold, color)
                self.addItemtoTable2(self.table,movement.paymentDate,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE, isBold, color)
                self.addItemtoTable2(self.table,movement.grossAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.netAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT, isBold, color)
            elif(isinstance(movement, CashMovement)):
                self.addItemtoTable2(self.table,"MOVEMENT",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE, isBold, color)
                self.addItemtoTable2(self.table,"CASH",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE, isBold, color)
                self.addItemtoTable2(self.table,"MXN",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME, isBold, color)
                self.addItemtoTable2(self.table,movement.inOut,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DIRECTION, isBold, color)
                self.addItemtoTable2(self.table,movement.movementDate,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE, isBold, color)
                self.addItemtoTable2(self.table,movement.amount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.amount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT, isBold, color)
            #HiddenID
            self.addItemtoTable2(self.table,self.row,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_HIDDEN_ID, isBold)
            self.row += 1
            

    def renderTableForRS(self, tableList):
        isBold = False
        for listItem in tableList:
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DIRECTION, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_QUANTITY, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_PRICE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_RATE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_PERCENTAGE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMISSION_IVA_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TENOR, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_CUSTODY_NAME, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMENT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EXTERNAL_ID, isBold)
            self.row += 1
    
    def doImport(self):
        index = self.table.item(self.table.currentRow(), Constant.CONST_COLUMN_IMPORT_MOVEMENT_HIDDEN_ID).text()
        operation = self.imLO.movementList[int(index)]
        print (operation.externalID)
        if(isinstance(operation, Movement)):
            rs = DaoMovement.getMovementsByExternalID(operation.externalID)
            if len(rs) == 0:
                newID = DaoMovement.insertMovement(operation)
                print("ADD externalID " + str(operation.externalID) + " newID: " + str(newID))
            else:
                print("CANNOT ADD externalID " + str(operation.externalID))
        elif(isinstance(operation, CorporateEvent)):
            rs = DaoCorporateEvent.getCorporateEventByExternalID(operation.externalID)
            if len(rs) == 0:
                newID = DaoCorporateEvent.insert(operation)
                print(newID)
                print("ADD externalID " + str(operation.externalID) + " newID: " + str(newID))
            else:
                print("CANNOT ADD externalID " + str(operation.externalID))
        elif(isinstance(operation, CashMovement)):
            rs = DaoCashMovement.getCashMovementsByExternalID(operation.externalID)
            if len(rs) == 0:
                newID = DaoCashMovement.insert(operation)
                print("ADD externalID " + str(operation.externalID) + " newID: " + str(newID))
            else:
                print("CANNOT ADD externalID " + str(operation.externalID))
        
    def doDelete(self):
        movementOID = self.table.item(self.table.currentRow(), Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID).text()
        movementType = self.table.item(self.table.currentRow(), Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE).text()
        movementSubType = self.table.item(self.table.currentRow(), Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE).text()
        print(movementOID)
        if(movementType == 'MOVEMENT' and movementSubType == 'TRX'):
            result = DaoMovement.deleteMovement(movementOID)
            print (result)
        elif(movementType == 'MOVEMENT' and movementSubType == 'CASH'):
            result = DaoCashMovement.deleteCashMovement(movementOID)
            print (result)
        elif(movementType == 'CORP EVENT' and movementSubType == 'CASH DIVIDEND'):
            result = DaoCorporateEvent.deleteCorporateEvent(movementOID)
            print (result)