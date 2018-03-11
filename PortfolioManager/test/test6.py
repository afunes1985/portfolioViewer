#===============================================================================
# '''
# Created on 11 mar. 2018
# 
# @author: afunes
# '''
# import pandas as pd
# import numpy as np
# from pprint import pprint
# 
# # reading the data
# data = pd.read_csv('C://Users//afunes//iCloudDrive//PortfolioViewer//import//data.csv', index_col=0);
# #data = pd.read_csv('data.csv', index_col=0)
# # sort the df by ascending years and descending happiness scores
# data.sort_values(['Year', "Happiness Rank"], ascending=[False, True], inplace=True)
# # getting an overview of our data
# print("Our data has {0} rows and {1} columns".format(data.shape[0], data.shape[1]))
# # checking for missing values
# print("Are there missing values? {}".format(data.isnull().any().any()))
# data.describe()
# pprint(data)
#===============================================================================

import pandas
from pprint import pprint

data = [('Apple',      'Coles',      1.50),
        ('Apple',      'Woolworths', 1.60),
        ('Apple',      'IGA',        1.70),
        ('Banana',     'Coles',      0.50),
        ('Banana',     'Woolworths', 0.60),
        ('Banana',     'IGA',        0.70),
        ('Cherry',     'Coles',      5.00),
        ('Date',       'Coles',      2.00),
        ('Date',       'Woolworths', 2.10),
        ('Elderberry', 'IGA',        10.00)]

df=pandas.DataFrame(data, columns=['Fruit', 'Shop', 'Price'])
df.pivot(index='Fruit', columns='Shop', values='Price')
df.sort_values(['Fruit', "Shop"], ascending=[False, True], inplace=True)

pprint(df)