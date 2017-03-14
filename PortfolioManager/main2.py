from datetime import date
import sys

from PySide import QtGui

from engine.engine import Engine
from modelClass.modelClass import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = Engine().startApp()
    sys.exit(app.exec_())

if __name__== '__main__':
    main()