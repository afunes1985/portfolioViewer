'''
Created on May 3, 2017

@author: afunes
'''
from PySide import QtGui
from PySide.QtGui import QTableWidgetItem

from frame.MainWidget import MainWidget
from frame.MovementEditor import MovementEditor
from modelClass.corporateEvent import CorporateEvent
from frame.CorporateEventEditor import CorporateEventEditor

class MainWindow(QtGui.QMainWindow):
    _instance = None
    mainWidget = None
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Portfolio Viewer')
        self.resize(1200, 800)
        self.createMenu()
        self.setCentralWidget(self.createMainWidget()) 
        self.show()
         
    def createMainWidget(self):
        self.mainWidget = MainWidget()
        return self.mainWidget
        
    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&Add")
        self.actionOpenMovementEditor = QtGui.QAction("&Add movement", self, checkable=True,
            shortcut="Ctrl+M", statusTip="Add movement",
            triggered=self.openMovementEditor)
        self.fileMenu.addAction(self.actionOpenMovementEditor)
        self.actionOpenCorporateEventEditor = QtGui.QAction("&Add corporate event", self, checkable=True,
            shortcut="Ctrl+C", statusTip="Add movement",
            triggered=self.openCorporateEventEditor)
        self.fileMenu.addAction(self.actionOpenCorporateEventEditor)

    def renderSubtotal(self, positionDict, assetType ,isSIC):
        self.mainWidget.renderSubtotal(positionDict, assetType, isSIC)
    
    def renderPositions(self, positionDict, assetType ,isSIC):  
        self.mainWidget.renderPositions(positionDict, assetType, isSIC) 
        
    def renderSummary(self, summaryDict):  
        self.mainWidget.renderSummary(summaryDict)     
    
    def paintEntireRow(self, row):
        for r in range(self.mainWidget.positionTableWidget.columnCount()+1):
            emptyCell = QTableWidgetItem()
            emptyCell.setBackground(QtGui.QColor(204,204,204))
            self.mainWidget.positionTableWidget.setItem(row, r, emptyCell)
            
    def openMovementEditor(self):
        self.movementEditor = MovementEditor()
        self.movementEditor.show()
    
    def openCorporateEventEditor(self):
        self.corporateEditor = CorporateEventEditor()
        self.corporateEditor.show()
    
    def clearTable(self):
        self.mainWidget.clearTables()
