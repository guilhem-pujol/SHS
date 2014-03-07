#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from gui import mainWindow

app = QtGui.QApplication(sys.argv)

w = mainWindow()
w.show()

sys.exit(app.exec_())
