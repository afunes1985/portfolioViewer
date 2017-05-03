'''
Created on Feb 19, 2017

@author: afunes
'''

from datetime import date
import datetime

from PySide import QtGui
from PySide.QtGui import QTableWidgetItem, QTableWidget, QLabel, QDateEdit, \
    QPushButton

from core.cache import Singleton, MainCache
from engine.engine import Engine


class QTableWidgetItemString(QTableWidgetItem):
    def __init__(self, value):
        super(QTableWidgetItemString, self).__init__(value)
        self.setTextAlignment(0x0080) 
          
class QTableWidgetItemDecimal(QTableWidgetItem):
    def __init__(self, value):
        super(QTableWidgetItemDecimal, self).__init__(str('{0:.2f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080)        

class QTableWidgetItemInt(QTableWidgetItem):
    def __init__(self, value):
        super(QTableWidgetItemInt, self).__init__(str('{0:.0f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080) 

class MainWidget(QtGui.QWidget):
    tableWidget = None
    def __init__(self): 
        super(MainWidget, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.layout.addWidget(MovementFilterWidget(), 1, 0)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(25)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels("Asset Name;Position;PPP;Market Price;Invested amount;Valuated amount;Tenor;Maturity Date;PNL;%PNL;%Portfolio".split(";"))
        #self.tableWidget.setSortingEnabled(True)  
        #self.tableWidget.sortItems(0)  
        #self.setCentralWidget(self.tableWidget)  
        self.layout.addWidget(self.tableWidget, 2, 0)     

class MovementFilterWidget(QtGui.QWidget):
    def __init__(self):      
        super(MovementFilterWidget, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        #lblFromDate
        self.lblFromDate = QLabel("From Date")
        self.layout.addWidget(self.lblFromDate, 1, 0)
        #dateFromDate
        self.dateFromDate = QDateEdit(self)
        self.dateFromDate.setDisplayFormat("dd-MM-yyyy")
        self.dateFromDate.setDate(date(2001, 7, 14))
        self.layout.addWidget(self.dateFromDate, 1, 1)
        #lblToDate
        self.lblToDate = QLabel("To Date")
        self.layout.addWidget(self.lblToDate, 2, 0)
        #dateToDate
        self.dateToDate = QDateEdit(self)
        self.dateToDate.setDisplayFormat("dd-MM-yyyy")
        self.dateToDate.setDate(date(2020, 7, 14))
        self.layout.addWidget(self.dateToDate, 2, 1)
        #btnSubmit
        self.btnSubmit = QPushButton("Submit", self)
        self.layout.addWidget(self.btnSubmit)
    
    def initListener(self):
        self.btnSubmit.clicked.connect(self.doSubmit)
    
    def doSubmit(self):
        Singleton(MainCache).positionDict = Engine.buildPositions(self.dateFromDate.date(),self.dateToDate.date())
