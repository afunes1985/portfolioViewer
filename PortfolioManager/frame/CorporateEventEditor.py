'''
Created on May 2, 2017

@author: afunes
'''
import datetime

from PySide import QtGui
from PySide.QtCore import SIGNAL, QRect
from PySide.QtGui import QWidget, QLabel, QComboBox, QLineEdit, \
    QDoubleValidator, QDateEdit, QPushButton

from dao.dao import DaoAsset, DaoCustody, DaoCorporateEventType
from modelClass.corporateEvent import CorporateEvent


class CorporateEventEditor(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(QRect(100, 100, 400, 200))
        self.layout = QtGui.QGridLayout(self)
        #lblCorporateEventType
        self.lblCorporateEventType = QLabel("Type")
        self.layout.addWidget(self.lblCorporateEventType, 0, 0)
        #cmbCorporateEventType
        self.cmbCorporateEventType = QComboBox(self)
        corporateEventTypeList = DaoCorporateEventType().getCorporateEventTypeList()
        for (corporateEventType) in corporateEventTypeList:
            self.cmbCorporateEventType.addItem(corporateEventType[1], corporateEventType[0])
        self.layout.addWidget(self.cmbCorporateEventType, 0, 1)
        #lblAssetName
        self.lblAssetName = QLabel("Asset Name")
        self.layout.addWidget(self.lblAssetName, 1, 0)
        #cmdAssetName
        self.cmdAssetName = QComboBox(self)
        assetNameList = DaoAsset().getAssetNames('EQUITY')
        for (assetName) in assetNameList:
            self.cmdAssetName.addItem(assetName[1], assetName[0]) 
        self.layout.addWidget(self.cmdAssetName, 1, 1)
        #lblCustody
        self.lblCustody = QLabel("Custody")
        self.layout.addWidget(self.lblCustody, 2, 0)
        #cmbCustody
        self.cmbCustody = QComboBox(self)
        custodyList = DaoCustody().getCustodyList()
        for (row) in custodyList:
            self.cmbCustody.addItem(row[1], row[0]) 
        self.layout.addWidget(self.cmbCustody, 2, 1)
        #lblGrossAmount
        self.lblGrossAmount = QLabel("Gross Amount")
        self.layout.addWidget(self.lblGrossAmount, 3, 0)
        #txtGrossAmount
        self.txtGrossAmount = QLineEdit(self)
        self.txtGrossAmount.setValidator(QDoubleValidator(0, 99999999, 6, self))
        self.layout.addWidget(self.txtGrossAmount, 3, 1)
        #lblPaymentDate
        self.lblPaymentDate = QLabel("Payment Date")
        self.layout.addWidget(self.lblPaymentDate, 4, 0)
        #cmbPaymentDate
        self.cmbPaymentDate = QDateEdit(self)
        self.cmbPaymentDate.setDisplayFormat("dd-MM-yyyy")
        self.cmbPaymentDate.setDate(datetime.datetime.now())
        self.layout.addWidget(self.cmbPaymentDate, 4, 1)
        #btnAdd
        self.btnAdd = QPushButton("Add", self)
        self.layout.addWidget(self.btnAdd)
        #btnClear
        self.btnClear = QPushButton("Clear", self)
        self.layout.addWidget(self.btnClear)
        #clearEditor
        self.clearEditor()
        self.initListener()
     
    def initListener(self):
        self.cmdAssetName.connect(self.cmdAssetName,SIGNAL("currentIndexChanged(const QString&)"),self.setDefaultCustody) 
        self.btnAdd.clicked.connect(self.addCorporateEvent)
        self.btnClear.clicked.connect(self.clearEditor)
         
    def addCorporateEvent(self):
        corporateEvent = CorporateEvent(None)
        corporateEvent.assetOID = self.cmdAssetName.itemData(self.cmdAssetName.currentIndex())
        corporateEvent.corporateEventTypeOID = self.cmbCorporateEventType.itemData(self.cmbCorporateEventType.currentIndex())
        corporateEvent.custody = self.cmbCustody.itemData(self.cmbCustody.currentIndex())
        corporateEvent.paymentDate = (self.cmbPaymentDate.date()).toString("yyyy-M-dd")
        corporateEvent.grossAmount = self.txtGrossAmount.text()
        DaoCorporateEventType().insert(corporateEvent)
        self.clearEditor()
     
    def clearEditor(self):
        self.txtGrossAmount.setText("0")
        self.cmbPaymentDate.setDate(datetime.datetime.now())
         
    def setDefaultCustody(self):
        defaultCustodyID = DaoCustody().getDefaultCustody(self.cmdAssetName.currentText())
        for (row) in defaultCustodyID:
            self.cmbCustody.setCurrentIndex(self.cmbCustody.findData(row[0]))  
         
        