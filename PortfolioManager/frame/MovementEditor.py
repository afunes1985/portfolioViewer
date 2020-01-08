'''
Created on May 2, 2017

@author: afunes
'''
import datetime

from PySide import QtGui, QtCore
from PySide.QtCore import SIGNAL, QRect
from PySide.QtGui import QWidget, QLabel, QComboBox, QCheckBox, QLineEdit, \
    QDoubleValidator, QDateEdit, QIntValidator, QPushButton

from dao.dao import DaoAsset, DaoMovement, DaoCustody
from core.constant import Constant
from modelClass.movement import Movement


class MovementEditor(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(QRect(100, 100, 400, 200))
        self.layout = QtGui.QGridLayout(self)
        #lblAssetType
        self.lblAssetType = QLabel("Asset Type")
        self.layout.addWidget(self.lblAssetType, 0, 0)
        #cmdAssetType
        self.cmdAssetType = QComboBox(self)
        self.cmdAssetType.addItems(DaoAsset().getAssetTypes())
        self.layout.addWidget(self.cmdAssetType, 0, 1)
        #lblAssetName
        self.lblAssetName = QLabel("Asset Name")
        self.layout.addWidget(self.lblAssetName, 1, 0)
        #cmdAssetName
        self.cmdAssetName = QComboBox(self)
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
        #lblBuySell
        self.lblBuySell = QLabel("Buy Sell")
        self.layout.addWidget(self.lblBuySell, 3, 0)
        #cmdBuySell
        self.cmdBuySell = QComboBox(self)
        self.cmdBuySell.addItem("BUY")
        self.cmdBuySell.addItem("SELL")
        self.layout.addWidget(self.cmdBuySell, 3, 1)
        #lblByAmount
        self.lblByAmount = QLabel("By Amount")
        self.layout.addWidget(self.lblByAmount, 4, 0)
        #chkByAmount
        self.chkByAmount = QCheckBox(self)
        self.layout.addWidget(self.chkByAmount, 4, 1)
        #lblGrossAmount
        self.lblGrossAmount = QLabel("Gross Amount")
        self.layout.addWidget(self.lblGrossAmount, 5, 0)
        #txtGrossAmount
        self.txtGrossAmount = QLineEdit(self)
        self.txtGrossAmount.setValidator(QDoubleValidator(0, 99999999, 6, self))
        self.layout.addWidget(self.txtGrossAmount, 5, 1)
        #lblAcquisitionDate
        self.lblAcquisitionDate = QLabel("Acquisition Date")
        self.layout.addWidget(self.lblAcquisitionDate, 6, 0)
        #cmdAcquisitionDate
        self.dateAcquisitionDate = QDateEdit(self)
        self.dateAcquisitionDate.setDisplayFormat("dd-MM-yyyy")
        self.dateAcquisitionDate.setDate(datetime.datetime.now())
        self.layout.addWidget(self.dateAcquisitionDate, 6, 1)
        #lblQuantity
        self.lblQuantity = QLabel("Quantity")
        self.layout.addWidget(self.lblQuantity, 7, 0)
        #txtQuantity
        self.txtQuantity = QLineEdit(self)
        self.txtQuantity.setValidator(QIntValidator(0, 1000000000, self))
        self.layout.addWidget(self.txtQuantity, 7, 1)
        #lblPrice
        self.lblPrice = QLabel("Price")
        self.layout.addWidget(self.lblPrice, 8, 0)
        #txtPrice
        self.txtPrice = QLineEdit(self)
        self.txtPrice.setValidator(QDoubleValidator(0, 99999999, 6, self))
        self.layout.addWidget(self.txtPrice, 8, 1)
        #lblRate
        self.lblRate = QLabel("Rate")
        self.layout.addWidget(self.lblRate, 9, 0)
        #txtRate
        self.txtRate = QLineEdit(self)
        self.txtRate.setValidator(QDoubleValidator(0, 99999999, 4, self))
        self.txtRate.setEnabled(0)
        self.layout.addWidget(self.txtRate, 9, 1)
        #lblNetAmount
        self.lblNetAmount = QLabel("Net Amount")
        self.layout.addWidget(self.lblNetAmount, 10, 0)
        #txtNetAmount
        self.txtNetAmount = QLineEdit(self)
        self.txtNetAmount.setEnabled(0)
        self.txtNetAmount.setValidator(QDoubleValidator(0, 99999999, 6, self))
        self.layout.addWidget(self.txtNetAmount, 10, 1)
        #lblCommissionPercentage
        self.lblCommissionPercentage = QLabel("Commission Percentage")
        self.layout.addWidget(self.lblCommissionPercentage, 11, 0)
        #txtCommissionPercentage
        self.txtCommissionPercentage = QLineEdit(self)
        self.txtCommissionPercentage.setValidator(QDoubleValidator(0, 9999999, 6, self))
        self.layout.addWidget(self.txtCommissionPercentage, 11, 1)
        #lblCommissionAmount
        self.lblCommissionAmount = QLabel("Commission Amount")
        self.layout.addWidget(self.lblCommissionAmount, 12, 0)
        #txtCommissionAmmount
        self.txtCommissionAmount = QLineEdit(self)
        self.txtCommissionAmount.setEnabled(0)
        self.txtCommissionAmount.setValidator(QDoubleValidator(0, 9999999, 6, self))
        self.layout.addWidget(self.txtCommissionAmount, 12, 1)
        #lblCommissionAmount
        self.lblCommissionVATAmount = QLabel("Commission VAT Amount")
        self.layout.addWidget(self.lblCommissionVATAmount, 13, 0)
        #txtCommissionAmmount
        self.txtCommissionVATAmount = QLineEdit(self)
        self.txtCommissionVATAmount.setEnabled(0)
        self.txtCommissionVATAmount.setValidator(QDoubleValidator(0, 9999999, 6, self))
        self.layout.addWidget(self.txtCommissionVATAmount, 13, 1)
        #lblTenor
        self.lblTenor = QLabel("Tenor")
        self.layout.addWidget(self.lblTenor, 14, 0)
        #txtTenor
        self.txtTenor = QLineEdit(self)
        self.txtTenor.setEnabled(0)
        self.txtTenor.setValidator(QDoubleValidator(0, 9999999, 0, self))
        self.layout.addWidget(self.txtTenor, 14, 1)
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
        self.cmdBuySell.connect(self.cmdBuySell, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.calculateNetAmount) 
        self.chkByAmount.connect(self.chkByAmount, QtCore.SIGNAL("stateChanged(int)"), self.configEditorByAmount) 
        self.txtGrossAmount.connect(self.txtGrossAmount,SIGNAL("editingFinished()"),self.calculatePrice) 
        self.cmdAssetType.connect(self.cmdAssetType, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.configEditorByAssetType) 
        self.txtQuantity.connect(self.txtQuantity,SIGNAL("textChanged(QString)"),self.calculateGrossAmount) 
        self.txtQuantity.connect(self.txtQuantity,SIGNAL("textChanged(QString)"),self.calculatePrice) 
        self.txtPrice.connect(self.txtPrice,SIGNAL("textChanged(QString)"),self.calculateGrossAmount) 
        self.cmdAssetName.connect(self.cmdAssetName,SIGNAL("currentIndexChanged(const QString&)"),self.setDefaultCustody) 
        self.txtCommissionPercentage.connect(self.txtCommissionPercentage,SIGNAL("textChanged(QString)"),self.calculateCommission) 
        self.btnAdd.clicked.connect(self.addMovement)
        self.btnClear.clicked.connect(self.clearEditor)
         
    def addMovement(self):
        buySell = self.cmdBuySell.currentText()
        assetOID = self.cmdAssetName.itemData(self.cmdAssetName.currentIndex())
        custodyOID = self.cmbCustody.itemData(self.cmbCustody.currentIndex())
        acquisitionDate = self.dateAcquisitionDate.date()
        quantity = self.txtQuantity.text()
        if self.cmdAssetType.currentText() == 'BOND':
            rate = self.txtRate.text();
            if self.txtTenor.text() == '': 
                tenor = None 
            else: 
                tenor = self.txtTenor.text()
            maturityDate = acquisitionDate.toPython() + datetime.timedelta(days = int(tenor))
        else:
            rate = None;
            maturityDate = None
            tenor = None
        price = self.txtPrice.text()
        grossAmount = self.txtGrossAmount.text()
        netAmount = self.txtNetAmount.text()
        commissionPercentage = self.txtCommissionPercentage.text()
        commissionAmount = self.txtCommissionAmount.text()
        commissionVATAmount = self.txtCommissionVATAmount.text()
        
        movement = Movement(None)
        movement.setAttr(None, assetOID, buySell, (acquisitionDate).toPython(), 
                         quantity, price, rate, grossAmount, 
                         netAmount, commissionPercentage, commissionAmount, commissionVATAmount, 
                         tenor, custodyOID, maturityDate, None, None )
        DaoMovement.insertMovement(movement)
        self.clearEditor()
     
    def clearEditor(self):
        #self.cmdAssetType.set
        self.txtQuantity.setText(None)
        self.txtPrice.setText(None)
        self.txtGrossAmount.setText("0")
        self.txtNetAmount.setText("0")
        self.txtRate.setText("0")
        #configDefaultCommission
        if self.cmdAssetType.currentText() == 'EQUITY':
            self.txtCommissionPercentage.setText(str(Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE))
        else:
            self.txtCommissionPercentage.setText(str(Constant.CONST_DEF_OTHER_COMMISSION_PERCENTAGE))
        self.txtTenor.setText("")
        self.dateAcquisitionDate.setDate(datetime.datetime.now())
        self.configEditorByAmount()
        self.configEditorByAssetType()
         
    def setDefaultCustody(self):
        defaultCustodyID = DaoCustody().getDefaultCustody(self.cmdAssetName.currentText())
        for (row) in defaultCustodyID:
            self.cmbCustody.setCurrentIndex(self.cmbCustody.findData(row[0]))  
         
    def configEditorByAssetType(self):
        self.cmdAssetName.clear()
        #loadAssetNames
        assetNameList = DaoAsset().getAssetNames(self.cmdAssetType.currentText())
        for (assetName) in assetNameList:
            self.cmdAssetName.addItem(assetName[1], assetName[0]) 
        #setPriceOrRate    
        if self.cmdAssetType.currentText() == 'EQUITY' or self.cmdAssetType.currentText() == 'FUND':
            self.txtPrice.setEnabled(1)
            self.txtRate.setEnabled(0)
            self.txtRate.setText("0")
            self.txtTenor.setEnabled(0)
            self.txtTenor.setText(None)
        else:
            self.txtPrice.setEnabled(0)
            self.txtRate.setEnabled(1)
            self.txtPrice.setText("0")
            self.txtTenor.setEnabled(1)
            self.txtTenor.setText(None)
        #configDefaultCommission
        if self.cmdAssetType.currentText() == 'EQUITY':
            self.txtCommissionPercentage.setText(str(Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE))
        else:
            self.txtCommissionPercentage.setText(str(Constant.CONST_DEF_OTHER_COMMISSION_PERCENTAGE))
     
    def configEditorByAmount(self):
        if self.chkByAmount.isChecked():
            self.txtPrice.setEnabled(0)
            self.txtGrossAmount.setEnabled(1)
        else:
            self.txtPrice.setEnabled(1)
            self.txtGrossAmount.setEnabled(0)
     
    def calculateCommission(self):
        commissionPercentage = self.txtCommissionPercentage.text()
        grossAmount = self.txtGrossAmount.text() 
        if commissionPercentage >= 0:
            commissionAmount = float(grossAmount) * float(commissionPercentage)
            self.txtCommissionAmount.setText(str('{0:.6f}'.format(commissionAmount)))
            commissionVATAmount = commissionAmount * Constant.CONST_IVA_PERCENTAGE
            self.txtCommissionVATAmount.setText(str('{0:.6f}'.format(commissionVATAmount)))
            self.calculateNetAmount()
         
    def calculatePrice(self):
        quantity = self.txtQuantity.text()
        amount = self.txtGrossAmount.text()
        if (quantity is not u"" or None) and (amount is not u"" or None):
            self.txtPrice.setText(str('{0:.6f}'.format(float(amount) / float(quantity))))
         
    def calculateNetAmount(self):
        buySell = self.cmdBuySell.currentText()
        grossAmount = float(self.txtGrossAmount.text()) 
        commissionAmount = float(self.txtCommissionAmount.text())
        commissionVATAmount = float(self.txtCommissionVATAmount.text())
        if buySell == 'BUY':
            netAmount = grossAmount + commissionVATAmount + commissionAmount
        else:
            netAmount = grossAmount - commissionVATAmount - commissionAmount    
        self.txtNetAmount.setText(str(netAmount))
         
    def calculateGrossAmount(self):
        quantity = self.txtQuantity.text()
        price = self.txtPrice.text()
        if (not self.chkByAmount.isChecked()) and (quantity is not u"" or None) and (price is not u"" or None):
            self.txtGrossAmount.setText(str('{0:.6f}'.format(float(quantity) * float(price))))
        self.calculateCommission()
        