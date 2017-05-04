
class ClaseB():
    def __init__(self):
        print('B')
    
    def getB(self):
        print('Get B')
    
    def getA(self):
        from test.claseA import ClaseA
        claseA = ClaseA()
        claseA.getA()