import sys

from PySide.QtGui import QApplication, QTreeWidgetItem, QWidget, QTreeWidget


if __name__ == '__main__':
    app = 0
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    l1 = QTreeWidgetItem(["ALFA", "100"])
    l2 = QTreeWidgetItem(["GRUMA", "200"])

    for i in range(3):
        l1_child = QTreeWidgetItem([None, str(i*10), "Child C" + str(i)])
        l1.addChild(l1_child)

    for j in range(2):
        l2_child = QTreeWidgetItem([None, str(j*20), "Child CC" + str(j)])
        l2.addChild(l2_child)

    w = QWidget()
    w.resize(510, 210)

    tw = QTreeWidget(w)
    tw.resize(500, 200)
    tw.setColumnCount(3)
    tw.setHeaderLabels(["Asset", "Gross Amount", "Payment Date"])
    tw.addTopLevelItem(l1)
    tw.addTopLevelItem(l2)

    w.show()
    sys.exit(app.exec_())