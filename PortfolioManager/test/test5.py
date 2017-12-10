import sys

from PySide.QtGui import QApplication, QTreeWidgetItem, QWidget, QTreeWidget

from engine.engine import Engine
from core.cache import Singleton, MainCache
mainCache = Singleton(MainCache)

if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)
    w = QWidget()
    w.resize(510, 210)
    tw = QTreeWidget(w)
    tw.resize(500, 200)
    tw.setColumnCount(3)
    tw.setHeaderLabels(["Asset", "Gross Amount", "Net Amount", "Payment Date"])
    mainCache = Singleton(MainCache)
    mainCache.refreshReferenceData()
    Engine.buildCorporateEventPosition()
    
    for key, cep in mainCache.corporateEventPositionDictAsset.items():
        l1 = QTreeWidgetItem([key, str(cep.accGrossAmount), str(cep.accNetAmount)])
        for ce in cep.corporateEventList:
            l1_child = QTreeWidgetItem([None, str(ce.grossAmount), str(ce.netAmount),str(ce.paymentDate)])
            l1.addChild(l1_child)
        tw.addTopLevelItem(l1)

    w.show()
    sys.exit(app.exec_())