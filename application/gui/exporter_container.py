from PySide2.QtWidgets import QWidget
from gui.common import GUICommon
from gui.generated.exporter import Ui_Exporter
from gui.exporter_config import ExporterConfig


class ExporterContainer(QWidget, GUICommon):
    def __init__(self, gui_root, exporter):
        self.exporter = exporter
        self.gui_root = gui_root
        QWidget.__init__(self)
        GUICommon.__init__(self, gui_root)
        self.ui = Ui_Exporter()
        self.ui.setupUi(self)
        self.config_window = None
        self.gui_root.fslapp.server.events.on('exporter_options_updated', self.filter_update)
        self.draw()

    def filter_update(self, updated_exporter):
        if updated_exporter == self.exporter:
            self.draw()

    def draw(self):
        self.ui.module_name.setText(self.exporter.name)

        try:  # In case settings file is corrupted.
            nickname = self.exporter.options['nickname'].get('value', self.exporter.options['nickname']['default'])
            self.ui.exporter_nickname.setText(nickname)
        except KeyError:
            pass

        self.ui.module_method.setText(self.exporter.method)
        self.ui.options_button.clicked.connect(self.show_exporter_config_window)
        self.ui.remove_button.clicked.connect(self.remove_exporter)
        self.ui.export_button.clicked.connect(self.export)

        self.ui.checkBox.setChecked(self.exporter.auto)
        self.ui.checkBox.stateChanged.connect(self.checkbox_triggered)

    def remove_exporter(self):
        self.gui_root.fslapp.server.remove_exporter(self.exporter.uuid)

    def show_exporter_config_window(self):
        if not self.config_window:
            self.config_window = ExporterConfig(self.gui_root, self.exporter, self)

    def checkbox_triggered(self):
        self.exporter.auto = bool(self.ui.checkBox.isChecked())
        self.gui_root.fslapp.settings.set(self.exporter.auto, 'exporters', {'uuid': self.exporter.uuid}, 'auto')

    def export(self):
        self.run_async(self.gui_root.fslapp.server.export, self.gui_root.fslapp.server.active_plan, only_uuids=[self.exporter.uuid])
