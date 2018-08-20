from datetime import date, timedelta, datetime
import logging
import math

import pandas

from dao.dao import DaoAsset, DaoPrice, DaoCurrency, DaoCompany
from modelClass.currency import CurrencyValue
from modelClass.price import Price


df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//Import_CIK_TICKER.xlsx');
df.fillna(0)
#get the values for a given column
cikValues = df['CIK'].values
tickerValues = df['Ticker'].values
exchangeValues = df['Exchange'].values
irsValues = df['IRS'].values

try:
    
    for index, cikValue in enumerate(cikValues):
        rs = DaoCompany.getCompanyByCIK(str(cikValue))
        if (len(rs) == 1):
            print("OK")
            #if(exchangeValues[index] != "OTC"
            #   and not ( math.isnan(irsValues[index]))):
            DaoCompany.updateCompanyNameAndTicker(rs[0][0], str(tickerValues[index]))
        else:
            logging.warning("NOT OK")
except Exception as e:
    print(e)