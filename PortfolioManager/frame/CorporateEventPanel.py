'''
Created on Feb 19, 2017

@author: afunes
'''

from PySide import QtGui
from PySide.QtGui import QTreeWidget, \
    QTreeWidgetItem

class CorporateEventPanel(QtGui.QWidget):
    tableCorporateEvent = None
    rowCorporateEvent = 0
    columnListCorporateEvent = "Asset;Gross Amount;Net Amount;Payment Date".split(";");
    
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.clearTables()
        
    def clearTables(self):    
        self.row = 0
        self.createCorpEventTable()
        
    def createCorpEventTable(self):
        self.treeCorporateEvent = QTreeWidget()
        self.layout.addWidget(self.treeCorporateEvent, 2, 0, 3, 3)   
        
    def renderCorpEvent(self, corporateEventPositionDictAsset):   
        self.clearTables();
        self.treeCorporateEvent.setColumnCount(3)
        self.treeCorporateEvent.setHeaderLabels(self.columnListCorporateEvent)
        for key, cep in corporateEventPositionDictAsset.items():
            l1 = QTreeWidgetItem([key, str(cep.accGrossAmount), str(cep.accNetAmount)])
            for ce in cep.corporateEventList:
                l1_child = QTreeWidgetItem([None, str(ce.grossAmount), str(ce.netAmount),str(ce.paymentDate)])
                l1.addChild(l1_child)
                self.treeCorporateEvent.addTopLevelItem(l1)
