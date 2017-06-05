'''
Created on 15 may. 2017

@author: afunes
'''
from PySide import QtGui
from PySide.QtGui import QTableWidgetItem


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