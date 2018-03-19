from datetime import date, datetime
import sys

from PySide import QtGui

from core.cache import Singleton
from core.mainEngine import MainEngine


def main():
    app = QtGui.QApplication(sys.argv)
    mainEngine = Singleton(MainEngine)
    mainEngine.refreshAll(datetime(2001, 7, 14).date(), datetime.now().date())
    sys.exit(app.exec_())

if __name__== '__main__':
    main()