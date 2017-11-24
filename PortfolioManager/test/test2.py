import pandas


#df = pandas.read_excel('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv')
df = pandas.read_csv('C://Users//afunes//iCloudDrive//PortfolioViewer//import//quotes.csv');
#print the column names
print df.columns
#get the values for a given column
assetName = 'ALFAA.MX'
symbolValues = df['Symbol'].values
curPriceValues = df['Current Price'].values
changeValues = df['Change'].values
#get a data frame with selected columns
print(symbolValues[0])
returnList = []
for index, rfRow in enumerate(symbolValues):
    print(index, rfRow)
    if assetName == rfRow:
        returnRow = []
        returnRow.append(rfRow)
        currentPrice = curPriceValues[index]
        returnRow.append(round(currentPrice,2))
        change = changeValues[index]
        returnRow.append(round((((currentPrice)/(currentPrice-change)-1)*100), 2))
        returnList.append(returnRow)
print(returnList)