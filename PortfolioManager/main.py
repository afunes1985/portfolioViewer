from datetime import date
import sys

from PySide import QtGui

from core.cache import Singleton
from core.mainEngine import MainEngine


def main():
    app = QtGui.QApplication(sys.argv)
    mainEngine = Singleton(MainEngine)
    mainEngine.refreshAll(date(2001, 7, 14), date(2020, 7, 14))
    sys.exit(app.exec_())

if __name__== '__main__':
    main()