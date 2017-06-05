import sys, time

from PySide import QtGui, QtCore

class test():
    def progress(self):
        widget = QtGui.QProgressDialog("Show Progress", "Stop", 0, 10)
        widget.show()
        for row in range(10):
            QtCore.QCoreApplication.instance().processEvents()
            widget.setValue(row)
            time.sleep(.1)
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    test().progress()
