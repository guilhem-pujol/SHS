# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Mon May 19 18:01:44 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1240, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1240, 800))
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setEnabled(False)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setContentsMargins(2, -1, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.leftSide = QtGui.QWidget(self.centralWidget)
        self.leftSide.setMinimumSize(QtCore.QSize(206, 190))
        self.leftSide.setMaximumSize(QtCore.QSize(206, 16777215))
        self.leftSide.setObjectName(_fromUtf8("leftSide"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.leftSide)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.textsList = QtGui.QListWidget(self.leftSide)
        self.textsList.setMinimumSize(QtCore.QSize(200, 0))
        self.textsList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textsList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.textsList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.textsList.setObjectName(_fromUtf8("textsList"))
        self.verticalLayout_2.addWidget(self.textsList)
        self.horizontalLayout_3.addWidget(self.leftSide)
        self.rightSide = QtGui.QWidget(self.centralWidget)
        self.rightSide.setObjectName(_fromUtf8("rightSide"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.rightSide)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.bar1 = QtGui.QWidget(self.rightSide)
        self.bar1.setMinimumSize(QtCore.QSize(0, 50))
        self.bar1.setMaximumSize(QtCore.QSize(16777215, 50))
        self.bar1.setObjectName(_fromUtf8("bar1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.bar1)
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.textSearch = QtGui.QLabel(self.bar1)
        self.textSearch.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textSearch.sizePolicy().hasHeightForWidth())
        self.textSearch.setSizePolicy(sizePolicy)
        self.textSearch.setMinimumSize(QtCore.QSize(0, 0))
        self.textSearch.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.textSearch.setObjectName(_fromUtf8("textSearch"))
        self.horizontalLayout_2.addWidget(self.textSearch)
        self.editSearch = QtGui.QLineEdit(self.bar1)
        self.editSearch.setMinimumSize(QtCore.QSize(0, 0))
        self.editSearch.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.editSearch.setObjectName(_fromUtf8("editSearch"))
        self.horizontalLayout_2.addWidget(self.editSearch)
        self.textFrom = QtGui.QLabel(self.bar1)
        self.textFrom.setMinimumSize(QtCore.QSize(50, 30))
        self.textFrom.setMaximumSize(QtCore.QSize(50, 30))
        self.textFrom.setObjectName(_fromUtf8("textFrom"))
        self.horizontalLayout_2.addWidget(self.textFrom)
        self.editBegin = QtGui.QLineEdit(self.bar1)
        self.editBegin.setMinimumSize(QtCore.QSize(100, 30))
        self.editBegin.setMaximumSize(QtCore.QSize(100, 30))
        self.editBegin.setText(_fromUtf8(""))
        self.editBegin.setObjectName(_fromUtf8("editBegin"))
        self.horizontalLayout_2.addWidget(self.editBegin)
        self.textTo = QtGui.QLabel(self.bar1)
        self.textTo.setMinimumSize(QtCore.QSize(80, 30))
        self.textTo.setMaximumSize(QtCore.QSize(80, 30))
        self.textTo.setObjectName(_fromUtf8("textTo"))
        self.horizontalLayout_2.addWidget(self.textTo)
        self.editEnd = QtGui.QLineEdit(self.bar1)
        self.editEnd.setMinimumSize(QtCore.QSize(100, 30))
        self.editEnd.setMaximumSize(QtCore.QSize(100, 30))
        self.editEnd.setObjectName(_fromUtf8("editEnd"))
        self.horizontalLayout_2.addWidget(self.editEnd)
        self.resetRange = QtGui.QPushButton(self.bar1)
        self.resetRange.setMinimumSize(QtCore.QSize(50, 0))
        self.resetRange.setMaximumSize(QtCore.QSize(50, 16777215))
        self.resetRange.setObjectName(_fromUtf8("resetRange"))
        self.horizontalLayout_2.addWidget(self.resetRange)
        self.searchResult = QtGui.QLabel(self.bar1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchResult.sizePolicy().hasHeightForWidth())
        self.searchResult.setSizePolicy(sizePolicy)
        self.searchResult.setMinimumSize(QtCore.QSize(400, 0))
        self.searchResult.setMaximumSize(QtCore.QSize(400, 16777215))
        self.searchResult.setText(_fromUtf8(""))
        self.searchResult.setObjectName(_fromUtf8("searchResult"))
        self.horizontalLayout_2.addWidget(self.searchResult)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.setStretch(8, 1)
        self.verticalLayout_5.addWidget(self.bar1)
        self.bar2 = QtGui.QWidget(self.rightSide)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bar2.sizePolicy().hasHeightForWidth())
        self.bar2.setSizePolicy(sizePolicy)
        self.bar2.setMinimumSize(QtCore.QSize(1020, 320))
        self.bar2.setMaximumSize(QtCore.QSize(16777215, 320))
        self.bar2.setObjectName(_fromUtf8("bar2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.bar2)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.colGraph1 = QtGui.QWidget(self.bar2)
        self.colGraph1.setObjectName(_fromUtf8("colGraph1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.colGraph1)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.graph1 = QtGui.QLabel(self.colGraph1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph1.sizePolicy().hasHeightForWidth())
        self.graph1.setSizePolicy(sizePolicy)
        self.graph1.setMinimumSize(QtCore.QSize(500, 300))
        self.graph1.setMaximumSize(QtCore.QSize(500, 300))
        self.graph1.setObjectName(_fromUtf8("graph1"))
        self.verticalLayout_4.addWidget(self.graph1)
        self.saveGraph1 = QtGui.QPushButton(self.colGraph1)
        self.saveGraph1.setObjectName(_fromUtf8("saveGraph1"))
        self.verticalLayout_4.addWidget(self.saveGraph1)
        self.horizontalLayout.addWidget(self.colGraph1)
        self.colGraph2 = QtGui.QWidget(self.bar2)
        self.colGraph2.setMinimumSize(QtCore.QSize(0, 250))
        self.colGraph2.setObjectName(_fromUtf8("colGraph2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.colGraph2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.graph2 = QtGui.QLabel(self.colGraph2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graph2.sizePolicy().hasHeightForWidth())
        self.graph2.setSizePolicy(sizePolicy)
        self.graph2.setMinimumSize(QtCore.QSize(500, 300))
        self.graph2.setMaximumSize(QtCore.QSize(500, 300))
        self.graph2.setObjectName(_fromUtf8("graph2"))
        self.verticalLayout.addWidget(self.graph2)
        self.saveGraph2 = QtGui.QPushButton(self.colGraph2)
        self.saveGraph2.setObjectName(_fromUtf8("saveGraph2"))
        self.verticalLayout.addWidget(self.saveGraph2)
        self.horizontalLayout.addWidget(self.colGraph2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_5.addWidget(self.bar2)
        self.textDisplay = QtGui.QStackedWidget(self.rightSide)
        self.textDisplay.setObjectName(_fromUtf8("textDisplay"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.textDisplay.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.textDisplay.addWidget(self.page_2)
        self.verticalLayout_5.addWidget(self.textDisplay)
        self.horizontalLayout_3.addWidget(self.rightSide)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1240, 27))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menuBar)
        self.openAction = QtGui.QAction(MainWindow)
        self.openAction.setObjectName(_fromUtf8("openAction"))
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName(_fromUtf8("exitAction"))
        self.menuFile.addAction(self.openAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.exitAction)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Analyse fréquentielle de textes", None))
        self.textSearch.setText(_translate("MainWindow", "Motif :", None))
        self.textFrom.setText(_translate("MainWindow", "Du vers", None))
        self.textTo.setText(_translate("MainWindow", "jusqu\'au vers", None))
        self.resetRange.setText(_translate("MainWindow", "Reset", None))
        self.graph1.setText(_translate("MainWindow", "Graphe 1", None))
        self.saveGraph1.setText(_translate("MainWindow", "Sauvegarder", None))
        self.graph2.setText(_translate("MainWindow", "Graphe 2", None))
        self.saveGraph2.setText(_translate("MainWindow", "Sauvegarder", None))
        self.menuFile.setTitle(_translate("MainWindow", "&Fichier", None))
        self.openAction.setText(_translate("MainWindow", "&Ouvrir", None))
        self.openAction.setStatusTip(_translate("MainWindow", "Ouvrir un fichier", None))
        self.openAction.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.exitAction.setText(_translate("MainWindow", "&Quitter", None))
        self.exitAction.setStatusTip(_translate("MainWindow", "Quitter le programme", None))
        self.exitAction.setShortcut(_translate("MainWindow", "Ctrl+W", None))

