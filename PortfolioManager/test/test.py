'''
Created on 9 nov. 2017

@author: afunes
'''
import httplib
import json



# Request: Market Quotes (https://sandbox.tradier.com/v1/markets/quotes?symbols=spy)
connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

# Headers

headers = {"Accept":"application/json",
           "Authorization":"Bearer XGabnWN7VqBkIuSVvS6QrhwtiQcK"}

# Send synchronously

connection.request('GET', '/v1/markets/quotes?symbols=NOK', None, headers)
try:
    response = connection.getresponse()
    content = response.read()
    # Success
    print('Response status ' + str(response.status))
    json_data = json.loads(content)
    # print (json_data['quotes']['quote']) 
    print('Response content ' + str(content))
    print (len(json_data['quotes']['quote']))
    if isinstance(json_data['quotes']['quote'], list): 
        print('list')
        for x in json_data['quotes']['quote']:
            print (x['symbol'])
            print (x['bid'])
            print (x['change_percentage'])
    else: 
        print (json_data['quotes']['quote']['symbol'])
        print (json_data['quotes']['quote']['bid'])
        print (json_data['quotes']['quote']['change_percentage'])

except httplib.HTTPException:
  # Exception
  print('Exception during request')