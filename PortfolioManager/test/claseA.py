from claseB import ClaseB

class ClaseA():
    def __init__(self):
        print('A')
    
    def getA(self):
        print('Get A')
        
    def getB(self):
        claseB = ClaseB()
        claseB.getB()