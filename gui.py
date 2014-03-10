#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import os
from reader import getFile
from debug import toGreek

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
        
        self.editSearch = QtGui.QLineEdit(self)
        #FIXME: this is old API style, see how to use new method
        self.editSearch.textEdited.connect(self.startSearch)
        self.editSearch.move(80, 30)
        
        self.txtResult = QtGui.QLabel(u'Résultat', self)
        self.txtResult.move(10, 70)
    
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
        if filename == "": return None
        
        text = getFile(filename)
        self.setWindowTitle(u'LICORNE : '+filename)
        self.txtResult.setFixedSize(500, 500)
        self.txtResult.setText(u"Fichier chargé :\n"+text.text())
        
    def startSearch(self):
        self.editSearch.setText(toGreek(self.editSearch.text()))
