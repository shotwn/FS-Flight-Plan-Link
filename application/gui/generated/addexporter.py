# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Works\Dev\FS Link\application\gui\ui\addexporter.ui',
# licensing of 'D:\Works\Dev\FS Link\application\gui\ui\addexporter.ui' applies.
#
# Created: Thu Apr 23 16:07:19 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddExporter(object):
    def setupUi(self, AddExporter):
        AddExporter.setObjectName("AddExporter")
        AddExporter.resize(721, 300)
        self.gridLayout = QtWidgets.QGridLayout(AddExporter)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(AddExporter)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.modules = QtWidgets.QWidget()
        self.modules.setGeometry(QtCore.QRect(0, 0, 699, 247))
        self.modules.setObjectName("modules")
        self.scrollArea.setWidget(self.modules)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.keep_open = QtWidgets.QCheckBox(AddExporter)
        self.keep_open.setObjectName("keep_open")
        self.horizontalLayout.addWidget(self.keep_open)
        self.info = QtWidgets.QLabel(AddExporter)
        self.info.setText("")
        self.info.setObjectName("info")
        self.horizontalLayout.addWidget(self.info)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddExporter)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(AddExporter)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AddExporter.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AddExporter.reject)
        QtCore.QMetaObject.connectSlotsByName(AddExporter)

    def retranslateUi(self, AddExporter):
        AddExporter.setWindowTitle(QtWidgets.QApplication.translate("AddExporter", "Dialog", None, -1))
        self.keep_open.setText(QtWidgets.QApplication.translate("AddExporter", "Keep this dialog open", None, -1))

