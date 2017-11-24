'''
Created on Feb 19, 2017

@author: afunes
'''

from PySide import QtGui
from PySide.QtGui import QTableWidget

from engine.engine import Engine
from frame.MovementFilterWidget import MovementFilterWidget
from frame.MovementView import MovementView
from frame.framework import QTableWidgetItemDecimal, \
    QTableWidgetItemDecimalColor, QTableWidgetItemString, QTableWidgetItemInt, \
    QTableWidgetItemDuoDecimal, QTableWidgetItemDuoInt, \
    QTableWidgetItemStringPlusMinus
from modelClass.constant import Constant


class MainPanel(QtGui.QWidget):
    positionTableWidget = None
    summaryTable = None
    movementFilterWidget = None
    row = 0
    summaryRow = 0
    positionColumnList = "Asset Name;Position;Unit Cost;Market Price;Change%;Invested amount;Valuated amount;Tenor;Maturity Date;Gross PNL;Net PNL;Gross%PNL;Net%PNL;Realized Pnl;%Portfolio;WeightedPNL%".split(";");
    summaryColumnList = "Custody;Asset type;Invested Amount;Valuated Amount;Net%PNL;Realized Pnl;%Portfolio;WeightedPNL%".split(";");
    def __init__(self): 
        super(self.__class__, self).__init__()
        self.layout = QtGui.QGridLayout(self)
        self.movementFilterWidget = MovementFilterWidget()
        self.layout.addWidget(self.movementFilterWidget, 1, 0)
        
    def clearTables(self):    
        self.row = 0
        self.summaryRow = 0
        self.createTable()
        self.createSummaryTable()
    
    def createSummaryTable(self):
        self.summaryTableWidget = QTableWidget()
        self.summaryTableWidget.setRowCount(6)
        self.summaryTableWidget.setColumnCount(len(self.summaryColumnList))
        self.summaryTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.summaryTableWidget.setHorizontalHeaderLabels(self.summaryColumnList)
        #self.summaryTableWidget.setSortingEnabled(True)  
        #self.summaryTableWidget.sortItems(0)  
        self.summaryTableWidget.resizeColumnsToContents()
        self.summaryTableWidget.resizeRowsToContents()
        self.summaryTableWidget.setFixedSize(700, 150) 
        self.layout.addWidget(self.summaryTableWidget, 1, 1)
        
    def createTable(self):
        self.positionTableWidget = QTableWidget()
        self.positionTableWidget.setRowCount(27)
        self.positionTableWidget.setColumnCount(len(self.positionColumnList) +1)
        self.positionTableWidget.setColumnHidden(Constant.CONST_COLUMN_POSITION_HIDDEN_ID, True)
        self.positionTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.positionTableWidget.setHorizontalHeaderLabels(self.positionColumnList)
        #self.positionTableWidget.setSortingEnabled(True)  
        #self.positionTableWidget.sortItems(0)  
        self.positionTableWidget.doubleClicked.connect(self.openMovementView)
        self.positionTableWidget.resizeColumnsToContents()
        self.positionTableWidget.resizeRowsToContents()
        self.layout.addWidget(self.positionTableWidget, 2, 0, 3, 3)   
        
    def renderSummary(self, summaryDict):
        for (key, summaryItem) in sorted(summaryDict.iteritems()):
            #custodyName
            custodyNameItem = QTableWidgetItemString(summaryItem.custodyName, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_CUSTODY_NAME,custodyNameItem)
            #assetTypeName
            assetTypeNameItem = QTableWidgetItemString(summaryItem.assetType, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_ASSET_TYPE_NAME,assetTypeNameItem)
            #InvestedAmount
            investedAmountItem = QTableWidgetItemDecimal(summaryItem.investedAmount, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_INVESTED_AMOUNT,investedAmountItem)
            #valuatedAmount
            valuatedAmountItem = QTableWidgetItemDecimal(summaryItem.valuatedAmount, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_VALUATED_AMOUNT,valuatedAmountItem)
            #netPNLPercentage
            netPNLPercentageItem = QTableWidgetItemDecimal(summaryItem.getNetPnLPercentage(), False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_NET_PNL_PERCENTAGE,netPNLPercentageItem)
            #realizedPnl
            realizedPnlItem = QTableWidgetItemDecimal(summaryItem.realizedPnl, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_REALIZED_PNL,realizedPnlItem)
            #positionPercentage
            positionPercentageItem = QTableWidgetItemDecimal(summaryItem.positionPercentage, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_POSITION_PERCENTAGE,positionPercentageItem)
            #weightedPnL
            weightedPnLItem = QTableWidgetItemDecimal(summaryItem.weightedPnL, False)
            self.summaryTableWidget.setItem(self.summaryRow,Constant.CONST_COLUMN_SUMMARY_CUST_WEIGHTED_PNL,weightedPnLItem)
            self.summaryRow += 1
            
    def renderSubtotal(self, positionDict, assetType ,isSIC):  
        accValuatedAmount = Engine.getSubTotalValuatedAmount(positionDict, assetType, isSIC)
        accInvestedAmount = Engine.getSubTotalInvestedAmount(positionDict, assetType, isSIC)
        accRealizedPnl = Engine.getAccRealizedPnL(positionDict, assetType, isSIC)
        accPositionPercentage = Engine.getAccPositionPercentage(positionDict, assetType, isSIC)
        accGrossPnlPercentage = Engine.getAccGrossPnlPercentage(positionDict, assetType, isSIC)
        accNetPnlPercentage = Engine.getAccNetPnlPercentage(positionDict, assetType, isSIC)
        accNetPNL = Engine.getAccNetPNL(positionDict, assetType, isSIC)
        accWeightedPNL = Engine.getAccWeightedPNL(positionDict, assetType, isSIC)
        #Invested amount
        investedAmountItem = QTableWidgetItemDecimal(accInvestedAmount, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
        #sub total valuated amount
        subTotalValuatedAmountItem = QTableWidgetItemDecimal(accValuatedAmount, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,subTotalValuatedAmountItem)   
        #sub total Gross PNL    
        subTotalGrossPNLItem = QTableWidgetItemDecimalColor(Engine.getSubtotalGrossPNL(positionDict, assetType, isSIC), True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL,subTotalGrossPNLItem)
        #sub total Net PNL    
        subTotalNetPNLItem = QTableWidgetItemDecimalColor(accNetPNL, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_NET_PNL,subTotalNetPNLItem)
        #subTotalGrossPnLPercentage
        subTotalGrossPnLPercentage = QTableWidgetItemDecimalColor(accGrossPnlPercentage, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL_PERCENTAGE,subTotalGrossPnLPercentage)
        #pnLNetPercentage
        subTotalNetPnLPercentage = QTableWidgetItemDecimalColor(accNetPnlPercentage, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_NET_PERCENTAGE,subTotalNetPnLPercentage)
        #realizedPnL
        realizedPnLItem = QTableWidgetItemDecimalColor(accRealizedPnl, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_REALIZED_PNL,realizedPnLItem)
        #positionPercentage
        positionPercentageItem = QTableWidgetItemDecimal(accPositionPercentage, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
        #weightedPercentageItem
        weightedPercentageItem = QTableWidgetItemDecimal(accWeightedPNL, True)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_WEIGHTED_PNL,weightedPercentageItem)
        #HiddenID
        hiddenIDItem = QTableWidgetItemDecimal(self.row, False)
        self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_HIDDEN_ID,hiddenIDItem)

    def renderPositions(self, positionDict, assetType ,isSIC):   
        positionList = Engine.getPositionByAssetType(positionDict, assetType, isSIC)
        for position in positionList:
            print('rendering ' + position.getAssetName())
            if(position.getTotalQuantity() != 0):
                position.row = self.row
                #assetName
                assetNameItem = QTableWidgetItemString(position.getAssetName(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_ASSET_NAME,assetNameItem)
                #totalQuantity
                totalQuantityItem = QTableWidgetItemInt(position.getTotalQuantity(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_QUANTITY,totalQuantityItem)
                #UnitCostOrRate
                unitCostItem = QTableWidgetItemDecimal(position.getUnitCostOrRate(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_PPP,unitCostItem)
                #Market price
                marketPriceItem = QTableWidgetItemDuoDecimal(position.getMarketPrice(), position.getMarketPriceOrig())
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MARKET_PRICE,marketPriceItem)
                #changePercentage
                changePercentageItem = QTableWidgetItemStringPlusMinus(position.changePercentage, False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_CHANGE_PERCENTAGE,changePercentageItem)
                #Invested amount
                investedAmountItem = QTableWidgetItemDecimal(position.getInvestedAmount(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_INVESTED_AMOUNT,investedAmountItem)
                #Valuated amount
                valuatedAmountItem = QTableWidgetItemDuoDecimal(position.getValuatedAmount(), position.getValuatedAmountOrig())
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_VALUATED_AMOUNT,valuatedAmountItem)
                #Tenor
                tenorItem = QTableWidgetItemDuoInt(position.tenor, position.getElapsedDays())
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_TENOR,tenorItem)
                #Maturity Date
                maturityDateItem = QTableWidgetItemString(position.getMaturityDate(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_MATURITY_DATE,maturityDateItem)
                #GrossPnL
                grossPnlItem = QTableWidgetItemDecimalColor(position.getGrossPnL(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL,grossPnlItem)
                #netPnL
                netPnlItem = QTableWidgetItemDecimalColor(position.getNetPnL(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_NET_PNL,netPnlItem)
                #pnLGrossPercentage
                pnLGrossPercentageItem = QTableWidgetItemDecimalColor(position.getGrossPnLPercentage(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_PNL_PERCENTAGE,pnLGrossPercentageItem)
                #pnLNetPercentage
                pnLNetPercentageItem = QTableWidgetItemDecimalColor(position.getNetPnLPercentage(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_GROSS_NET_PERCENTAGE,pnLNetPercentageItem)
                #realizedPnL
                realizedPnLItem = QTableWidgetItemDecimalColor(position.realizedPnl, False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_REALIZED_PNL,realizedPnLItem)
                #positionPercentage
                positionPercentageItem = QTableWidgetItemDecimal(position.getPositionPercentage(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_POSITION_PERCENTAGE,positionPercentageItem)
                #weightedPercentageItem
                weightedPercentageItem = QTableWidgetItemDecimal(position.getWeightedPnl(), False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_WEIGHTED_PNL,weightedPercentageItem)
                #HiddenID
                hiddenIDItem = QTableWidgetItemDecimal(self.row, False)
                self.positionTableWidget.setItem(self.row,Constant.CONST_COLUMN_POSITION_HIDDEN_ID,hiddenIDItem)
                self.row +=1  
        self.renderSubtotal(positionDict, assetType, isSIC)
        self.row +=1 
        
    def openMovementView(self):
        assetName = self.positionTableWidget.item(self.positionTableWidget.currentRow(), Constant.CONST_COLUMN_POSITION_ASSET_NAME).text()
        movementList = Engine.getMovementListByAsset(assetName, (self.movementFilterWidget.dateFromDate.date()).toString("yyyy-M-dd"),(self.movementFilterWidget.dateToDate.date()).toString("yyyy-M-dd"))
        self.movementView = MovementView(movementList)
        self.movementView.show()
