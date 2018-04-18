# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Lists.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmSpeciesList(object):
    def setupUi(self, frmSpeciesList):
        frmSpeciesList.setObjectName("frmSpeciesList")
        frmSpeciesList.resize(676, 486)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmSpeciesList.sizePolicy().hasHeightForWidth())
        frmSpeciesList.setSizePolicy(sizePolicy)
        frmSpeciesList.setMinimumSize(QtCore.QSize(200, 300))
        frmSpeciesList.setSizeIncrement(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_bird.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmSpeciesList.setWindowIcon(icon)
        self.scrollArea = QtWidgets.QScrollArea(frmSpeciesList)
        self.scrollArea.setGeometry(QtCore.QRect(0, 23, 671, 480))
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
        self.layLists.setGeometry(QtCore.QRect(0, 0, 657, 492))
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
        self.frmRow2 = QtWidgets.QFrame(self.layLists)
        self.frmRow2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmRow2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmRow2.setLineWidth(0)
        self.frmRow2.setObjectName("frmRow2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frmRow2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frmRangeAndDetails = QtWidgets.QFrame(self.frmRow2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmRangeAndDetails.sizePolicy().hasHeightForWidth())
        self.frmRangeAndDetails.setSizePolicy(sizePolicy)
        self.frmRangeAndDetails.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmRangeAndDetails.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmRangeAndDetails.setLineWidth(0)
        self.frmRangeAndDetails.setObjectName("frmRangeAndDetails")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frmRangeAndDetails)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblDateRange = QtWidgets.QLabel(self.frmRangeAndDetails)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblDateRange.setFont(font)
        self.lblDateRange.setLineWidth(0)
        self.lblDateRange.setObjectName("lblDateRange")
        self.verticalLayout.addWidget(self.lblDateRange)
        self.lblDetails = QtWidgets.QLabel(self.frmRangeAndDetails)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.lblDetails.setFont(font)
        self.lblDetails.setLineWidth(0)
        self.lblDetails.setObjectName("lblDetails")
        self.verticalLayout.addWidget(self.lblDetails)
        self.horizontalLayout.addWidget(self.frmRangeAndDetails)
        self.frmLocationButton = QtWidgets.QFrame(self.frmRow2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmLocationButton.sizePolicy().hasHeightForWidth())
        self.frmLocationButton.setSizePolicy(sizePolicy)
        self.frmLocationButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frmLocationButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frmLocationButton.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmLocationButton.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmLocationButton.setLineWidth(0)
        self.frmLocationButton.setObjectName("frmLocationButton")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frmLocationButton)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btnShowLocation = QtWidgets.QPushButton(self.frmLocationButton)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnShowLocation.sizePolicy().hasHeightForWidth())
        self.btnShowLocation.setSizePolicy(sizePolicy)
        self.btnShowLocation.setMinimumSize(QtCore.QSize(100, 20))
        self.btnShowLocation.setStatusTip("")
        self.btnShowLocation.setObjectName("btnShowLocation")
        self.verticalLayout_3.addWidget(self.btnShowLocation)
        self.horizontalLayout.addWidget(self.frmLocationButton)
        self.verticalLayout_2.addWidget(self.frmRow2)
        self.frmRow3 = QtWidgets.QFrame(self.layLists)
        self.frmRow3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmRow3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmRow3.setLineWidth(0)
        self.frmRow3.setObjectName("frmRow3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frmRow3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frmSpecies = QtWidgets.QFrame(self.frmRow3)
        self.frmSpecies.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmSpecies.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmSpecies.setLineWidth(0)
        self.frmSpecies.setObjectName("frmSpecies")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frmSpecies)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblSpecies = QtWidgets.QLabel(self.frmSpecies)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblSpecies.setFont(font)
        self.lblSpecies.setObjectName("lblSpecies")
        self.verticalLayout_4.addWidget(self.lblSpecies)
        self.horizontalLayout_2.addWidget(self.frmSpecies)
        self.frmSpeciesAndFind = QtWidgets.QFrame(self.frmRow3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmSpeciesAndFind.sizePolicy().hasHeightForWidth())
        self.frmSpeciesAndFind.setSizePolicy(sizePolicy)
        self.frmSpeciesAndFind.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frmSpeciesAndFind.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frmSpeciesAndFind.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frmSpeciesAndFind.setLineWidth(0)
        self.frmSpeciesAndFind.setObjectName("frmSpeciesAndFind")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frmSpeciesAndFind)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblFind = QtWidgets.QLabel(self.frmSpeciesAndFind)
        self.lblFind.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblFind.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblFind.setObjectName("lblFind")
        self.horizontalLayout_3.addWidget(self.lblFind)
        self.txtFind = QtWidgets.QLineEdit(self.frmSpeciesAndFind)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtFind.sizePolicy().hasHeightForWidth())
        self.txtFind.setSizePolicy(sizePolicy)
        self.txtFind.setObjectName("txtFind")
        self.horizontalLayout_3.addWidget(self.txtFind)
        self.horizontalLayout_2.addWidget(self.frmSpeciesAndFind)
        self.verticalLayout_2.addWidget(self.frmRow3)
        self.tblList = QtWidgets.QTableWidget(self.layLists)
        self.tblList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tblList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tblList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tblList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblList.setShowGrid(False)
        self.tblList.setObjectName("tblList")
        self.tblList.setColumnCount(0)
        self.tblList.setRowCount(0)
        self.tblList.horizontalHeader().setVisible(False)
        self.tblList.horizontalHeader().setHighlightSections(False)
        self.tblList.verticalHeader().setVisible(False)
        self.tblList.verticalHeader().setDefaultSectionSize(100)
        self.tblList.verticalHeader().setHighlightSections(False)
        self.tblList.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout_2.addWidget(self.tblList)
        self.txtChecklistComments = QtWidgets.QPlainTextEdit(self.layLists)
        self.txtChecklistComments.setObjectName("txtChecklistComments")
        self.verticalLayout_2.addWidget(self.txtChecklistComments)
        self.scrollArea.setWidget(self.layLists)
        self.actionSetDateFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetDateFilter.setObjectName("actionSetDateFilter")
        self.actionSetLocationFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetLocationFilter.setObjectName("actionSetLocationFilter")
        self.actionSetFirstDateFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetFirstDateFilter.setObjectName("actionSetFirstDateFilter")
        self.actionSetLastDateFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetLastDateFilter.setObjectName("actionSetLastDateFilter")
        self.actionSetSpeciesFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetSpeciesFilter.setObjectName("actionSetSpeciesFilter")
        self.actionSetCountryFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetCountryFilter.setObjectName("actionSetCountryFilter")
        self.actionSetStateFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetStateFilter.setObjectName("actionSetStateFilter")
        self.actionSetCountyFilter = QtWidgets.QAction(frmSpeciesList)
        self.actionSetCountyFilter.setObjectName("actionSetCountyFilter")

        self.retranslateUi(frmSpeciesList)
        QtCore.QMetaObject.connectSlotsByName(frmSpeciesList)

    def retranslateUi(self, frmSpeciesList):
        _translate = QtCore.QCoreApplication.translate
        frmSpeciesList.setWindowTitle(_translate("frmSpeciesList", "Species Report"))
        self.lblLocation.setText(_translate("frmSpeciesList", "Location"))
        self.lblDateRange.setText(_translate("frmSpeciesList", "Date Range"))
        self.lblDetails.setText(_translate("frmSpeciesList", "Details Label"))
        self.btnShowLocation.setToolTip(_translate("frmSpeciesList", "Click to show the checklist location."))
        self.btnShowLocation.setText(_translate("frmSpeciesList", "Location"))
        self.lblSpecies.setText(_translate("frmSpeciesList", "Species"))
        self.lblFind.setText(_translate("frmSpeciesList", "Find:  "))
        self.tblList.setSortingEnabled(True)
        self.actionSetDateFilter.setText(_translate("frmSpeciesList", "Set Filter to Date"))
        self.actionSetLocationFilter.setText(_translate("frmSpeciesList", "Set Filter to Location"))
        self.actionSetFirstDateFilter.setText(_translate("frmSpeciesList", "Set Filter to \"First\" Date"))
        self.actionSetLastDateFilter.setText(_translate("frmSpeciesList", "Set Filter to \"Last\" Date"))
        self.actionSetSpeciesFilter.setText(_translate("frmSpeciesList", "Set Filter to Species"))
        self.actionSetCountryFilter.setText(_translate("frmSpeciesList", "Set Filter to Country"))
        self.actionSetStateFilter.setText(_translate("frmSpeciesList", "Set Filter to State"))
        self.actionSetCountyFilter.setText(_translate("frmSpeciesList", "Set Filter to County"))

import icons_rc
