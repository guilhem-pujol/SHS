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
        self.setWindowTitle(u'Analyse fréquentielle de textes')
        
        self.text = None
    
    def buildLayout(self):
        txtSearch = QtGui.QLabel('Motif', self)
        txtSearch.move(10, 30)
        
        self.editSearch = QtGui.QLineEdit(self)
        #FIXME: this is the old API style, see how to use new method
        self.editSearch.textEdited.connect(self.startSearch)
        self.editSearch.move(80, 30)

        self.searchResult = QtGui.QLabel(u'Résultat', self)
        self.searchResult.move(200, 30)
        self.searchResult.setFixedSize(300, 30)
        
        self.graph1 = QtGui.QLabel(u'Graphe', self)
        self.graph1.move(10, 70)
        self.graph1.setFixedSize(500, 200) 
        
        self.graph2 = QtGui.QLabel(u'Graphe 2', self)
        self.graph2.move(550, 70)
        self.graph2.setFixedSize(500, 200)  
        
        txtFrom = QtGui.QLabel(u'Vers no', self)
        txtFrom.move(10, 275)
        self.editBegin = QtGui.QLineEdit(self)
        self.editBegin.move(40, 275)
        #FIXME: this is the old API style, see how to use new method
        self.editBegin.textEdited.connect(self.updateBounds)
        txtTo = QtGui.QLabel(u'jusqu\'à', self)
        txtTo.move(140, 275)
        self.editEnd = QtGui.QLineEdit(self)
        self.editEnd.move(190, 275)
        #FIXME: this is the old API style, see how to use new method
        self.editEnd.textEdited.connect(self.updateBounds)
               
        self.txtDisplay = QtGui.QLabel(u'Texte', self)
        self.txtScrollArea = QtGui.QScrollArea(self);
        self.txtScrollArea.move(10, 310)
        self.txtScrollArea.setFixedSize(1000, 500)
        self.txtScrollArea.setWidget(self.txtDisplay)
        self.txtScrollArea.ensureWidgetVisible(self.txtDisplay)
        
    
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
        
        self.editBegin.setText(str(self.text.begin + 1))
        self.editEnd.setText(str(self.text.end + 1))
        
        self.setWindowTitle(filename)
        self.displayText()
    
    def displayText(self):
        self.txtDisplay.setText("\n".join([str(i + 1)+" "+self.text.verses[i].text() for i in range(self.text.begin, self.text.end + 1)]))
        self.txtDisplay.setFixedSize(900, 15*(self.text.end - self.text.begin + 2))
    
    def updateBounds(self):
        begin = int(self.editBegin.text()) - 1
        end = int(self.editEnd.text()) - 1
        if begin > end: return
        if begin < 0: return
        if end >= len(self.text.verses): return
        
        self.text.begin = begin
        self.text.end = end
        
        self.displayText()
        self.startSearch()
    
    def startSearch(self):
        if self.text == None: return
        self.editSearch.setText(toGreek(self.editSearch.text()))
        self.text.search(unicode(self.editSearch.text()))
        self.searchResult.setText(str(self.text.numMatch)+u" occurence(s) trouvée(s)")
        
        graph1 = GraphDrawer(self.text, GraphDrawer.plotGlobal)
        graph1.buildGraph()
        self.graph1.setPixmap(graph1.getImage())
        
        graph2 = GraphDrawer(self.text, GraphDrawer.plotPositions)
        graph2.buildGraph()
        self.graph2.setPixmap(graph2.getImage())
        
