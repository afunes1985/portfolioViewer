'''
Created on 15 jun. 2018

@author: afunes
'''

from PySide import QtGui
from PySide.QtGui import QLabel, QSizePolicy, QComboBox, QPushButton, \
    QLineEdit

from dao.dao import DaoCustody


class ImportMovementFilter(QtGui.QWidget):
    def __init__(self, parent):      
        super(self.__class__, self).__init__()
        self.parent = parent
        self.layout = QtGui.QGridLayout(self)
        #btnfileFinder
        self.btnfileFinder = QtGui.QPushButton("File")
        self.layout.addWidget(self.btnfileFinder, 1, 0)
        #txtFile
        self.txtFile = QLineEdit(self)
        self.layout.addWidget(self.txtFile, 1, 1)
        #btnSubmit
        self.btnSubmit = QPushButton("Submit", self)
        self.btnSubmit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.layout.addWidget(self.btnSubmit)
        self.setFixedSize(190, 150) 
        self.initListener() 
    
    def initListener(self):
        self.btnSubmit.clicked.connect(self.doSubmit)
        self.btnfileFinder.clicked.connect(self.doFile)
        self.btnfileFinder.show()
    
    def doSubmit(self):
        #custodyName = self.cmdCustodyName.currentText()
        self.parent.doSubmit(self.txtFile.text())
    
    def doFile(self):
        filePath = QtGui.QFileDialog.getOpenFileName()
        self.txtFile.setText(filePath[0])