from functools import partial

from PySide2.QtWidgets import (QDialog, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton)

from gui.common import GUICommon
from gui.generated.addexporter import Ui_AddExporter


class AddExporter(QDialog, GUICommon):
    def __init__(self, gui_root):
        QDialog.__init__(self)
        GUICommon.__init__(self, gui_root)
        self.ui = Ui_AddExporter()
        self.ui.setupUi(self)
        self.setWindowTitle('FS Link - Add Exporter Module')
        self.draw()

    def draw(self):
        self.ui.modules.setLayout(QVBoxLayout())
        for key, exporter_module in self.gui_root.fslapp.server.available_exporters.items():
            widget = QWidget()
            widget.setMaximumHeight(40)
            layout = QHBoxLayout(widget)
            layout.addWidget(QLabel(exporter_module.CLASS.name))
            layout.addWidget(QLabel(exporter_module.CLASS.description))

            button = QPushButton('Select')
            button.clicked.connect(partial(self.add_module, key, exporter_module))
            button.setMinimumWidth(80)
            button.setMaximumWidth(80)
            layout.addWidget(button)

            self.ui.modules.layout().addWidget(widget)

        self.ui.modules.layout().addItem(QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.show()

    def add_module(self, module_id, exporter_module):
        self.gui_root.fslapp.server.add_exporter(module_id)
        message = f'| Export module added: {exporter_module.CLASS.name}'

        if message in self.ui.info.text():
            message = f"{self.ui.info.text()}."
        self.ui.info.setText(message)

        if not self.ui.keep_open.isChecked():
            self.accept()

    def accept(self):
        self.done(1)

    def reject(self):
        self.done(0)
