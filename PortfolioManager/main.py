from datetime import date
import sys

from PySide import QtGui

from engine.engine import Engine
from modelClass.gui import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindow()
    positionDict = Engine().buildPositions()
    mainWindow.renderPositions(positionDict, 'EQUITY', 0)
    mainWindow.renderPositions(positionDict, 'EQUITY', 1)
    mainWindow.renderPositions(positionDict, 'FUND', 0)
    mainWindow.renderPositions(positionDict, 'BOND', 0)
    mainWindow.renderSubtotal(positionDict, 'ALL', 0)
    sys.exit(app.exec_())

if __name__== '__main__':
    main()