#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import os
from reader import getFile
from debug import toGreek
from graph import GraphDrawer
import ui_gui

class TextItem(QtGui.QListWidgetItem):
    def __init__(self, text, fullName):
        super(TextItem, self).__init__(text.name)
        self.fullName = fullName
        self.text = text

class mainWindow(QtGui.QMainWindow, ui_gui.Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setupUi(self)
        self.setupSignals()
        
        #FIXME: not sure this attribute is useful
        self.texts = {}
        
        self.graphDrawer1 = GraphDrawer(self.graph1)
        self.graphDrawer2 = GraphDrawer(self.graph2)
    
    def setupSignals(self):
        #FIXME: this is the old API style, see how to use new method
        self.textsList.currentItemChanged.connect(self.updateDisplay)
        self.editSearch.textEdited.connect(self.startSearch)
        self.editBegin.textEdited.connect(self.updateText)
        self.editEnd.textEdited.connect(self.updateText)
        self.exitAction.triggered.connect(QtGui.qApp.quit)
        self.openAction.triggered.connect(self.openNewFile)
        self.saveGraph1.clicked.connect(self.save1)
        self.saveGraph2.clicked.connect(self.save2)
        self.graph1.wheelEvent = self.graphZoomHandler
        
    def graphZoomHandler(self, wheelEvent):
        if wheelEvent.delta() > 0:
          zoomFactor = 2.0
        else:
          zoomFactor = 0.5
        
        verseIndex = self.graphDrawer1.getPointedVerse(wheelEvent.x())
        n = (self.graphDrawer1.end - self.graphDrawer1.begin) + 1
        newBegin = verseIndex - (1 + n / 2) / zoomFactor
        newEnd = verseIndex + (1 + n / 2) / zoomFactor
        if newBegin < 0: newBegin = 0
        if newEnd >= len(self.graphDrawer1.result): newEnd = len(self.graphDrawer1.result) - 1

        self.graphDrawer1.begin = int(newBegin)
        self.graphDrawer1.end = int(newEnd)
        self.graphDrawer1.buildGraph()
    
    def save1(self):
        self.save(self.graph1)
    
    def save2(self):
        self.save(self.graph2)
        
    def save(self, graph):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", ".png")
        
        if len(filename) < 4 or filename[-4:].toLower() != ".png":
            filename += ".png"
        
        graph.pixmap().save(filename)
        
    def openNewFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Ouvrir un fichier',
            os.getenv('HOME'))
        self.loadFile(filename)
    
    def loadFile(self, filename):
        if filename == "": return None
        #TODO: better handling of this case
        if filename in self.texts: return None
        
        newText = getFile(filename)
        newItem = TextItem(newText, filename)
        self.texts[filename] = newItem
        
        self.textsList.addItem(newItem)
        self.textsList.setCurrentItem(newItem)
        
        self.updateDisplay()

    def updateDisplay(self):
        self.updateCurrentTextDisplay()
        for i in range(len(self.textsList)):
            item = self.textsList.item(i)

            font = item.font()
            item.setFont(font)
            name = u'{}'.format(item.text.name)
            item.setText(name)
        self.startSearch()

    def updateCurrentTextDisplay(self):
        currentItem = self.textsList.currentItem()
        if currentItem == None:
          self.centralWidget.setEnabled(False)
          return
        self.centralWidget.setEnabled(True)
        currentText = currentItem.text

        self.editBegin.setText(str(currentText.begin + 1))
        self.editEnd.setText(str(currentText.end + 1))
        self.setWindowTitle(currentText.name)
        
        #TODO: maybe move this to the class Text
        #TODO: also, better display of verses numbers
        self.textDisplay.setHtml(currentText.html(True))
    
    def updateText(self):
        currentText = self.textsList.currentItem().text
        if self.editBegin.text() == '' or self.editEnd.text() == '':
          return
        begin, bok = self.editBegin.text().toInt()
        end, eok = self.editEnd.text().toInt()
        if not bok or not eok: return
        begin -= 1
        end -= 1
        if end >= len(currentText.verses): return
        if begin > end: return
        
        currentText.begin = begin
        currentText.end = end
        
        self.updateDisplay()
        self.startSearch()
    
    def startSearch(self):
        currentItem = self.textsList.currentItem()
        if currentItem == None: return
        currentText = currentItem.text
        
        if len(self.editSearch.text()) == 0: return
        
        self.editSearch.setText(toGreek(self.editSearch.text()))
        query = unicode(self.editSearch.text())
        
        currentText.search(query)
        numMatchFile = currentText.numMatch
            
        self.searchResult.setText(str(numMatchFile)+u" occurence(s) trouvée(s)")
        self.textDisplay.setHtml(currentText.html(True))
      
        result1 = [("verseId", 100), ("otherverseId", 42)]
        result2 = [("posId", 1)]
        
        self.graphDrawer1.result = result1
        self.graphDrawer1.begin = 0
        self.graphDrawer1.end = len(result1) - 1
        self.graphDrawer2.result = result2
        self.graphDrawer2.begin = 0
        self.graphDrawer2.end = len(result2) - 1
        
        self.graphDrawer1.buildGraph()
        self.graphDrawer2.buildGraph()
        
