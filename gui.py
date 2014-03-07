#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import os
from reader import getFile

class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        
        self.buildMenu()
        self.buildLayout()
        
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle(u'Lecteur Interdisciplinaire de Chants Oniriques Répondant aux Nouvelles Exigences')
    
    def buildLayout(self):
        txtSearch = QtGui.QLabel('Motif', self)
        txtSearch.move(10, 30)
        editSearch = QtGui.QLineEdit(self)
        editSearch.move(80, 30)
        txtResult = QtGui.QLabel(u'Résultat', self)
        txtResult.move(10, 50)
        displayResult = QtGui.QLineEdit(self)
        displayResult.move(10, 70)
    
    def buildMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&Fichier')

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Quitter', self)        
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Quitter le programme')
        exitAction.triggered.connect(QtGui.qApp.quit)
        fileMenu.addAction(exitAction)

        openAction = QtGui.QAction('&Ouvrir', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Ouvrir un fichier')
        openAction.triggered.connect(self.openNewFile)
        fileMenu.addAction(openAction)

    def openNewFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        if filename != "":
            getFile(filename)
