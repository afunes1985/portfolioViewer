from datetime import date, timedelta, datetime
import logging

import pandas

from dao.dao import DaoAsset, DaoPrice, DaoCurrency
from modelClass.price import Price
from modelClass.currency import CurrencyValue


df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//ImportHistoricalPrice.xlsx');
df.fillna(0)
#get the values for a given column
assetNameValues = df['Asset Name'].values
dateValues = df['Date'].values
closePriceValues = df['Close*'].values
isCurrencyValues = df['Is currency'].values

date_time_str = '2018-06-29'  
date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
print(date_time_obj)

dateToImport = date(2019, 1, 1)
dateToImport -= timedelta(days=1)
while dateToImport.weekday() > 4: # Mon-Fri are 0-4
    dateToImport -= timedelta(days=1)
print("Import to date " + str(dateToImport))
for index, assetNameValue in enumerate(assetNameValues):
    dateValue = datetime.strptime(str(dateValues[index]), '%Y-%m-%dT%H:%M:%S.000000000')
    if dateValue.date() == dateToImport:
        if isCurrencyValues[index]:
            rs = DaoCurrency.getCurrencyValueByDate(assetNameValue, dateToImport)
            currencyRs = DaoCurrency.getCurrencyByName(assetNameValue)
            if len(rs) == 0:
                currencyValue = CurrencyValue(None)
                currencyValue.setAttr(None, currencyRs[0][0], dateToImport.strftime('%Y-%m-%d %H:%M:%S'), round(closePriceValues[index], 4))
                DaoCurrency.insertCurrencyValue(currencyValue)
                print("ADD PRICE ASSET NAME :" + assetNameValue + " " + str(dateToImport))
            else:
                logging.warning("CANNOT ADD PRICE ASSET NAME :" + assetNameValue + " " + str(dateToImport))
        else:
            rs = DaoPrice.getPriceByDate(assetNameValue, dateToImport)
            assetRs = DaoAsset().getAssetByName(assetNameValue)
            assetOID = assetRs[0][0]
            if len(rs) == 0:
                price = Price(None)
                lastPrice = closePriceValues[index]
                price.setAttr(None, assetOID, round(lastPrice, 4), dateToImport.strftime('%Y-%m-%d %H:%M:%S')) 
                print(assetNameValue + " " + str(lastPrice) + " " + str(dateToImport))
                DaoPrice.insert(price)
                print("ADD PRICE ASSET NAME :" + assetNameValue + " " + str(dateToImport))
            else:
                logging.warning("CANNOT ADD PRICE ASSET NAME :" + assetNameValue + " " + str(dateToImport))
