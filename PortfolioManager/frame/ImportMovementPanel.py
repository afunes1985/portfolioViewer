'''
Created on 15 jun. 2018

@author: afunes
'''
from PySide import QtGui, QtCore
from PySide.QtGui import QTableWidget, QPushButton, QSizePolicy, \
    QMessageBox

from dao.dao import DaoMovement, DaoCorporateEvent, DaoCashMovement, DaoTax
from dataImport.importMovementFromPDF import MovementImporter
from engine.engine import Engine
from frame.ImportMovementFilter import ImportMovementFilter
from frame.ReportMovementPanel import ReportMovementPanel
from frame.framework import PanelWithTable
from modelClass.cashMovement import CashMovement
from core.constant import Constant
from modelClass.corporateEvent import CorporateEvent
from modelClass.movement import Movement


class ImportMovementPanel(PanelWithTable):
    
    columnList = ReportMovementPanel.columnList
    
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
        self.table.doubleClicked.connect(self.doImportOrDelete)
        self.table.resizeRowsToContents()
        self.table.setFixedSize(1100, 900) 
        return self.table 
    
    def doSubmit(self, filePath, assetName):
        self.imLO = MovementImporter().getMovementList(filePath, assetName) 
        self.table.setSortingEnabled(False) 
        self.table.clearContents()
        if (self.imLO.movementList is not None):
            countRowTable = len(self.imLO.movementList)
            self.table.setRowCount(countRowTable)
            self.renderTableForObject(self.imLO.movementList)
            imLO2 = Engine.getReportMovementList(self.imLO.fromDate, self.imLO.toDate, 'ALL', assetName, self.imLO.custodyName)
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
            self.addItemtoTable2(self.table,movement.OID,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID, isBold, color)
            self.addItemtoTable2(self.table,movement.externalID,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EXTERNAL_ID, isBold, color)
            self.addItemtoTable2(self.table,movement.comment,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMENT, isBold, color)
            self.addItemtoTable2(self.table,movement.custody.name,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_CUSTODY_NAME, isBold, color)
            self.addItemtoTable2(self.table,movement.getMovementType(),self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE, isBold, color)
            self.addItemtoTable2(self.table,movement.getMovementSubType(),self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE, isBold, color)
            if(movement.asset is not None):
                self.addItemtoTable2(self.table,movement.asset.name,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_ASSET_NAME, isBold, color)
            if (movement.tax is not None):
                    self.addItemtoTable2(self.table,"NEW",self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID, isBold, color)    
                    self.addItemtoTable2(self.table,movement.tax.taxAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_AMOUNT, isBold, color)
            if(isinstance(movement, Movement)):
                self.addItemtoTable2(self.table,movement.buySell,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DIRECTION, isBold, color)
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
                self.addItemtoTable2(self.table,movement.maturityDate,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_MATURITY_DATE, isBold, color)
            elif(isinstance(movement, CorporateEvent)):
                self.addItemtoTable2(self.table,movement.paymentDate,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_DATE, isBold, color)
                self.addItemtoTable2(self.table,movement.grossAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_GROSS_AMOUNT, isBold, color)
                self.addItemtoTable2(self.table,movement.netAmount,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_NET_AMOUNT, isBold, color)
            elif(isinstance(movement, CashMovement)):
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
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_MATURITY_DATE, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_CUSTODY_NAME, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_AMOUNT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_COMMENT, isBold)
            self.addItemtoTable(self.table,listItem,self.row,Constant.CONST_COLUMN_IMPORT_MOVEMENT_EXTERNAL_ID, isBold)
            self.row += 1
    
    def doImportOrDelete(self):
        index = self.getCurrentRowValue(Constant.CONST_COLUMN_IMPORT_MOVEMENT_HIDDEN_ID)
        if (index is not None): 
            self.doImport()
        else:
            self.doDelete()
            
    def doImport(self):
        index = self.getCurrentRowValue(Constant.CONST_COLUMN_IMPORT_MOVEMENT_HIDDEN_ID)
        if (index is not None): 
            operation = self.imLO.movementList[int(index)]
            print (operation.externalID)
            newID = None
            taxNewID = None
            if(isinstance(operation, Movement)):
                rs = DaoMovement.getMovementsByExternalID(operation.externalID)
                if len(rs) == 0:
                    if (operation.OID == "NEW"):
                        newID = DaoMovement.insertMovement(operation)
                if (operation.tax is not None and operation.tax.OID == "NEW"):
                    rs = DaoTax.getTaxByExternalID(operation.tax.externalID);
                    if len(rs) == 0:
                        taxNewID = DaoTax.insert(operation.tax)
            elif(isinstance(operation, CorporateEvent)):
                rs = DaoCorporateEvent.getCorporateEventByExternalID(operation.externalID)
                if len(rs) == 0:
                    newID = DaoCorporateEvent.insert(operation)
                    print(newID)
                    if (operation.tax is not None):
                        rs = DaoTax.getTaxByExternalID(operation.tax.externalID);
                        if len(rs) == 0:
                            operation.tax.originOID = newID
                            taxNewID = DaoTax.insert(operation.tax)
            elif(isinstance(operation, CashMovement)):
                rs = DaoCashMovement.getCashMovementsByExternalID(operation.externalID)
                if len(rs) == 0:
                    newID = DaoCashMovement.insert(operation)
            box = QMessageBox()
            box.setWindowTitle('ADD')
            if (newID is None and taxNewID is None):
                box.setText("CANNOT ADD externalID "+ operation.externalID)
            else:
                if(newID is not None and taxNewID is not None):
                    box.setText("INSERTED MOVEMENT " + operation.externalID + " NEWID: " + str(newID) + " NEWTAXID: "+ str(taxNewID))
                elif(newID is not None and taxNewID is None):
                    box.setText("INSERTED MOVEMENT " + operation.externalID + " NEWID: " + str(newID))
                else:
                    box.setText("INSERTED TAX " + operation.tax.externalID + " NEWTAXID: " + str(taxNewID))
            box.exec_()
            
    def doDelete(self):
        movementOID = self.getCurrentRowValue(Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_ID)
        movementType = self.getCurrentRowValue(Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_TYPE) 
        movementSubType = self.getCurrentRowValue(Constant.CONST_COLUMN_IMPORT_MOVEMENT_EVENT_SUB_TYPE) 
        taxOID = self.getCurrentRowValue(Constant.CONST_COLUMN_IMPORT_MOVEMENT_TAX_ID)
        result = 0
        if(movementType == Constant.CONST_MOVEMENT_TYPE and movementSubType == Constant.CONST_MOVEMENT_SUB_TYPE):
            result = DaoMovement.deleteMovement(movementOID)
            print (result)
        elif(movementType == Constant.CONST_MOVEMENT_TYPE and movementSubType == Constant.CONST_CASH_MOVEMENT_SUB_TYPE):
            result = DaoCashMovement.deleteCashMovement(movementOID)
            print (result)
        elif(movementType == Constant.CONST_CORP_EVENT_TYPE and movementSubType == Constant.CONST_CORP_EVENT_SUB_TYPE):
            if (taxOID):
                taxResult = DaoTax.deleteTax(taxOID)
            result = DaoCorporateEvent.deleteCorporateEvent(movementOID)
            print (result)
        box = QMessageBox()
        box.setWindowTitle('DELETED')
        if (result == 0):
            box.setText("CANNOT DELETE "+ movementType + "-" + movementSubType + "-" + movementOID)
        else:
            if(taxOID is None or taxOID == ""):
                box.setText(movementType + "-" + movementSubType + "-" + movementOID +": " + str(result) + " record(s) deleted")
            else:
                box.setText(movementType + "-" + movementSubType + "-" + movementOID +": " + str(result) + " record(s) deleted and taxID: " + taxOID + " " + str(taxResult) + " record(s) deleted")
        box.exec_()