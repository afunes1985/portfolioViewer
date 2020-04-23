'''
Created on May 4, 2017

@author: afunes
'''

from datetime import datetime
import threading

from core.cache import MainCache
from core.constant import Constant
from core.corporateEventPosition import CorporateEventPosition
from core.position import Position
from dao.corporateEventDao import CorporateEventDao
from dao.movementDao import MovementDao
import pandas as pd


class PositionEngine():

    def refreshPositions(self, fromDate, toDate):
        position_DF = pd.DataFrame(columns=['Asset Name','Asset Type','isSIC','Position','Unit Cost', 'Market Price', 'Change', 'Invested Amount', 'Valuated Amount', 'Tenor', 'Maturity Date', 'Gross PnL', 'Net PnL', 'Gross%PNL', 'Net%PNL', 'Realized PnL', '%Portfolio', 'WeightedPnL%'])
        resultPositionDict = self.buildPositions(fromDate, toDate, True)
        
        for row in resultPositionDict[Constant.CONST_POSITION_DICT].items():
            position = row[1]
            position_DF = position_DF.append(pd.Series([position.asset.getName(), position.asset.assetType, position.asset.isSIC, position.getTotalQuantity(), position.getUnitCostOrRate(), position.getMarketPrice(), position.changePercentage, position.getInvestedAmount(), 
                  position.getValuatedAmount(), position.getElapsedDays(), position.getMaturityDate(), position.getGrossPnL(), position.getNetPnL(), position.getGrossPnLPercentage(), 
                  position.getNetPnLPercentage(), position.getConsolidatedRealizedPnl(), None, None], index=position_DF.columns), ignore_index=True)
        
        position_DF = position_DF.sort_values(['Asset Type', 'isSIC', 'Asset Name'], ascending=[1, 0, 1])
        
        totalValuatedAmount = position_DF['Valuated Amount'].sum()
        
        posEquityNoSIC = position_DF.loc[(position_DF['Asset Type'] == 'EQUITY') & (position_DF['isSIC'] == False)]
        posEquityNoSIC = posEquityNoSIC.append(pd.Series([posEquityNoSIC['Invested Amount'].sum(), posEquityNoSIC['Valuated Amount'].sum()], index=['Invested Amount', 'Valuated Amount']), ignore_index=True)
        
        posEquitySIC = position_DF.loc[(position_DF['Asset Type'] == 'EQUITY') & (position_DF['isSIC'] == True)]
        posEquitySIC = posEquitySIC.append(pd.Series([posEquitySIC['Invested Amount'].sum(), posEquitySIC['Valuated Amount'].sum()], index=['Invested Amount', 'Valuated Amount']), ignore_index=True)
        
        posFund = position_DF.loc[(position_DF['Asset Type'] == 'FUND')]
        posFund = posFund.append(pd.Series([posFund['Invested Amount'].sum(), posFund['Valuated Amount'].sum()], index=['Invested Amount', 'Valuated Amount']), ignore_index=True)
       
        posBond = position_DF.loc[(position_DF['Asset Type'] == 'BOND')]
        posBond = posBond.append(pd.Series([posBond['Invested Amount'].sum(), posBond['Valuated Amount'].sum()], index=['Invested Amount', 'Valuated Amount']), ignore_index=True)
        
        finalPosition_DF = posEquityNoSIC.append(posEquitySIC, ignore_index=True)
        finalPosition_DF = finalPosition_DF.append(posFund, ignore_index=True)
        finalPosition_DF = finalPosition_DF.append(posBond, ignore_index=True)
        finalPosition_DF = finalPosition_DF.append(pd.Series(['Total MXN', position_DF['Invested Amount'].sum(), totalValuatedAmount], index=['Asset Name','Invested Amount', 'Valuated Amount']), ignore_index=True)
        
        for index, row in finalPosition_DF.iterrows():
            positionPercentage = row['Valuated Amount']/totalValuatedAmount
            finalPosition_DF.at[index, '%Portfolio'] = positionPercentage
            if (not pd.isnull(row['Gross%PNL'])):
                finalPosition_DF.at[index, 'WeightedPnL%'] = row['Gross%PNL'] * positionPercentage
        
        finalPosition_DF = finalPosition_DF.append(pd.Series(['Total USD', totalValuatedAmount/MainCache.usdMXN], index=['Asset Name','Valuated Amount']), ignore_index=True)
        
        return finalPosition_DF
        
        
    def buildPositions(self, fromDate, toDate, setLastMarketData):
        movementList = MovementDao().getMovementsByDate(fromDate, toDate)
        positionDict = {}
        oldPositionDict = {}
        threads = []
        today = datetime.now().date()
        for movement in movementList:
            position = None
            asset = movement.asset
            assetName = asset.name
            if(asset.assetType == 'BOND'):
                assetName = assetName + str(movement.ID)
            position =  positionDict.get(assetName, None)
            if position == None:
                position = Position(asset, movement)
                positionDict[assetName] = position
            else:           
                position.addMovement(movement)
            #pasa la posicion al viejo diccionario de posiciones si no tiene mas posicion o esta vencida
            if (position.asset.assetType == 'BOND'
                 and ((position.isMatured and today == toDate)
                    or (position.maturityDate.date() < toDate and today != toDate))
                or position.totalQuantity == 0):
                oldPosition =  oldPositionDict.get(assetName, None)
                if oldPosition == None:
                    oldPositionDict[assetName] = position
                else:
                    oldPosition.addPositionToOldPosition(position)#TODO TESTEAR
                positionDict.pop(assetName, None)
        if setLastMarketData:         
            for key, position2 in positionDict.items():
                t = threading.Thread(target=position2.refreshMarketData)
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()
        
        returnDict = {}
        returnDict[Constant.CONST_POSITION_DICT] = positionDict
        returnDict[Constant.CONST_OLD_POSITION_DICT] = oldPositionDict
        
        #Corporate event 
        corporateEventPositionDict = self.buildCorporateEventPosition()
        for (positionKey, corporateEventPosition) in corporateEventPositionDict.items():
            position = positionDict.get(positionKey, None)
            if(position is not None):
                position.addRealizedPnlCorporateEvent(corporateEventPosition.accGrossAmount)
        
        return returnDict

    def buildCorporateEventPosition(self):
        resultDict = {}
        ceList = CorporateEventDao().getCorporateEventList()
        for ce in ceList:
            corporateEventPosition = resultDict.get(ce.asset.name, None)
            if corporateEventPosition == None:
                resultDict[ce.asset.name] = CorporateEventPosition(ce)
            else:
                corporateEventPosition.addCorporateEvent(ce)
        return resultDict