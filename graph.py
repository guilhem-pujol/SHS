#!/usr/bin/env python2
# -*- coding: utf-8 -

from PyQt4 import QtGui

def drawRotatedText(painter, x, y, text):
  painter.save();
  painter.translate(x, y);
  painter.rotate(90)
  painter.drawText(0, 0, text);
  painter.restore()


class GraphDrawer:
  plotGlobal = 0
  plotPositions = 1

  def __init__(self, widget):
    self.widget = widget
    self.begin = 0
    self.end = 0
    self.result = [('0', 0)]
    self.image = None
    self.painter = None

  def getPointedVerse(self, x):
    if x <= self.pxX0: return self.begin
    if x > self.pxXmax: return self.end
    return self.begin + (self.end - self.begin) * (x - self.pxX0) / (self.pxXmax - self.pxX0)

  def initParameters(self):
    if self.begin < 0 or self.end >= len(self.result) or self.end < self.begin:
      raise Exception('GraphDrawer: invalid begin/end')

    self.yMax = 0
    self.xLegendMaxLength = 0
    for verseIndex in range(self.begin, self.end + 1):
      self.yMax = max(self.yMax, self.result[verseIndex][1])
      self.xLegendMaxLength = max(self.xLegendMaxLength, len(self.result[verseIndex][0]))

    self.marginLeft = 5
    self.marginRight = 25
    self.marginBottom = 5
    self.marginTop = 15

    self.xLegendHeight = max(10, 8*self.xLegendMaxLength)
    self.yLegendWidth = 30

    self.xMinOffset = 10
    self.yMinOffset = 10

    self.pxXAxis = self.marginLeft + self.yLegendWidth
    self.pxX0 = self.marginLeft + self.yLegendWidth + 5
    self.pxXmax = self.widget.width() - self.marginRight
    self.pxY0 = self.widget.height() - self.marginBottom - self.xLegendHeight
    self.pxYmax = self.marginTop
    self.pxPerVerse = float((self.pxXmax - self.pxX0)) / (self.end - self.begin + 1)

  def buildGraph(self):
    self.initParameters()

    self.image = QtGui.QImage(self.widget.width(), self.widget.height(),
      QtGui.QImage.Format_RGB32)

    white = QtGui.QColor(255, 255, 255)
    black = QtGui.QColor(0, 0, 0)
    red = QtGui.QColor(255, 0, 0)

    self.painter = QtGui.QPainter()
    self.painter.begin(self.image)

    self.painter.setBackground(white)
    self.painter.eraseRect(0, 0, self.widget.width(), self.widget.height())
    self.pxYmax = self.marginTop

    self.painter.setPen(black)
    self.drawAxis()

    self.painter.setPen(red)
    self.drawValues()

    self.painter.end()

    self.widget.setPixmap(QtGui.QPixmap.fromImage(self.image))

  def drawAxis(self):
    # x-axis
    self.painter.drawLine(self.pxXAxis, self.pxY0, self.pxXmax, self.pxY0)

    # y-axis
    self.painter.drawLine(self.pxXAxis, self.pxY0, self.pxXAxis, self.pxYmax)

    # x graduations
    oldX = -self.xMinOffset
    for verseIndex in range(self.begin, self.end + 1):
      x = self.pxX0 + (verseIndex - self.begin) * self.pxPerVerse
      if x >= oldX + self.xMinOffset:
        self.painter.drawLine(x, self.pxY0 - 2, x, self.pxY0 + 2)
        drawRotatedText(self.painter, x, self.pxY0 + 2, self.result[verseIndex][0])
        oldX = x

    # y graduations
    if(self.yMax == 0): return
    oldY = self.widget.height() + self.yMinOffset
    for i in range(self.yMax + 1):
      y = self.pxY0 + i * (self.pxYmax - self.pxY0) / self.yMax
      if y <= oldY - self.yMinOffset:
        self.painter.drawLine(self.pxXAxis - 2, y, self.pxXAxis + 2, y)
        self.painter.drawText(self.pxXAxis - self.yLegendWidth, y + 5, str(i))
        oldY = y

  def drawValues(self):
    if(self.yMax == 0): return

    currentSum = 0
    currentNumber = 0
    previousX = self.pxX0

    for verseIndex in range(self.begin, self.end + 1):
      x = int(self.pxX0 + (verseIndex - self.begin) * self.pxPerVerse)
      if x != previousX:
        y = self.pxY0 + (currentSum * (self.pxYmax - self.pxY0)) / (currentNumber * self.yMax)
        self.painter.drawLine(previousX, self.pxY0, previousX, y)
        currentSum = 0
        currentNumber = 0

      currentSum += self.result[verseIndex][1]
      currentNumber += 1

      if verseIndex == self.end:
        y = self.pxY0 + (currentSum * (self.pxYmax - self.pxY0)) / (currentNumber * self.yMax)
        self.painter.drawLine(x, self.pxY0, x, y)

      previousX = x
