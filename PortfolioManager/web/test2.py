import json

import pyEX
import requests


# date1 = '2018-02-05'
# c = pyEX.Client(api_token="pk_c4c339ea14ba4aad92d9256ac75705e4")
# for d in c.chart(symbol='CCRE', date=date1, timeframe='5d'):
#     print(d)
#     if (d['date'] == date1):
#         print(d)
result = requests.get('https://cloud.iexapis.com/stable/stock/CCRE/chart/date/20180205?chartByDay=true&token=pk_c4c339ea14ba4aad92d9256ac75705e4')
json_data = json.loads(result.text)
print(json_data)

#DTB = 60 - Price not found for YBAO Start=2012-11-01 End=2012-12-31