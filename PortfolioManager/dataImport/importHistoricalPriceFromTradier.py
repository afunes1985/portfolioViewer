from datetime import date, timedelta
import httplib
import json
import logging

from dao.dao import DaoAsset, DaoPrice
from modelClass.price import Price


# Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)
# Headers
headers = {"Accept":"application/json",
           "Authorization":"Bearer XGabnWN7VqBkIuSVvS6QrhwtiQcK"}

dateToImport = date(2019, 01, 01)
dateToImport -= timedelta(days=1)
while dateToImport.weekday() > 4: # Mon-Fri are 0-4
    dateToImport -= timedelta(days=1)
print(dateToImport)

assetList = DaoAsset().getAssetList()
for asset in assetList:
    assetOID = asset[0]
    assetName = asset[2]
    assetOrigName = asset[3]
    isSic = asset[4]
    if isSic:
        if assetOrigName is not None:
            assetName = assetOrigName
        print(assetName)
        # Send synchronously
        connection.request('GET', '/v1/markets/history?symbol=' + assetName +'&interval=daily&start='+(dateToImport).strftime("%Y-%m-%d")+ '&end=' + (dateToImport).strftime("%Y-%m-%d"), None, headers)
        response = connection.getresponse()
        content = response.read()
        json_data = json.loads(content)
        print(json_data)
        rs = DaoPrice.getPriceByDate(assetName, dateToImport)
        if len(rs) == 0:
            price = Price(None)
            lastPrice = json_data['history']['day']['close']
            price.setAttr(None, assetOID, round(lastPrice, 2), dateToImport) 
            DaoPrice.insert(price)
        else:
            logging.warning("CANNOT ADD ASSET NAME :" + str(assetName))
