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
        
        self.texts = {}
    
    def setupSignals(self):
        #FIXME: this is the old API style, see how to use new method
        self.textsList.currentItemChanged.connect(self.updateTextDisplay)
        self.editSearch.textEdited.connect(self.startSearch)
        self.editBegin.textEdited.connect(self.updateText)
        self.editEnd.textEdited.connect(self.updateText)
        self.used.toggled.connect(self.updateText)
        self.exitAction.triggered.connect(QtGui.qApp.quit)
        self.openAction.triggered.connect(self.openNewFile)

    def openNewFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
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

        self.updateTextDisplay()

    def currentText(self):
        currentItem = self.textsList.currentItem()
        if currentItem == None:
          return None
        return currentItem.text

    def updateTextDisplay(self):
        currentText = self.currentText()
        if currentText == None:
          #FIXME: disable every input widget
          return

        self.editBegin.setText(str(currentText.begin + 1))
        self.editEnd.setText(str(currentText.end + 1))
        self.used.setChecked(currentText.used)
        self.setWindowTitle(currentText.name)

        #TODO: update the list of texts (bold used text, show verses, ...)
        
        #TODO: maybe move this to the class Text
        #TODO: also, better display of verses numbers
        verses = currentText.verses[currentText.begin:currentText.end+1]
        l = [str(currentText.begin+i+1) + " " + v.text() for (i, v) in enumerate(verses)]
        self.textDisplay.setText("\n".join(l))
    
    def updateText(self):
        currentText = self.currentText()
        if currentText == None:
          #FIXME: if the input widgets are disabled, this shouldn't happen
          return

        begin = int(self.editBegin.text()) - 1
        end = int(self.editEnd.text()) - 1
        used = self.used.isChecked()

        #FIXME: add a validator to the QLineEdit
        if begin > end: return
        if begin < 0: return
        if end >= len(currentText.verses): return
        
        currentText.begin = begin
        currentText.end = end
        currentText.used = used
        
        self.updateTextDisplay()
        #if used: FIXME: add this line when the multi-text search works
        self.startSearch()
    
    def startSearch(self):
        #TODO: multi-text search
        currentText = self.currentText()
        if currentText == None: return
        self.editSearch.setText(toGreek(self.editSearch.text()))
        currentText.search(unicode(self.editSearch.text()))
        self.searchResult.setText(str(currentText.numMatch)+u" occurence(s) trouvée(s)")
        
        graph1 = GraphDrawer(currentText, GraphDrawer.plotGlobal)
        graph1.buildGraph()
        self.graph1.setPixmap(graph1.getImage())
        
        graph2 = GraphDrawer(currentText, GraphDrawer.plotPositions)
        graph2.buildGraph()
        self.graph2.setPixmap(graph2.getImage())
        
