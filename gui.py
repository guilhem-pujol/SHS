#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import os
from reader import getFile
from debug import toGreek
from graph import GraphDrawer
from textstructure import Foot
import ui_gui

class TextItem(QtGui.QListWidgetItem):
  def __init__(self, text, fullName, display):
    super(TextItem, self).__init__(text.name)
    self.fullName = fullName
    self.text = text
    self.display = display

class TextDisplay(QtGui.QTableWidget):

  yellow = QtGui.QColor('#ffff82')
  red = QtGui.QColor('#ff6022')

  def __init__(self, text):
    super(TextDisplay, self).__init__()
    self.text = text
    self.setMinimumSize(QtCore.QSize(1020, 0))
    self.setMaximumSize(QtCore.QSize(1020, 16777215))
    self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    self.setRowCount(len(self.text.verses))
    self.setColumnCount(18)
    self.horizontalHeader().setVisible(True)
    self.horizontalHeader().setDefaultSectionSize(54)
    self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
    self.horizontalHeader().resizeSection(0, 86)
    self.setHorizontalHeaderLabels(['', '1', '11', '12',
                                        '2', '21', '22',
                                        '3', '31', '32',
                                        '4', '41', '42',
                                        '5', '51', '52',
                                        '6', '60'])
    self.verticalHeader().setVisible(False)

    self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)

    self.verticalScrollBar().valueChanged.connect(self.update)

    for i in range(self.rowCount()):
      v = self.text.verses[i]
      item = QtGui.QTableWidgetItem(v.name)
      self.setItem(i, 0, item)
      for j in range(6):
        f = v.feet[j]
        if f.metric == Foot.spondee:
          self.setSpan(i, 2+j*3, 1, 2)
          l = 2
        else:
          l = 3
        for k in range(l):
          item = QtGui.QTableWidgetItem(f.syllables[k].text)
          self.setItem(i, 1+j*3+k, item)

  def update(self):
    header = self.verticalHeader()
    start = header.visualIndexAt(0)-1
    end = header.visualIndexAt(self.height())
    if start == -1:
      start = 0
    if end == -1:
      end = self.rowCount() - 1
    self.updateLines(start, end)

  def updateLines(self, start, end):
    for i in range(start, end+1):
      v = self.text.verses[i]
      if v.numMatch > 0:
        background = TextDisplay.yellow
      else:
        background = QtCore.Qt.white
      self.item(i, 0).setBackground(background)
      for j in range(6):
        f = v.feet[j]
        if f.metric == Foot.dactyl:
          l = 3
        else:
          l = 2
        for k in range(l):
          s = f.syllables[k]
          if s.numMatch > 0:
            foreground = TextDisplay.red
          else:
            foreground = QtCore.Qt.black
          item = self.item(i, 1+j*3+k)
          item.setForeground(foreground)
          item.setBackground(background)

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
    filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '', '.png')

    if len(filename) < 4 or filename[-4:].toLower() != '.png':
      filename += '.png'

    graph.pixmap().save(filename)

  def openNewFile(self):
    filename = QtGui.QFileDialog.getOpenFileName(self, 'Ouvrir un fichier',
      os.getenv('HOME'))
    self.loadFile(filename)

  def loadFile(self, filename):
    if filename == '': return None
    #TODO: better handling of this case
    if filename in self.texts: return None

    newText = getFile(filename)
    newDisplay = TextDisplay(newText)
    self.textDisplay.addWidget(newDisplay)
    newItem = TextItem(newText, filename, newDisplay)
    self.texts[filename] = newItem

    self.textsList.addItem(newItem)
    self.textsList.setCurrentItem(newItem)

    self.updateDisplay()

  def updateDisplay(self):
    self.updateCurrentTextDisplay()
    self.startSearch()

  def updateCurrentTextDisplay(self):
    currentItem = self.textsList.currentItem()
    if currentItem == None:
      self.centralWidget.setEnabled(False)
      return
    self.centralWidget.setEnabled(True)
    self.textDisplay.setCurrentWidget(currentItem.display)
    currentText = currentItem.text

    self.editBegin.setText(str(currentText.begin + 1))
    self.editEnd.setText(str(currentText.end + 1))
    self.setWindowTitle(currentText.name)

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

    self.searchResult.setText(str(numMatchFile)+u' occurence(s) trouvée(s)')
    self.textDisplay.currentWidget().update()

    result1 = currentText.result1()
    result2 = currentText.result2()

    self.graphDrawer1.result = result1
    self.graphDrawer1.begin = 0
    self.graphDrawer1.end = len(result1) - 1
    self.graphDrawer2.result = result2
    self.graphDrawer2.begin = 0
    self.graphDrawer2.end = len(result2) - 1
    
    self.graphDrawer1.title = 'Vers - "'+self.editSearch.text()+'" dans '+currentText.name+u' (de à )'
    self.graphDrawer2.title = 'Positions - "'+self.editSearch.text()+'" dans '+currentText.name+u' (de à )'

    self.graphDrawer1.buildGraph()
    self.graphDrawer2.buildGraph()
