# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Find.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmFind(object):
    def setupUi(self, frmFind):
        frmFind.setObjectName("frmFind")
        frmFind.setWindowModality(QtCore.Qt.ApplicationModal)
        frmFind.resize(414, 421)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmFind.sizePolicy().hasHeightForWidth())
        frmFind.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmFind.setWindowIcon(icon)
        frmFind.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scrollArea = QtWidgets.QScrollArea(frmFind)
        self.scrollArea.setGeometry(QtCore.QRect(9, 9, 365, 418))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 363, 416))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frameMain = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frameMain.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frameMain.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameMain.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameMain.setLineWidth(0)
        self.frameMain.setObjectName("frameMain")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frameMain)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtFind = QtWidgets.QLineEdit(self.frameMain)
        self.txtFind.setObjectName("txtFind")
        self.horizontalLayout.addWidget(self.txtFind)
        self.lblFind = QtWidgets.QLabel(self.frameMain)
        self.lblFind.setObjectName("lblFind")
        self.horizontalLayout.addWidget(self.lblFind)
        self.verticalLayout_4.addWidget(self.frameMain)
        self.lblWhatToSearch = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lblWhatToSearch.setObjectName("lblWhatToSearch")
        self.verticalLayout_4.addWidget(self.lblWhatToSearch)
        self.frame_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frameCheckboxesLeft = QtWidgets.QFrame(self.frame_2)
        self.frameCheckboxesLeft.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameCheckboxesLeft.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameCheckboxesLeft.setLineWidth(0)
        self.frameCheckboxesLeft.setObjectName("frameCheckboxesLeft")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameCheckboxesLeft)
        self.verticalLayout_2.setContentsMargins(-1, 4, -1, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.chkCommonName = QtWidgets.QCheckBox(self.frameCheckboxesLeft)
        self.chkCommonName.setChecked(True)
        self.chkCommonName.setObjectName("chkCommonName")
        self.verticalLayout_2.addWidget(self.chkCommonName)
        self.chkScientificName = QtWidgets.QCheckBox(self.frameCheckboxesLeft)
        self.chkScientificName.setChecked(True)
        self.chkScientificName.setObjectName("chkScientificName")
        self.verticalLayout_2.addWidget(self.chkScientificName)
        self.chkChecklistComments = QtWidgets.QCheckBox(self.frameCheckboxesLeft)
        self.chkChecklistComments.setChecked(True)
        self.chkChecklistComments.setObjectName("chkChecklistComments")
        self.verticalLayout_2.addWidget(self.chkChecklistComments)
        self.chkSpeciesComments = QtWidgets.QCheckBox(self.frameCheckboxesLeft)
        self.chkSpeciesComments.setChecked(True)
        self.chkSpeciesComments.setObjectName("chkSpeciesComments")
        self.verticalLayout_2.addWidget(self.chkSpeciesComments)
        self.horizontalLayout_2.addWidget(self.frameCheckboxesLeft)
        self.frameCheckboxesRight = QtWidgets.QFrame(self.frame_2)
        self.frameCheckboxesRight.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameCheckboxesRight.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameCheckboxesRight.setLineWidth(0)
        self.frameCheckboxesRight.setObjectName("frameCheckboxesRight")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameCheckboxesRight)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chkCountryName = QtWidgets.QCheckBox(self.frameCheckboxesRight)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkCountryName.sizePolicy().hasHeightForWidth())
        self.chkCountryName.setSizePolicy(sizePolicy)
        self.chkCountryName.setChecked(True)
        self.chkCountryName.setObjectName("chkCountryName")
        self.verticalLayout_3.addWidget(self.chkCountryName)
        self.chkStateName = QtWidgets.QCheckBox(self.frameCheckboxesRight)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkStateName.sizePolicy().hasHeightForWidth())
        self.chkStateName.setSizePolicy(sizePolicy)
        self.chkStateName.setChecked(True)
        self.chkStateName.setObjectName("chkStateName")
        self.verticalLayout_3.addWidget(self.chkStateName)
        self.chkCountyName = QtWidgets.QCheckBox(self.frameCheckboxesRight)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkCountyName.sizePolicy().hasHeightForWidth())
        self.chkCountyName.setSizePolicy(sizePolicy)
        self.chkCountyName.setChecked(True)
        self.chkCountyName.setObjectName("chkCountyName")
        self.verticalLayout_3.addWidget(self.chkCountyName)
        self.chkLocationName = QtWidgets.QCheckBox(self.frameCheckboxesRight)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkLocationName.sizePolicy().hasHeightForWidth())
        self.chkLocationName.setSizePolicy(sizePolicy)
        self.chkLocationName.setChecked(True)
        self.chkLocationName.setObjectName("chkLocationName")
        self.verticalLayout_3.addWidget(self.chkLocationName)
        self.horizontalLayout_2.addWidget(self.frameCheckboxesRight)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.frame_5 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_5.setLineWidth(0)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnFind = QtWidgets.QPushButton(self.frame_5)
        self.btnFind.setObjectName("btnFind")
        self.horizontalLayout_3.addWidget(self.btnFind)
        self.btnCancel = QtWidgets.QPushButton(self.frame_5)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.verticalLayout_4.addWidget(self.frame_5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(frmFind)
        QtCore.QMetaObject.connectSlotsByName(frmFind)

    def retranslateUi(self, frmFind):
        _translate = QtCore.QCoreApplication.translate
        frmFind.setWindowTitle(_translate("frmFind", "Species Report"))
        self.lblFind.setText(_translate("frmFind", "Find:"))
        self.lblWhatToSearch.setText(_translate("frmFind", "What to search:"))
        self.chkCommonName.setText(_translate("frmFind", "Species Common Name"))
        self.chkScientificName.setText(_translate("frmFind", "Species Scientific Name"))
        self.chkChecklistComments.setText(_translate("frmFind", "Checklist Comments"))
        self.chkSpeciesComments.setText(_translate("frmFind", "Species Comments"))
        self.chkCountryName.setText(_translate("frmFind", "Country Name"))
        self.chkStateName.setText(_translate("frmFind", "State Name"))
        self.chkCountyName.setText(_translate("frmFind", "County Name"))
        self.chkLocationName.setText(_translate("frmFind", "Location Name"))
        self.btnFind.setText(_translate("frmFind", "Find"))
        self.btnCancel.setText(_translate("frmFind", "Cancel"))

import icons_rc
