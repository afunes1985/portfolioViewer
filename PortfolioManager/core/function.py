'''
Created on 18 mar. 2018

@author: afunes
'''
from datetime import timedelta


class Function():
    @staticmethod
    def getLastWorkingDay(date):
        lastWorkingDay = date
        lastWorkingDay -= timedelta(days=1)
        while lastWorkingDay.weekday() > 4: # Mon-Fri are 0-4
            lastWorkingDay -= timedelta(days=1)
        return lastWorkingDay 