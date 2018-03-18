from datetime import date, timedelta, datetime
import logging

import pandas

from dao.dao import DaoAsset, DaoPrice
from modelClass.price import Price


df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//ImportHistoricalPrice.xlsx');
df.fillna(0)
#get the values for a given column
assetNameValues = df['Asset Name'].values
dateValues = df['Date'].values
closePriceValues = df['Close*'].values

dateToImport = date(2017, 01, 01)
dateToImport -= timedelta(days=1)
while dateToImport.weekday() > 4: # Mon-Fri are 0-4
    dateToImport -= timedelta(days=1)
print(dateToImport)
for index, assetNameValue in enumerate(assetNameValues):
    dateValue = datetime.strptime(dateValues[index], '%b %d, %Y')
    if dateValue.date() == dateToImport:
        rs = DaoPrice.getPriceByDate(assetNameValue, dateToImport)
        assetRs = DaoAsset().getAssetByName(assetNameValue)
        assetOID = assetRs[0][0]
        if len(rs) == 0:
            price = Price(None)
            lastPrice = closePriceValues[index]
            price.setAttr(None, assetOID, round(lastPrice, 4), dateToImport) 
            print(assetNameValue + " " + str(lastPrice) + " " + str(dateToImport))
            DaoPrice.insert(price)
        else:
            logging.warning("CANNOT ADD ASSET NAME :" + assetNameValue + " " + str(dateToImport))
