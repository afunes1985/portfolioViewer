'''
Created on 11 jun. 2018

@author: afunes
'''

from datetime import datetime

import PyPDF2
import pandas

from core.cache import Singleton, MainCache
from dao.dao import DaoMovement
from engine.engine import Engine
from modelClass.movement import Movement


types = {'ABONO DIVIDENDO EMISORA EXTRANJERA' : 'DIVIDENDO', 
         'ISR 10 % POR DIVIDENDOS SIC' : 'ISR_DIVIDENDO', 
         'Compra Soc. de Inv. - Cliente' : 'FUND_BUY', 
         'Compra de Acciones.' : 'EQUITY_BUY', 
         'Venta Soc. de Inv. - Cliente' : 'FUND_SELL',
         'DEPOSITO DE EFECTIVO' : 'CASH'}
class tools():
    @staticmethod
    def getNextPointBySpace(data,strToFind, startPoint, steps):
        nextPoint = startPoint
        if strToFind == '\n': 
            fix = 0 
        else:
            fix = 1
        while steps != 0:
            if steps > 0:
                nextPoint = data.find(strToFind, nextPoint) + len(strToFind) + fix
                steps = steps - 1
            elif steps < 0:
                nextPoint = data.rfind(strToFind,0 , nextPoint) - len(strToFind) - fix
                steps = steps + 1
        return nextPoint

mainCache = Singleton(MainCache)
mainCache.refreshReferenceData()
fileName = "GBM_18-04.pdf"
pdfFileObj = open(fileName, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
page = pdfReader.getPage(3)
page_content = page.extractText().encode('utf-8')
print (page_content)
date =  fileName.replace(".pdf", '')
date = date.replace("GBM_","")
custodyOID = Engine.getCustodyDictName()['GBM'].OID
assetDict = Engine.getAssetDict()
assetTranslator = {'GBMF2 BF' : 'GBMF2BF.MX'}
print (date)
for key, value in types.iteritems():
    nextSection = (page_content.find(key, 0))
    while nextSection != -1:
            print("------------------INIT-----------")
            nextPoint = nextSection
            externalID = page_content[page_content.rfind('\n', 0, nextPoint-1): nextPoint -1]
            externalID = externalID.replace('\n', "")
            print("externalID " + externalID)
            nextPointToBack = tools.getNextPointBySpace(page_content, '\n', nextPoint - 1, -1)
            paymentDate = page_content[page_content.rfind('\n', 0, nextPointToBack): nextPointToBack]
            paymentDate = paymentDate[1:3]
            paymentDate = date + "-" + paymentDate
            paymentDate =  pandas.to_datetime(datetime.strptime(paymentDate, '%y-%m-%d')).to_pydatetime() 
            print ("paymentDate " + str(paymentDate))
            #nextPoint = nextPoint + len(key) + 1
            nextPoint = tools.getNextPointBySpace(page_content, key, nextPoint, 1)
            nextSection = nextPoint
            #print("STEP " +  str(nextPoint))
            assetName = page_content[nextPoint: page_content.find('\n', nextPoint)]
            print (assetName)
            if (value != 'CASH'):
                asset = assetDict[assetTranslator[assetName]]
            nextPoint = tools.getNextPointBySpace(page_content, '\n', nextPoint, 1)
            quantity = page_content[nextPoint: page_content.find('\n', nextPoint)]
            print (quantity)
            nextPoint = tools.getNextPointBySpace(page_content, '\n', nextPoint, 1)
            price = page_content[nextPoint: page_content.find('\n', nextPoint)]
            print (price)
            nextPoint = tools.getNextPointBySpace(page_content, '\n', nextPoint, 4)
            netAmount = page_content[nextPoint: page_content.find('\n', nextPoint)]
            netAmount = float(netAmount.replace(',',''))
            print (netAmount)
            comment = "UPLOAD " + date
            print (comment)
            rs = DaoMovement.getMovementsByExternalID(externalID)
            if len(rs) == 0:
                m = Movement(None)
                #m.setAttr( None, asset.OID, 'BUY', paymentDate, quantity, price, None, netAmount, netAmount, 0, 0, 0, externalID, custodyOID, comment, None, None)
                #newID = DaoMovement.insertMovement(m)
                print("ADD externalID " + str(externalID))
            else:
                print("CANNOT ADD externalID " + str(externalID))
            #print (page_content)
            nextSection = (page_content.find(key, nextSection))



 

