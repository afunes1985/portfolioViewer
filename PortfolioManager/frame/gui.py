'''
Created on Feb 19, 2017

@author: afunes
'''
import datetime

from PySide import QtGui
from PySide.QtCore import QRect
from PySide.QtGui import QTableWidgetItem, QTableWidget

from engine.engine import Engine
from frame.movementEditor import MovementEditor
from modelClass.constant import Constant


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

