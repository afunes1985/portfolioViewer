'''
Created on 15 may. 2017

@author: afunes
'''
from datetime import datetime
from decimal import Decimal

from PySide import QtGui
from PySide.QtGui import QTableWidgetItem


class QTableWidgetItemStringPlusMinus(QTableWidgetItem):
    def __init__(self, value, bold):
        super(self.__class__, self).__init__(value)
        self.setTextAlignment(0x0080) 
        font = self.font()
        font.setBold(bold)
        self.setFont(font)
        if(value is not None and value[0]!='-'):
            self.setBackground(QtGui.QColor(102,204,51))
        elif(value is not None):
            self.setBackground(QtGui.QColor(255,000,51))

class QTableWidgetItemString(QTableWidgetItem):
    def __init__(self, value, bold):
        super(self.__class__, self).__init__(value)
        self.setTextAlignment(0x0080) 
        font = self.font()
        font.setBold(bold)
        self.setFont(font)
          
class QTableWidgetItemDecimal(QTableWidgetItem):
    def __init__(self, value, bold):
        super(self.__class__, self).__init__(str('{0:.2f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080) 
        font = self.font()
        font.setBold(bold)
        self.setFont(font)

class QTableWidgetItem6Decimal(QTableWidgetItem):
    def __init__(self, value, bold):
        super(self.__class__, self).__init__(str('{0:.6f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080)
        font = self.font()
        font.setBold(bold)
        self.setFont(font)        

class QTableWidgetItemDuoDecimal(QTableWidgetItem):
    def __init__(self, value1, value2):
        if(value2 == 0):
            value = str('{0:.2f}'.format(value1))
        elif (value1 is not None):    
            value = str('{0:.2f}'.format(value1)) + '(' + str('{0:.2f}'.format(value2)) + ')'
        else:
            value = None
        super(self.__class__, self).__init__(str(value))
        self.setTextAlignment(0x0002 | 0x0080)

class QTableWidgetItemDecimalColor(QTableWidgetItem):
    def __init__(self, value, bold):
        super(self.__class__, self).__init__(str('{0:.2f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080) 
        if(value < 0):  
            self.setBackground(QtGui.QColor(255,000,51))
        else:
            self.setBackground(QtGui.QColor(102,204,51))
        font = self.font()
        font.setBold(bold)
        self.setFont(font) 

class QTableWidgetItemDuoInt(QTableWidgetItem):
    def __init__(self, value1, value2):
        if(value2 == 0):
            value = str('{0:.0f}'.format(value1))
        elif (value1 != 0):    
            value = str('{0:.0f}'.format(value1)) + '(' + str('{0:.0f}'.format(value2)) + ')'
        else:
            value = ''
        super(self.__class__, self).__init__(str(value))
        self.setTextAlignment(0x0002 | 0x0080)

class QTableWidgetItemInt(QTableWidgetItem):
    def __init__(self, value, bold):
        super(self.__class__, self).__init__(str('{0:.0f}'.format(value)))
        self.setTextAlignment(0x0002 | 0x0080) 
        font = self.font()
        font.setBold(bold)
        self.setFont(font)
        
class PanelWithTable(QtGui.QWidget):
    
    def addItemtoTable(self, table, listItem, row, column, isBold):
        self.addItemtoTable2(table, listItem[column], row, column, isBold)
        
    def addItemtoTable2(self, table, cellValue, row, column, isBold, backgroundColor=None):
        if isinstance(cellValue, basestring):
            Item = QTableWidgetItemString(cellValue, isBold)
        elif isinstance(cellValue, datetime):
            Item = QTableWidgetItemString(cellValue.strftime("%Y-%m-%d"), isBold)
        elif isinstance(cellValue, (int, long)):
            Item = QTableWidgetItemInt(cellValue, isBold)
        elif isinstance(cellValue, (float, Decimal)):
            if float(cellValue).is_integer():
                Item = QTableWidgetItemInt(cellValue, isBold)
            else:
                Item = QTableWidgetItem6Decimal(cellValue, isBold)
        elif cellValue is None:
            Item = QTableWidgetItemString(cellValue, isBold)
        if (backgroundColor is not None):
            Item.setBackground(backgroundColor)
        table.setItem(row,column,Item)
        
    def getCurrentRowValue(self, rowNum):
        value = self.table.item(self.table.currentRow(), rowNum)
        if (value is not None):
            return value.text()
        else:
            return None