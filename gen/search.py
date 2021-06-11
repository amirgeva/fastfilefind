# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/search.ui'
#
#
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(595, 549)
        Dialog.searchTerm = QtWidgets.QLineEdit(Dialog)
        Dialog.searchTerm.setGeometry(QtCore.QRect(160, 16, 209, 33))
        Dialog.searchTerm.setObjectName(_fromUtf8("searchTerm"))
        Dialog.SearchTermLabel = QtWidgets.QLabel(Dialog)
        Dialog.SearchTermLabel.setGeometry(QtCore.QRect(32, 16, 113, 33))
        Dialog.SearchTermLabel.setObjectName(_fromUtf8("SearchTermLabel"))
        Dialog.SearchTermLabel_2 = QtWidgets.QLabel(Dialog)
        Dialog.SearchTermLabel_2.setGeometry(QtCore.QRect(32, 48, 113, 33))
        Dialog.SearchTermLabel_2.setObjectName(_fromUtf8("SearchTermLabel_2"))
        Dialog.extensionName = QtWidgets.QLineEdit(Dialog)
        Dialog.extensionName.setGeometry(QtCore.QRect(160, 54, 209, 32))
        Dialog.extensionName.setObjectName(_fromUtf8("extensionName"))
        Dialog.sizeType = QtWidgets.QComboBox(Dialog)
        Dialog.sizeType.setGeometry(QtCore.QRect(32, 96, 113, 33))
        Dialog.sizeType.setObjectName(_fromUtf8("sizeType"))
        Dialog.sizeType.addItem(_fromUtf8(""))
        Dialog.sizeType.addItem(_fromUtf8(""))
        Dialog.sizeType.addItem(_fromUtf8(""))
        Dialog.sizeEdit = QtWidgets.QLineEdit(Dialog)
        Dialog.sizeEdit.setEnabled(False)
        Dialog.sizeEdit.setGeometry(QtCore.QRect(160, 96, 129, 33))
        Dialog.sizeEdit.setObjectName(_fromUtf8("sizeEdit"))
        Dialog.smallButton = QtWidgets.QPushButton(Dialog)
        Dialog.smallButton.setGeometry(QtCore.QRect(304, 96, 81, 33))
        Dialog.smallButton.setObjectName(_fromUtf8("smallButton"))
        Dialog.largeButton = QtWidgets.QPushButton(Dialog)
        Dialog.largeButton.setGeometry(QtCore.QRect(396, 96, 81, 32))
        Dialog.largeButton.setObjectName(_fromUtf8("largeButton"))
        Dialog.SearchTermLabel_3 = QtWidgets.QLabel(Dialog)
        Dialog.SearchTermLabel_3.setGeometry(QtCore.QRect(32, 144, 81, 33))
        Dialog.SearchTermLabel_3.setObjectName(_fromUtf8("SearchTermLabel_3"))
        Dialog.dateType = QtWidgets.QComboBox(Dialog)
        Dialog.dateType.setGeometry(QtCore.QRect(128, 144, 113, 33))
        Dialog.dateType.setObjectName(_fromUtf8("dateType"))
        Dialog.dateType.addItem(_fromUtf8(""))
        Dialog.dateType.addItem(_fromUtf8(""))
        Dialog.dateType.addItem(_fromUtf8(""))
        Dialog.dateEdit = QtWidgets.QLineEdit(Dialog)
        Dialog.dateEdit.setEnabled(False)
        Dialog.dateEdit.setGeometry(QtCore.QRect(256, 144, 113, 33))
        Dialog.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        Dialog.recentButton = QtWidgets.QPushButton(Dialog)
        Dialog.recentButton.setGeometry(QtCore.QRect(384, 144, 93, 33))
        Dialog.recentButton.setObjectName(_fromUtf8("recentButton"))
        Dialog.SearchTermLabel_4 = QtWidgets.QLabel(Dialog)
        Dialog.SearchTermLabel_4.setGeometry(QtCore.QRect(32, 192, 145, 33))
        Dialog.SearchTermLabel_4.setObjectName(_fromUtf8("SearchTermLabel_4"))
        Dialog.baseEdit = QtWidgets.QLineEdit(Dialog)
        Dialog.baseEdit.setGeometry(QtCore.QRect(176, 192, 369, 33))
        Dialog.baseEdit.setObjectName(_fromUtf8("baseEdit"))
        Dialog.resultsList = QtWidgets.QTableView(Dialog)
        Dialog.resultsList.setGeometry(QtCore.QRect(0, 288, 593, 257))
        Dialog.resultsList.setShowGrid(False)
        Dialog.resultsList.setObjectName(_fromUtf8("resultsList"))
        Dialog.searchButton = QtWidgets.QPushButton(Dialog)
        Dialog.searchButton.setGeometry(QtCore.QRect(496, 16, 97, 33))
        Dialog.searchButton.setDefault(True)
        Dialog.searchButton.setObjectName(_fromUtf8("searchButton"))
        Dialog.resultsEdit = QtWidgets.QLineEdit(Dialog)
        Dialog.resultsEdit.setGeometry(QtCore.QRect(208, 240, 129, 32))
        Dialog.resultsEdit.setReadOnly(True)
        Dialog.resultsEdit.setObjectName(_fromUtf8("resultsEdit"))
        Dialog.label = QtWidgets.QLabel(Dialog)
        Dialog.label.setGeometry(QtCore.QRect(32, 240, 177, 33))
        Dialog.label.setObjectName(_fromUtf8("label"))
        Dialog.resetButton = QtWidgets.QPushButton(Dialog)
        Dialog.resetButton.setGeometry(QtCore.QRect(352, 240, 97, 32))
        Dialog.resetButton.setObjectName(_fromUtf8("resetButton"))
        Dialog.exactCB = QtWidgets.QCheckBox(Dialog)
        Dialog.exactCB.setGeometry(QtCore.QRect(384, 16, 97, 27))
        Dialog.exactCB.setObjectName(_fromUtf8("exactCB"))

        self.retranslateUi(Dialog)
        Dialog.sizeType.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        Dialog.searchTerm.setToolTip(_translate("Dialog", "Search Term", None))
        Dialog.SearchTermLabel.setText(_translate("Dialog", "Search Term", None))
        Dialog.SearchTermLabel_2.setText(_translate("Dialog", "Extension:", None))
        Dialog.extensionName.setToolTip(_translate("Dialog", "Search Term", None))
        Dialog.sizeType.setItemText(0, _translate("Dialog", "Any Size", None))
        Dialog.sizeType.setItemText(1, _translate("Dialog", "Less Than", None))
        Dialog.sizeType.setItemText(2, _translate("Dialog", "More Than", None))
        Dialog.smallButton.setText(_translate("Dialog", "Small", None))
        Dialog.largeButton.setText(_translate("Dialog", "Large", None))
        Dialog.SearchTermLabel_3.setText(_translate("Dialog", "Modified:", None))
        Dialog.dateType.setItemText(0, _translate("Dialog", "Any Time", None))
        Dialog.dateType.setItemText(1, _translate("Dialog", "Before", None))
        Dialog.dateType.setItemText(2, _translate("Dialog", "After", None))
        Dialog.recentButton.setText(_translate("Dialog", "Recent", None))
        Dialog.SearchTermLabel_4.setText(_translate("Dialog", "Base Directory:", None))
        Dialog.searchButton.setText(_translate("Dialog", "Search", None))
        Dialog.label.setText(_translate("Dialog", "Number of Results:", None))
        Dialog.resetButton.setText(_translate("Dialog", "Reset", None))
        Dialog.exactCB.setText(_translate("Dialog", "Exact", None))

