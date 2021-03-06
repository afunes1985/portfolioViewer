'''
Created on May 3, 2017

@author: afunes
'''
from PySide import QtGui
from PySide.QtGui import QTabWidget

from frame.CorporateEventEditor import CorporateEventEditor
from frame.CorporateEventPanel import CorporateEventPanel
from frame.ImportMovementPanel import ImportMovementPanel
from frame.MovementEditor import MovementEditor
from frame.PnLPanel import PnLPanel
from frame.PositionPanel import PositionPanel
from frame.ReportMovementPanel import ReportMovementPanel
from core.dumpexporter import DumpExporter


class MainWindow(QtGui.QMainWindow):
    _instance = None
    tabPanel = None
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Portfolio Viewer')
        self.resize(1300, 900)
        self.createMenu()
        self.setCentralWidget(self.createTabWidget()) 
        self.show()
         
    def createTabWidget(self):
        self.tabPanel = QTabWidget()
        self.tabPanel.addTab(self.createPositionPanel(), "Position")
        self.tabPanel.addTab(self.createCorporateEventPanel(), "Corporate Event")
        self.tabPanel.addTab(self.createPnLPanel(), "PnL")
        self.tabPanel.addTab(self.createReportMovementPanel(), "Report Movement")
        self.tabPanel.addTab(self.createImporterMovementPanel(), "Import Movement")
        return self.tabPanel
    
    def createCorporateEventPanel(self):
        self.corpEventPanel = CorporateEventPanel()
        return self.corpEventPanel
        
    def createPositionPanel(self):
        self.positionPanel = PositionPanel()
        return self.positionPanel
        
    def createPnLPanel(self):
        self.pnLPanel = PnLPanel()
        return self.pnLPanel
    
    def createReportMovementPanel(self):
        self.reportMovementPanel = ReportMovementPanel()
        return self.reportMovementPanel
    
    def createImporterMovementPanel(self):
        self.importerMovement = ImportMovementPanel()
        return self.importerMovement
    
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
        self.fileMenu = self.menuBar().addMenu("&Dump")
        self.actionExportDump = QtGui.QAction("&Export Dump", self, checkable=True,
            statusTip="Export Dumpt",
            triggered=self.exportAllDump)
        self.fileMenu.addAction(self.actionExportDump)

    def openMovementEditor(self):
        self.movementEditor = MovementEditor()
        self.movementEditor.show()
    
    def openCorporateEventEditor(self):
        self.corporateEditor = CorporateEventEditor()
        self.corporateEditor.show()
        
    def exportAllDump(self):
        DumpExporter.exportAllDump(self)
        
    def clearTable(self):
        self.positionPanel.clearTables()

    ################################### RENDERS #########################################

    def renderSubtotal(self, positionDict, assetType ,isSIC):
        self.positionPanel.renderSubtotal(positionDict, assetType, isSIC)
    
    def renderPositions(self, positionDict, assetType ,isSIC):  
        self.positionPanel.renderPositions(positionDict, assetType, isSIC) 
        
    def renderSummary(self, summaryDict):  
        self.positionPanel.renderSummary(summaryDict)   
    
    def renderCorpEvent(self, corporateEventPositionDictAsset):  
        self.corpEventPanel.renderCorpEvent(corporateEventPositionDictAsset) 
        
    def renderGeneralInfoPanel(self, usdMXNvalue):  
        self.positionPanel.renderGeneralInfoPanel(usdMXNvalue) 