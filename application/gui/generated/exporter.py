# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Works\Dev\FS Link\application\gui\ui\exporter.ui',
# licensing of 'D:\Works\Dev\FS Link\application\gui\ui\exporter.ui' applies.
#
# Created: Thu Apr 23 16:07:19 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Exporter(object):
    def setupUi(self, Exporter):
        Exporter.setObjectName("Exporter")
        Exporter.resize(681, 38)
        self.gridLayout = QtWidgets.QGridLayout(Exporter)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.checkBox = QtWidgets.QCheckBox(Exporter)
        self.checkBox.setMaximumSize(QtCore.QSize(20, 16777215))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_6.addWidget(self.checkBox)
        self.module_name = QtWidgets.QLabel(Exporter)
        self.module_name.setMinimumSize(QtCore.QSize(110, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.module_name.setFont(font)
        self.module_name.setObjectName("module_name")
        self.horizontalLayout_6.addWidget(self.module_name)
        self.line = QtWidgets.QFrame(Exporter)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_6.addWidget(self.line)
        self.exporter_nickname = QtWidgets.QLabel(Exporter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.exporter_nickname.setFont(font)
        self.exporter_nickname.setObjectName("exporter_nickname")
        self.horizontalLayout_6.addWidget(self.exporter_nickname)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.module_method = QtWidgets.QLabel(Exporter)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.module_method.setFont(font)
        self.module_method.setObjectName("module_method")
        self.horizontalLayout_6.addWidget(self.module_method)
        self.options_button = QtWidgets.QPushButton(Exporter)
        self.options_button.setObjectName("options_button")
        self.horizontalLayout_6.addWidget(self.options_button)
        self.export_button = QtWidgets.QPushButton(Exporter)
        self.export_button.setObjectName("export_button")
        self.horizontalLayout_6.addWidget(self.export_button)
        self.remove_button = QtWidgets.QPushButton(Exporter)
        self.remove_button.setMaximumSize(QtCore.QSize(20, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.remove_button.setFont(font)
        self.remove_button.setObjectName("remove_button")
        self.horizontalLayout_6.addWidget(self.remove_button)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

        self.retranslateUi(Exporter)
        QtCore.QMetaObject.connectSlotsByName(Exporter)

    def retranslateUi(self, Exporter):
        Exporter.setWindowTitle(QtWidgets.QApplication.translate("Exporter", "Form", None, -1))
        self.module_name.setText(QtWidgets.QApplication.translate("Exporter", "Vatsim Prefile", None, -1))
        self.exporter_nickname.setText(QtWidgets.QApplication.translate("Exporter", "VP1", None, -1))
        self.module_method.setText(QtWidgets.QApplication.translate("Exporter", "Browser", None, -1))
        self.options_button.setText(QtWidgets.QApplication.translate("Exporter", "Options", None, -1))
        self.export_button.setText(QtWidgets.QApplication.translate("Exporter", "Export", None, -1))
        self.remove_button.setText(QtWidgets.QApplication.translate("Exporter", "-", None, -1))

