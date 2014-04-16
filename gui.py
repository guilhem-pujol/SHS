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
    
    def setupSignals(self):
        #FIXME: this is the old API style, see how to use new method
        self.textsList.currentItemChanged.connect(self.updateDisplay)
        self.editSearch.textEdited.connect(self.startSearch)
        self.editBegin.textEdited.connect(self.updateText)
        self.editEnd.textEdited.connect(self.updateText)
        self.used.toggled.connect(self.updateText)
        self.exitAction.triggered.connect(QtGui.qApp.quit)
        self.openAction.triggered.connect(self.openNewFile)
        self.selectAll.clicked.connect(self.doSelectAll)
        self.deselectAll.clicked.connect(self.doDeselectAll)
        self.saveGraph1.clicked.connect(self.save1)
        self.saveGraph2.clicked.connect(self.save2)
    
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

    def doSelectAll(self):
        for i in range(len(self.textsList)):
            item = self.textsList.item(i)
            item.text.used = True
        self.updateDisplay()

    def doDeselectAll(self):
        for i in range(len(self.textsList)):
            item = self.textsList.item(i)
            item.text.used = False
        self.updateDisplay()
    
    def updateDisplay(self):
        self.updateCurrentTextDisplay()
        for i in range(len(self.textsList)):
            item = self.textsList.item(i)

            font = item.font()
            font.setBold(item.text.used)
            item.setFont(font)
            if item.text.used:
                name = u'{} ({} à {})'.format(item.text.name, item.text.begin+1,
                    item.text.end+1)
            else:
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
        self.used.setChecked(currentText.used)
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
        used = self.used.isChecked()
        
        currentText.begin = begin
        currentText.end = end
        currentText.used = used
        
        self.updateDisplay()
        #if used: FIXME: add this line when the multi-text search works
        self.startSearch()
    
    def startSearch(self):
        #TODO: multi-text search
        currentItem = self.textsList.currentItem()
        if currentItem == None: return
        currentText = currentItem.text
        
        if len(self.editSearch.text()) == 0: return
        
        textList = [self.textsList.item(i).text for i in range(len(self.textsList)) if self.textsList.item(i).text.used]
        
        self.editSearch.setText(toGreek(self.editSearch.text()))
        query = unicode(self.editSearch.text())
        numMatchAll = 0
        for text in textList:
            numMatchAll += text.search(query)
        if not currentText.used:
            currentText.search(query)
        numMatchFile = currentText.numMatch
            
        self.searchResult.setText(str(numMatchAll)+u" occurence(s) trouvée(s) dans la sélection, "+str(numMatchFile)+u" occurence(s) trouvée(s) dans ce fichier")
        self.textDisplay.setHtml(currentText.html(True))
        
        graph1 = GraphDrawer([currentText], GraphDrawer.plotGlobal)
        graph1.buildGraph()
        self.graph1.setPixmap(graph1.getImage())
        graph2 = GraphDrawer([self.textsList.item(i).text for i in range(len(self.textsList)) if self.textsList.item(i).text.used], GraphDrawer.plotPositions)
        graph2.buildGraph()
        self.graph2.setPixmap(graph2.getImage())
        
