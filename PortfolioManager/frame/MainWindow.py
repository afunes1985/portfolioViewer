'''
Created on May 3, 2017

@author: afunes
'''
from PySide import QtGui
from PySide.QtGui import QTableWidgetItem, QTabWidget

from frame.CorporateEventEditor import CorporateEventEditor
from frame.CorporateEventPanel import CorporateEventPanel
from frame.MainPanel import MainPanel
from frame.MovementEditor import MovementEditor


class MainWindow(QtGui.QMainWindow):
    _instance = None
    mainPanel = None
    corpEventPanel = None
    tabPanel = None
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Portfolio Viewer')
        self.resize(1300, 800)
        self.createMenu()
        self.setCentralWidget(self.createTabWidget()) 
        self.show()
         
    def createTabWidget(self):
        self.tabPanel = QTabWidget()
        self.tabPanel.addTab(self.createMainWidget(), "Main")
        self.tabPanel.addTab(self.createCorporateEventPanel(), "Corporate Event")
        return self.tabPanel
    
    def createCorporateEventPanel(self):
        self.corpEventPanel = CorporateEventPanel()
        return self.corpEventPanel
        
    def createMainWidget(self):
        self.mainPanel = MainPanel()
        return self.mainPanel
        
    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu("&Add")
        self.actionOpenMovementEditor = QtGui.QAction("&Add movement", self, checkable=True,
            shortcut="Ctrl+M", statusTip="Add movement",
            triggered=self.openMovementEditor)
        self.fileMenu.addAction(self.actionOpenMovementEditor)
        self.actionOpenCorporateEventEditor = QtGui.QAction("&Add corporate event", self, checkable=True,
            shortcut="Ctrl+E", statusTip="Add movement",
            triggered=self.openCorporateEventEditor)
        self.fileMenu.addAction(self.actionOpenCorporateEventEditor)

    
    def paintEntireRow(self, row):
        for r in range(self.mainPanel.positionTableWidget.columnCount()+1):
            emptyCell = QTableWidgetItem()
            emptyCell.setBackground(QtGui.QColor(204,204,204))
            self.mainPanel.positionTableWidget.setItem(row, r, emptyCell)
            
    def openMovementEditor(self):
        self.movementEditor = MovementEditor()
        self.movementEditor.show()
    
    def openCorporateEventEditor(self):
        self.corporateEditor = CorporateEventEditor()
        self.corporateEditor.show()
    
    def clearTable(self):
        self.mainPanel.clearTables()

    ################################### RENDERS #########################################

    def renderSubtotal(self, positionDict, assetType ,isSIC):
        self.mainPanel.renderSubtotal(positionDict, assetType, isSIC)
    
    def renderPositions(self, positionDict, assetType ,isSIC):  
        self.mainPanel.renderPositions(positionDict, assetType, isSIC) 
        
    def renderSummary(self, summaryDict):  
        self.mainPanel.renderSummary(summaryDict)   
    
    def renderCorpEvent(self, corpEventList):  
        self.corpEventPanel.renderCorpEvent(corpEventList) 