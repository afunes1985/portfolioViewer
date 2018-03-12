'''
Created on 11 MAR. 2018

@author: afunes
'''
from datetime import date

from PySide import QtGui
from PySide.QtCore import QDate
from PySide.QtGui import QLabel, QSizePolicy, QDateEdit, QPushButton, QComboBox

from dao.dao import DaoReportMovement


class ReportMovementFilter(QtGui.QWidget):
    def __init__(self, parent):      
        super(ReportMovementFilter, self).__init__()
        self.parent = parent
        self.layout = QtGui.QGridLayout(self)
        #lblFromDate
        self.lblFromDate = QLabel("From Date")
        self.lblFromDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.lblFromDate, 1, 0)
        #dateFromDate
        self.dateFromDate = QDateEdit(self)
        self.dateFromDate.setDisplayFormat("dd-MM-yyyy")
        self.dateFromDate.setDate(date(2017, 1, 1))
        self.dateFromDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.dateFromDate, 1, 1)
        #lblToDate
        self.lblToDate = QLabel("To Date")
        self.lblToDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.lblToDate, 2, 0)
        #dateToDate
        self.dateToDate = QDateEdit(self)
        self.dateToDate.setDisplayFormat("dd-MM-yyyy")
        self.dateToDate.setDate(QDate.currentDate())
        self.dateToDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.dateToDate, 2, 1)
        #lblMovementType
        self.lblMovementType = QLabel("Movement Type")
        self.layout.addWidget(self.lblMovementType, 3, 0)
        #cmdMovementType
        self.cmdMovementType = QComboBox(self)
        self.cmdMovementType.addItems(DaoReportMovement.getMovementType())
        self.layout.addWidget(self.cmdMovementType, 3, 1)
        #lblAssetName
        self.lblAssetName = QLabel("Asset Name")
        self.layout.addWidget(self.lblAssetName, 4, 0)
        #cmdAssetName
        self.cmdAssetName = QComboBox(self)
        self.cmdAssetName.addItems(DaoReportMovement.getAssetNames())
        self.layout.addWidget(self.cmdAssetName, 4, 1)
        #btnSubmit
        self.btnSubmit = QPushButton("Submit", self)
        self.btnSubmit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.btnSubmit)
        self.setFixedSize(190, 150) 
        self.initListener() 
    
    def initListener(self):
        self.btnSubmit.clicked.connect(self.doSubmit)
    
    def doSubmit(self):
        fromDate = (self.dateFromDate.date()).toString("yyyy-M-dd")
        toDate = (self.dateToDate.date()).toString("yyyy-M-dd")
        movementType = self.cmdMovementType.currentText()
        assetName = self.cmdAssetName.currentText()
        self.parent.doSubmit(fromDate, toDate, movementType, assetName)
        
