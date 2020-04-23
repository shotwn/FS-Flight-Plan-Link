# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Works\Dev\FS Link\application\gui\ui\exporterconfig.ui',
# licensing of 'D:\Works\Dev\FS Link\application\gui\ui\exporterconfig.ui' applies.
#
# Created: Thu Apr 23 16:07:20 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ExporterConfig(object):
    def setupUi(self, ExporterConfig):
        ExporterConfig.setObjectName("ExporterConfig")
        ExporterConfig.resize(596, 417)
        self.gridLayout_2 = QtWidgets.QGridLayout(ExporterConfig)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(ExporterConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setMaximumSize(QtCore.QSize(16777215, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.config_items = QtWidgets.QVBoxLayout()
        self.config_items.setObjectName("config_items")
        self.gridLayout.addLayout(self.config_items, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(ExporterConfig)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ExporterConfig.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ExporterConfig.reject)
        QtCore.QMetaObject.connectSlotsByName(ExporterConfig)

    def retranslateUi(self, ExporterConfig):
        ExporterConfig.setWindowTitle(QtWidgets.QApplication.translate("ExporterConfig", "Exporter Config", None, -1))

