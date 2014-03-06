#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

txtSearch = QtGui.QLabel('Motif')
editSearch = QtGui.QLineEdit()
txtResult = QtGui.QLabel(u'Résultat')
displayResult = QtGui.QLineEdit()

grid = QtGui.QGridLayout()
grid.setSpacing(10)

grid.addWidget(txtSearch, 1, 0)
grid.addWidget(editSearch, 1, 1)

grid.addWidget(txtResult, 2, 0)
grid.addWidget(displayResult, 3, 0)

w = QtGui.QWidget()
w.setLayout(grid)

w.move(300, 300)
w.setWindowTitle('Analyse de texte')
w.show()

sys.exit(app.exec_())
