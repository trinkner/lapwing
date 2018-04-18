# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DateTotals.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmDateTotals(object):
    def setupUi(self, frmDateTotals):
        frmDateTotals.setObjectName("frmDateTotals")
        frmDateTotals.resize(676, 486)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmDateTotals.sizePolicy().hasHeightForWidth())
        frmDateTotals.setSizePolicy(sizePolicy)
        frmDateTotals.setMinimumSize(QtCore.QSize(200, 300))
        frmDateTotals.setSizeIncrement(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_datetotals.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmDateTotals.setWindowIcon(icon)
        self.scrollArea = QtWidgets.QScrollArea(frmDateTotals)
        self.scrollArea.setGeometry(QtCore.QRect(0, 23, 671, 451))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.layLists = QtWidgets.QWidget()
        self.layLists.setGeometry(QtCore.QRect(0, 0, 671, 451))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layLists.sizePolicy().hasHeightForWidth())
        self.layLists.setSizePolicy(sizePolicy)
        self.layLists.setObjectName("layLists")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layLists)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblLocation = QtWidgets.QLabel(self.layLists)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblLocation.setFont(font)
        self.lblLocation.setWordWrap(True)
        self.lblLocation.setObjectName("lblLocation")
        self.verticalLayout_2.addWidget(self.lblLocation)
        self.lblDateRange = QtWidgets.QLabel(self.layLists)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblDateRange.setFont(font)
        self.lblDateRange.setLineWidth(0)
        self.lblDateRange.setObjectName("lblDateRange")
        self.verticalLayout_2.addWidget(self.lblDateRange)
        self.lblDetails = QtWidgets.QLabel(self.layLists)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblDetails.setFont(font)
        self.lblDetails.setLineWidth(0)
        self.lblDetails.setObjectName("lblDetails")
        self.verticalLayout_2.addWidget(self.lblDetails)
        self.tabDateTotals = QtWidgets.QTabWidget(self.layLists)
        self.tabDateTotals.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tabDateTotals.setObjectName("tabDateTotals")
        self.tabYear = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabYear.sizePolicy().hasHeightForWidth())
        self.tabYear.setSizePolicy(sizePolicy)
        self.tabYear.setObjectName("tabYear")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabYear)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tblYearTotals = QtWidgets.QTableWidget(self.tabYear)
        self.tblYearTotals.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tblYearTotals.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tblYearTotals.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblYearTotals.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblYearTotals.setObjectName("tblYearTotals")
        self.tblYearTotals.setColumnCount(0)
        self.tblYearTotals.setRowCount(0)
        self.tblYearTotals.horizontalHeader().setVisible(False)
        self.tblYearTotals.horizontalHeader().setHighlightSections(False)
        self.tblYearTotals.verticalHeader().setVisible(False)
        self.tblYearTotals.verticalHeader().setHighlightSections(False)
        self.horizontalLayout_3.addWidget(self.tblYearTotals)
        self.tabDateTotals.addTab(self.tabYear, "")
        self.tabMonth = QtWidgets.QWidget()
        self.tabMonth.setObjectName("tabMonth")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tabMonth)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tblMonthTotals = QtWidgets.QTableWidget(self.tabMonth)
        self.tblMonthTotals.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tblMonthTotals.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblMonthTotals.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblMonthTotals.setObjectName("tblMonthTotals")
        self.tblMonthTotals.setColumnCount(0)
        self.tblMonthTotals.setRowCount(0)
        self.tblMonthTotals.horizontalHeader().setVisible(False)
        self.tblMonthTotals.horizontalHeader().setSortIndicatorShown(True)
        self.tblMonthTotals.verticalHeader().setVisible(False)
        self.tblMonthTotals.verticalHeader().setHighlightSections(False)
        self.tblMonthTotals.verticalHeader().setSortIndicatorShown(False)
        self.tblMonthTotals.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_2.addWidget(self.tblMonthTotals)
        self.tabDateTotals.addTab(self.tabMonth, "")
        self.tabDateTotals_2 = QtWidgets.QWidget()
        self.tabDateTotals_2.setObjectName("tabDateTotals_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tabDateTotals_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tblDateTotals = QtWidgets.QTableWidget(self.tabDateTotals_2)
        self.tblDateTotals.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tblDateTotals.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblDateTotals.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblDateTotals.setObjectName("tblDateTotals")
        self.tblDateTotals.setColumnCount(0)
        self.tblDateTotals.setRowCount(0)
        self.tblDateTotals.horizontalHeader().setVisible(False)
        self.tblDateTotals.horizontalHeader().setDefaultSectionSize(150)
        self.tblDateTotals.horizontalHeader().setHighlightSections(False)
        self.tblDateTotals.horizontalHeader().setSortIndicatorShown(True)
        self.tblDateTotals.verticalHeader().setVisible(False)
        self.tblDateTotals.verticalHeader().setHighlightSections(False)
        self.horizontalLayout.addWidget(self.tblDateTotals)
        self.tabDateTotals.addTab(self.tabDateTotals_2, "")
        self.verticalLayout_2.addWidget(self.tabDateTotals)
        self.scrollArea.setWidget(self.layLists)
        self.actionSetDateFilter = QtWidgets.QAction(frmDateTotals)
        self.actionSetDateFilter.setObjectName("actionSetDateFilter")
        self.actionSetDateFilterToYear = QtWidgets.QAction(frmDateTotals)
        self.actionSetDateFilterToYear.setObjectName("actionSetDateFilterToYear")
        self.actionSetDateFilterToMonth = QtWidgets.QAction(frmDateTotals)
        self.actionSetDateFilterToMonth.setObjectName("actionSetDateFilterToMonth")

        self.retranslateUi(frmDateTotals)
        self.tabDateTotals.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmDateTotals)

    def retranslateUi(self, frmDateTotals):
        _translate = QtCore.QCoreApplication.translate
        frmDateTotals.setWindowTitle(_translate("frmDateTotals", "Species Report"))
        self.lblLocation.setText(_translate("frmDateTotals", "Location"))
        self.lblDateRange.setText(_translate("frmDateTotals", "Date Range"))
        self.lblDetails.setText(_translate("frmDateTotals", "Details Label"))
        self.tblYearTotals.setSortingEnabled(True)
        self.tabDateTotals.setTabText(self.tabDateTotals.indexOf(self.tabYear), _translate("frmDateTotals", "Year"))
        self.tblMonthTotals.setSortingEnabled(True)
        self.tabDateTotals.setTabText(self.tabDateTotals.indexOf(self.tabMonth), _translate("frmDateTotals", "Month"))
        self.tabDateTotals.setTabText(self.tabDateTotals.indexOf(self.tabDateTotals_2), _translate("frmDateTotals", "Date"))
        self.actionSetDateFilter.setText(_translate("frmDateTotals", "Set Filter to Date"))
        self.actionSetDateFilterToYear.setText(_translate("frmDateTotals", "Set Filter To Year"))
        self.actionSetDateFilterToMonth.setText(_translate("frmDateTotals", "Set Filter to Month"))

import icons_rc
