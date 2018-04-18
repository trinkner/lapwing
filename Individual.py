# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Individual.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmIndividual(object):
    def setupUi(self, frmIndividual):
        frmIndividual.setObjectName("frmIndividual")
        frmIndividual.resize(780, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmIndividual.sizePolicy().hasHeightForWidth())
        frmIndividual.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_individual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmIndividual.setWindowIcon(icon)
        self.scrollArea = QtWidgets.QScrollArea(frmIndividual)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 780, 500))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 780, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(5, 5, 5, 0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameTop = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTop.sizePolicy().hasHeightForWidth())
        self.frameTop.setSizePolicy(sizePolicy)
        self.frameTop.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frameTop.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameTop.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameTop.setLineWidth(0)
        self.frameTop.setObjectName("frameTop")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frameTop)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frameNames = QtWidgets.QFrame(self.frameTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameNames.sizePolicy().hasHeightForWidth())
        self.frameNames.setSizePolicy(sizePolicy)
        self.frameNames.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frameNames.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameNames.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameNames.setLineWidth(0)
        self.frameNames.setObjectName("frameNames")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameNames)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblCommonName = QtWidgets.QLabel(self.frameNames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCommonName.sizePolicy().hasHeightForWidth())
        self.lblCommonName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblCommonName.setFont(font)
        self.lblCommonName.setWordWrap(True)
        self.lblCommonName.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblCommonName.setObjectName("lblCommonName")
        self.verticalLayout_3.addWidget(self.lblCommonName)
        self.lblScientificName = QtWidgets.QLabel(self.frameNames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblScientificName.sizePolicy().hasHeightForWidth())
        self.lblScientificName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.lblScientificName.setFont(font)
        self.lblScientificName.setWordWrap(True)
        self.lblScientificName.setObjectName("lblScientificName")
        self.verticalLayout_3.addWidget(self.lblScientificName)
        self.lblOrderName = QtWidgets.QLabel(self.frameNames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOrderName.sizePolicy().hasHeightForWidth())
        self.lblOrderName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lblOrderName.setFont(font)
        self.lblOrderName.setWordWrap(True)
        self.lblOrderName.setObjectName("lblOrderName")
        self.verticalLayout_3.addWidget(self.lblOrderName)
        self.lblFirstSeen = QtWidgets.QLabel(self.frameNames)
        self.lblFirstSeen.setWordWrap(True)
        self.lblFirstSeen.setObjectName("lblFirstSeen")
        self.verticalLayout_3.addWidget(self.lblFirstSeen)
        self.lblMostRecentlySeen = QtWidgets.QLabel(self.frameNames)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMostRecentlySeen.sizePolicy().hasHeightForWidth())
        self.lblMostRecentlySeen.setSizePolicy(sizePolicy)
        self.lblMostRecentlySeen.setWordWrap(True)
        self.lblMostRecentlySeen.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblMostRecentlySeen.setObjectName("lblMostRecentlySeen")
        self.verticalLayout_3.addWidget(self.lblMostRecentlySeen)
        self.horizontalLayout.addWidget(self.frameNames)
        self.frameButtons = QtWidgets.QFrame(self.frameTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameButtons.sizePolicy().hasHeightForWidth())
        self.frameButtons.setSizePolicy(sizePolicy)
        self.frameButtons.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frameButtons.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameButtons.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameButtons.setLineWidth(0)
        self.frameButtons.setObjectName("frameButtons")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frameButtons)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.buttonMacaulay = QtWidgets.QPushButton(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonMacaulay.sizePolicy().hasHeightForWidth())
        self.buttonMacaulay.setSizePolicy(sizePolicy)
        self.buttonMacaulay.setObjectName("buttonMacaulay")
        self.verticalLayout_10.addWidget(self.buttonMacaulay)
        self.buttonWikipedia = QtWidgets.QPushButton(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonWikipedia.sizePolicy().hasHeightForWidth())
        self.buttonWikipedia.setSizePolicy(sizePolicy)
        self.buttonWikipedia.setObjectName("buttonWikipedia")
        self.verticalLayout_10.addWidget(self.buttonWikipedia)
        self.buttonAllAboutBirds = QtWidgets.QPushButton(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAllAboutBirds.sizePolicy().hasHeightForWidth())
        self.buttonAllAboutBirds.setSizePolicy(sizePolicy)
        self.buttonAllAboutBirds.setObjectName("buttonAllAboutBirds")
        self.verticalLayout_10.addWidget(self.buttonAllAboutBirds)
        self.buttonAudubon = QtWidgets.QPushButton(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonAudubon.sizePolicy().hasHeightForWidth())
        self.buttonAudubon.setSizePolicy(sizePolicy)
        self.buttonAudubon.setObjectName("buttonAudubon")
        self.verticalLayout_10.addWidget(self.buttonAudubon)
        self.buttonMap = QtWidgets.QPushButton(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonMap.sizePolicy().hasHeightForWidth())
        self.buttonMap.setSizePolicy(sizePolicy)
        self.buttonMap.setObjectName("buttonMap")
        self.verticalLayout_10.addWidget(self.buttonMap)
        self.buttonChecklists = QtWidgets.QPushButton(self.frameButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonChecklists.sizePolicy().hasHeightForWidth())
        self.buttonChecklists.setSizePolicy(sizePolicy)
        self.buttonChecklists.setObjectName("buttonChecklists")
        self.verticalLayout_10.addWidget(self.buttonChecklists)
        self.horizontalLayout.addWidget(self.frameButtons)
        self.verticalLayout.addWidget(self.frameTop)
        self.tabIndividual = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabIndividual.setObjectName("tabIndividual")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblLocations = QtWidgets.QLabel(self.frame)
        self.lblLocations.setObjectName("lblLocations")
        self.verticalLayout_4.addWidget(self.lblLocations)
        self.trLocations = QtWidgets.QTreeWidget(self.frame)
        self.trLocations.setObjectName("trLocations")
        self.trLocations.headerItem().setText(0, "1")
        self.trLocations.header().setVisible(False)
        self.verticalLayout_4.addWidget(self.trLocations)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblDatesForLocation = QtWidgets.QLabel(self.frame_2)
        self.lblDatesForLocation.setObjectName("lblDatesForLocation")
        self.verticalLayout_5.addWidget(self.lblDatesForLocation)
        self.lstDates = QtWidgets.QListWidget(self.frame_2)
        self.lstDates.setObjectName("lstDates")
        self.verticalLayout_5.addWidget(self.lstDates)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.tabIndividual.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.tab_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lblDates = QtWidgets.QLabel(self.frame_3)
        self.lblDates.setObjectName("lblDates")
        self.verticalLayout_6.addWidget(self.lblDates)
        self.trDates = QtWidgets.QTreeWidget(self.frame_3)
        self.trDates.setObjectName("trDates")
        self.trDates.headerItem().setText(0, "1")
        self.trDates.header().setVisible(False)
        self.verticalLayout_6.addWidget(self.trDates)
        self.horizontalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.tab_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setLineWidth(0)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblLocationsForDate = QtWidgets.QLabel(self.frame_4)
        self.lblLocationsForDate.setObjectName("lblLocationsForDate")
        self.verticalLayout_7.addWidget(self.lblLocationsForDate)
        self.tblYearLocations = QtWidgets.QTableWidget(self.frame_4)
        self.tblYearLocations.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblYearLocations.setShowGrid(False)
        self.tblYearLocations.setObjectName("tblYearLocations")
        self.tblYearLocations.setColumnCount(0)
        self.tblYearLocations.setRowCount(0)
        self.verticalLayout_7.addWidget(self.tblYearLocations)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.tabIndividual.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_5 = QtWidgets.QFrame(self.tab_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_5.setLineWidth(0)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lblMonthDates = QtWidgets.QLabel(self.frame_5)
        self.lblMonthDates.setObjectName("lblMonthDates")
        self.verticalLayout_8.addWidget(self.lblMonthDates)
        self.trMonthDates = QtWidgets.QTreeWidget(self.frame_5)
        self.trMonthDates.setObjectName("trMonthDates")
        self.trMonthDates.headerItem().setText(0, "1")
        self.trMonthDates.header().setVisible(False)
        self.verticalLayout_8.addWidget(self.trMonthDates)
        self.horizontalLayout_4.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.tab_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_6.setLineWidth(0)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lblMonthLocationsForDate = QtWidgets.QLabel(self.frame_6)
        self.lblMonthLocationsForDate.setObjectName("lblMonthLocationsForDate")
        self.verticalLayout_9.addWidget(self.lblMonthLocationsForDate)
        self.tblMonthLocations = QtWidgets.QTableWidget(self.frame_6)
        self.tblMonthLocations.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblMonthLocations.setShowGrid(False)
        self.tblMonthLocations.setObjectName("tblMonthLocations")
        self.tblMonthLocations.setColumnCount(0)
        self.tblMonthLocations.setRowCount(0)
        self.verticalLayout_9.addWidget(self.tblMonthLocations)
        self.horizontalLayout_4.addWidget(self.frame_6)
        self.tabIndividual.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabIndividual)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(frmIndividual)
        self.tabIndividual.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frmIndividual)

    def retranslateUi(self, frmIndividual):
        _translate = QtCore.QCoreApplication.translate
        frmIndividual.setWindowTitle(_translate("frmIndividual", "Species Report"))
        self.lblCommonName.setText(_translate("frmIndividual", "Common Name"))
        self.lblScientificName.setText(_translate("frmIndividual", "Scientific Name"))
        self.lblOrderName.setText(_translate("frmIndividual", "Order Name"))
        self.lblFirstSeen.setText(_translate("frmIndividual", "First Seen:"))
        self.lblMostRecentlySeen.setText(_translate("frmIndividual", "Most Recently Seen:"))
        self.buttonMacaulay.setText(_translate("frmIndividual", "Macaulay"))
        self.buttonWikipedia.setText(_translate("frmIndividual", "Wikipedia"))
        self.buttonAllAboutBirds.setText(_translate("frmIndividual", "All About Birds"))
        self.buttonAudubon.setText(_translate("frmIndividual", "Audubon"))
        self.buttonMap.setText(_translate("frmIndividual", "Map"))
        self.buttonChecklists.setText(_translate("frmIndividual", "Checklists"))
        self.lblLocations.setText(_translate("frmIndividual", "Locations"))
        self.lblDatesForLocation.setText(_translate("frmIndividual", "Dates for the selected Locations"))
        self.lstDates.setSortingEnabled(True)
        self.tabIndividual.setTabText(self.tabIndividual.indexOf(self.tab), _translate("frmIndividual", "By Location"))
        self.lblDates.setText(_translate("frmIndividual", "Dates"))
        self.lblLocationsForDate.setText(_translate("frmIndividual", "Locations for the selected date"))
        self.tabIndividual.setTabText(self.tabIndividual.indexOf(self.tab_2), _translate("frmIndividual", "By Year"))
        self.lblMonthDates.setText(_translate("frmIndividual", "Dates"))
        self.lblMonthLocationsForDate.setText(_translate("frmIndividual", "Locations for the selected date"))
        self.tabIndividual.setTabText(self.tabIndividual.indexOf(self.tab_3), _translate("frmIndividual", "By Month"))

import icons_rc
