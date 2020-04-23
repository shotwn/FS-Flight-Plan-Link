from functools import partial

from PySide2.QtWidgets import (QDialog, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QFileDialog)
from PySide2.QtCore import Qt

from gui.common import GUICommon
from gui.generated.exporterconfig import Ui_ExporterConfig


class ExporterConfig(QDialog, GUICommon):
    def __init__(self, gui_root, exporter, exporter_container=None):
        QDialog.__init__(self)
        GUICommon.__init__(self, gui_root)
        self.exporter = exporter
        self.exporter_container = exporter_container
        self.ui = Ui_ExporterConfig()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle(f"{self.exporter.name} Exporter Options")
        self.drawed_options = {}
        self.draw()

    def add_drawed_options(self, opt_key, get_from, opt_field='value', get_what='text'):
        """Add an option to the self.drawed_options to get fetched and saved when dialog is OK'ed.

        Args:
            opt_key (str): options's key in module.options
            get_from (QWidget): widget to get value from.
            opt_field (str, optional): options's field in module.options. Defaults to 'value'.
            get_what (str, optional): function to call in widget to get value. Defaults to 'text'.
        """
        self.drawed_options[opt_key] = {
            'opt_field': opt_field,
            'get_from': get_from,
            'get_what': get_what
        }

    def collect_and_save_values(self):
        settings_manager = self.gui_root.fslapp.settings
        for key, option in self.drawed_options.items():
            value = getattr(option['get_from'], option['get_what'])()
            settings_manager.set(value, 'exporters', {
                'uuid': self.exporter.uuid
            }, 'options', key, option['opt_field'])

        # This will release an event from exporter, which will update the exporter in main window.
        self.exporter.update_options(settings_manager.get('exporters', {
            'uuid': self.exporter.uuid
        }, 'options'))

        self.done(1)
        if self.exporter_container:
            self.exporter_container.config_window = None

    def folder_selector(self, key, option):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(option.get('label', '')))

        folder_widget = QWidget()
        folder_layout = QHBoxLayout(folder_widget)
        folder_layout.setContentsMargins(0, 0, 0, 0)

        folder_input = QLineEdit()
        folder_input.setText(option.get('dir', option.get('default', '')))
        folder_layout.addWidget(folder_input)

        button = QPushButton('Select')
        button.clicked.connect(partial(self.folder_select, folder_input))
        folder_layout.addWidget(button)

        layout.addWidget(folder_widget)
        self.add_drawed_options(key, folder_input, opt_field='dir')
        return widget

    def folder_select(self, text_input):
        directory = QFileDialog.getExistingDirectory()
        if directory:
            text_input.setText(directory)

    def str_input(self, key, option):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(QLabel(option['label']))
        text_input = QLineEdit(option.get('value', option.get('default', '')))
        layout.addWidget(text_input)
        self.add_drawed_options(key, text_input)
        return widget

    def draw(self):
        if not self.exporter.options:
            label = QLabel('There are options to set for this module.')
            self.ui.config_items.addWidget(label)
        else:
            for key, option in self.exporter.options.items():
                if option['type'] == 'folder':
                    self.ui.config_items.addWidget(self.folder_selector(key, option))
                elif option['type'] == 'str':
                    self.ui.config_items.addWidget(self.str_input(key, option))

            self.ui.config_items.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        if getattr(self.exporter, 'description', False):
            description = QLabel(self.exporter.description)
            self.ui.config_items.addWidget(description)

        self.show()
        return

    def accept(self):
        self.collect_and_save_values()

    def reject(self):
        if self.exporter_container:
            self.exporter_container.config_window = None

        self.done(0)
