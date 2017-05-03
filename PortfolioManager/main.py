from datetime import date
import sys

from PySide import QtGui

from core.cache import Singleton, MainCache
from engine.engine import Engine
from frame.mainWindow import MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = Singleton(MainWindow)
    mainCache = Singleton(MainCache)
    mainCache.positionDict = Engine.buildPositions(date(2001, 7, 14), date(2020, 7, 14))
    mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 0)
    mainWindow.renderPositions(mainCache.positionDict, 'EQUITY', 1)
    mainWindow.renderPositions(mainCache.positionDict, 'FUND', 0)
    mainWindow.renderPositions(mainCache.positionDict, 'BOND', 0)
    mainWindow.renderSubtotal(mainCache.positionDict, 'ALL', 0)
    sys.exit(app.exec_())

if __name__== '__main__':
    main()