'''
Created on Apr 26, 2017

@author: afunes
'''
def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance

class MainCache:
    _instance = None
    positionDict = None



