
from dao.dao import DaoCompanyFundamental
import matplotlib.pyplot as plt

indicatorID = 'GrossProfit'
resultDict = DaoCompanyFundamental.getCompanyFundamental('50863', indicatorID)
print(resultDict["column"])
print(resultDict["rs"])
listY = []
for row in resultDict["rs"][0]:
    if row is not None:
        listY.append(row/1000000)
    else:
        listY.append(row)
listX = []
for row in resultDict["column"]:
    if row is not None:
        listX.append(row[2:6])
plt.plot(listX, listY, color='orange')
plt.xlabel('Quarter')
plt.ylabel('Millions')
plt.title(indicatorID)
plt.show() 