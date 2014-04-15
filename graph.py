#!/usr/bin/env python2
# -*- coding: utf-8 -

from PyQt4 import QtGui

class GraphDrawer:
    plotGlobal = 0
    plotPositions = 1
    
    def __init__(self, textList, graphType):
        self.width = 500
        self.height = 200
        
        self.marginLeft = 5
        self.marginRight = 25
        self.marginBottom = 5
        self.marginTop = 15
        
        self.xLegendHeight = 15
        self.yLegendWidth = 30
        
        self.xMinOffset = 0 # redefined by generateData
        self.yMinOffset = 10
        
        self.textList = textList
        self.graphType = graphType
        
        self.image = None
    
    def buildGraph(self):
        if self.graphType == GraphDrawer.plotGlobal:
            self.generateDataGlobal(self.textList[0])
        else:
            self.generateDataPos(self.textList)
        
        self.image = QtGui.QImage(self.width, self.height, 
            QtGui.QImage.Format_RGB32)
            
        white = QtGui.QColor(255, 255, 255)
        black = QtGui.QColor(0, 0, 0)
        red = QtGui.QColor(255, 0, 0)

        self.painter = QtGui.QPainter()
        self.painter.begin(self.image)
        
        self.painter.setBackground(white)
        self.painter.eraseRect(0, 0, self.width, self.height)
        
        if self.yMax == 0:
            self.painter.end()
            return False
        
        self.pxX0 = self.marginLeft + self.yLegendWidth
        self.pxXmax = self.width - self.marginRight
        self.pxY0 = self.height - self.marginBottom - self.xLegendHeight
        self.pxYmax = self.marginTop
        
        self.painter.setPen(black)
        self.drawAxis()
        
        self.painter.setPen(red)
        self.drawValues()
        
        self.painter.end()
    
    def getImage(self):
        if self.image == None: return None
        return QtGui.QPixmap.fromImage(self.image)

    def drawAxis(self):
        # x-axis
        self.painter.drawLine(self.pxX0, self.pxY0, self.pxXmax, self.pxY0)
        
        # y-axis
        self.painter.drawLine(self.pxX0, self.pxY0, self.pxX0, self.pxYmax)
        
        # x graduations
        oldX = -self.xMinOffset
        for i, xVal in enumerate(self.xValues):
            x = self.pxX0 + (i + 1) * (self.pxXmax - self.pxX0) / len(self.xValues)
            if x >= oldX + self.xMinOffset:
                self.painter.drawLine(x, self.pxY0 - 2, x, self.pxY0 + 2)
                self.painter.drawText(x, self.pxY0 + self.xLegendHeight, str(xVal))
                oldX = x
            
        # y graduations
        oldY = self.height + self.yMinOffset
        for i in range(self.yMax + 1):
            y = self.pxY0 + i * (self.pxYmax - self.pxY0) / self.yMax
            if y <= oldY - self.yMinOffset:
                self.painter.drawLine(self.pxX0 - 2, y, self.pxX0 + 2, y)
                self.painter.drawText(self.pxX0 - self.yLegendWidth, y + 5, str(i))
                oldY = y
        
    def drawValues(self):
        for i, yVal in enumerate(self.yValues):
            x = self.pxX0 + (i + 1) * (self.pxXmax - self.pxX0) / len(self.xValues)
            y = self.pxY0 + yVal * (self.pxYmax - self.pxY0) / self.yMax
            self.painter.drawLine(x, self.pxY0, x, y)

    def generateDataGlobal(self, text):
        self.xValues = range(text.begin + 1, text.end + 2)
        self.yValues = [text.verses[x - 1].numMatch for x in self.xValues]
        
        self.xMinOffset = 10 * max([len(str(x)) for x in self.xValues])
        self.yMax = max(self.yValues)
        
    def generateDataPos(self, textList):
        self.xValues = sorted(textList[0].matchByPos.keys())
        self.yValues = [sum([text.matchByPos[x] for text in textList]) for x in self.xValues]
                    
        self.xMinOffset = 10 * max([len(str(x)) for x in self.xValues])
        self.yMax = max(self.yValues)

