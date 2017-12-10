'''
Created on 21 nov. 2017

@author: afunes
'''
class CEExcelImport:
    
    @staticmethod
    def importData():
        import pandas
        
        from dao.dao import DaoCorporateEvent
        from engine.engine import Engine
        from modelClass.corporateEvent import CorporateEvent
        
        
        #df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
        df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//Import_Corporate_Event.xlsx');
        #get the values for a given column
        paymentDateValues = df['Payment date'].values
        descriptionValues = df['Description'].values
        assetNameValues = df['Asset name'].values
        amountValues = df['Amount'].values
        returnList = []
        grossAmount = 0
        isrAmount = 0
        assetDict = Engine.getAssetDict()
        corporateEventTypeDictOID = Engine.getCorporateEventTypeDictOID()
        for index, rfRow in enumerate(assetNameValues):
                paymentDate = None
                assetName = assetNameValues[index]
                if descriptionValues[index].find('ISR') == 0:
                    isrAmount = float(amountValues[index])
                else:
                    grossAmount = float(amountValues[index])
                    netAmount = round(grossAmount - isrAmount, 2)
                    paymentDate =  pandas.to_datetime(str(paymentDateValues[index])).to_pydatetime()  
                    print(isrAmount)
                    print(grossAmount)
                    print(paymentDate)
                    isrAmount = 0
                    grossAmount = 0
                    asset = assetDict[assetName]
                    ce = CorporateEvent(None)
                    ce.setAttr(None, asset.defaultCustody, corporateEventTypeDictOID[1], asset, paymentDate, grossAmount, netAmount, 'TEST')
                    DaoCorporateEvent().insert(ce)

    
    
    
    
    
    