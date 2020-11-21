'''
Created on 8 sep. 2018

@author: afunes
'''
from datetime import timedelta
import logging


def createLog(logName, level):
    logger= logging.getLogger(logName)
    logger.setLevel(level)
    fh = logging.FileHandler('log\\' + logName + '.log', mode='w')
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
    logger.addHandler(fh)
    return logger

def getLastWorkingDay(date):
    lastWorkingDay = date
    lastWorkingDay -= timedelta(days=1)
    while lastWorkingDay.weekday() > 4: # Mon-Fri are 0-4
        lastWorkingDay -= timedelta(days=1)
    return lastWorkingDay 

def getDateFormated(date, formatDate):
    if(date is not None):
        return date.strftime(formatDate)