'''
Created on 5 jun. 2017

@author: afunes
'''
from datetime import date, datetime

from PySide import QtGui
from PySide.QtGui import QLabel, QSizePolicy, QDateEdit, QPushButton

from core.cache import Singleton


class MovementFilterWidget(QtGui.QWidget):
    def __init__(self):      
        super(MovementFilterWidget, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        #lblFromDate
        self.lblFromDate = QLabel("From Date")
        self.lblFromDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.lblFromDate, 1, 0)
        #dateFromDate
        self.dateFromDate = QDateEdit(self)
        self.dateFromDate.setDisplayFormat("dd-MM-yyyy")
        self.dateFromDate.setDate(date(2001, 7, 14))
        self.dateFromDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.dateFromDate, 1, 1)
        #lblToDate
        self.lblToDate = QLabel("To Date")
        self.lblToDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.lblToDate, 2, 0)
        #dateToDate
        self.dateToDate = QDateEdit(self)
        self.dateToDate.setDisplayFormat("dd-MM-yyyy")
        self.dateToDate.setDate(datetime.now())
        self.dateToDate.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.dateToDate, 2, 1)
        #btnSubmit
        self.btnSubmit = QPushButton("Submit", self)
        self.btnSubmit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.btnSubmit)
        self.setFixedSize(190, 100) 
        self.initListener() 
    
    def initListener(self):
        self.btnSubmit.clicked.connect(self.doSubmit)
    
    def doSubmit(self):
        from core.mainEngine import MainEngine
        mainEngine = Singleton(MainEngine)
        mainEngine.refreshAll((self.dateFromDate.date()).toPython(),(self.dateToDate.date()).toPython())
        
