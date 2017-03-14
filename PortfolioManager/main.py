'''
Created on Feb 12, 2017

@author: afunes
'''

from datetime import date
from dao.dao import DaoMovement
from modelClass.modelClass import Position

movementList = DaoMovement().getMovementsByDate(date(2001, 7, 14), date(2020, 7, 14))
positionDict = {}
position = 0
#print(positionDict.get('1'))

for (movement) in movementList:
    assetName = movement[1]
    buySell = movement[2]
    print("asset = {}".format(assetName))
    position = positionDict.get(assetName)
    if position is None:
        position = Position(movement)
        positionDict[assetName] = position
    else:    
        position.addMovement(movement)

for key, value in positionDict.items():
    print("key = {}".format(key)) 
    print("PPP = {}".format(value.getPPP()))
    print("totalamount = {}".format(value.accumulatedAmount))
    print("totalquantity = {}".format(value.totalQuantity))
