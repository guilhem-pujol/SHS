#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import os
from reader import getFile
from debug import toGreek
from graph import GraphDrawer

class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        
        self.buildMenu()
        self.buildLayout()
        
        self.setGeometry(200, 200, 1200, 800)
        self.setWindowTitle(u'Lecteur Interdisciplinaire de Chants Oniriques Répondant aux Nouvelles Exigences')
        
        self.text = None
    
    def buildLayout(self):
        txtSearch = QtGui.QLabel('Motif', self)
        txtSearch.move(10, 30)
        
        self.editSearch = QtGui.QLineEdit(self)
        #FIXME: this is the old API style, see how to use new method
        self.editSearch.textEdited.connect(self.startSearch)
        self.editSearch.move(80, 30)
        
        self.txtDisplay = QtGui.QLabel(u'Texte', self)
        self.txtDisplay.move(10, 300)
        self.txtDisplay.setFixedSize(500, 1000)
        
        self.searchResult = QtGui.QLabel(u'Résultat', self)
        self.searchResult.move(200, 30)
        
        self.graph1 = QtGui.QLabel(u'Graphe', self)
        self.graph1.move(10, 70)
        self.graph1.setFixedSize(500, 200) 
        
        self.graph2 = QtGui.QLabel(u'Graphe 2', self)
        self.graph2.move(550, 70)
        self.graph2.setFixedSize(500, 200) 
    
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
        self.loadFile(filename)
    
    def loadFile(self, filename):
        if filename == "": return None
        
        self.text = getFile(filename)
        self.setWindowTitle(u'LICORNE : '+filename)
        self.txtDisplay.setText(u"Fichier chargé :\n"+self.text.text())
    
    def startSearch(self):
        if self.text == None: return
        self.editSearch.setText(toGreek(self.editSearch.text()))
        self.text.search(unicode(self.editSearch.text()))
        self.searchResult.setText(str(self.text.numMatch))
        
        graph1 = GraphDrawer(self.text)
        graph1.buildGraph()
        self.graph1.setPixmap(graph1.getImage())
        
        graph2 = GraphDrawer(self.text)
        graph2.buildGraph()
        self.graph2.setPixmap(graph2.getImage())
