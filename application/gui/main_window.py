from datetime import datetime, timedelta
from functools import partial
import re
from loguru import logger
from PySide2.QtWidgets import QMainWindow, QSizePolicy, QSpacerItem
from PySide2.QtCore import Qt, QTime, QDate, QAbstractTableModel

from server.plan import Plan
import server.exceptions
from gui.generated.mainwindow import Ui_MainWindow

from gui.common import GUICommon
from gui.exporter_container import ExporterContainer
from gui.add_exporter import AddExporter


class AdditionalItemsTableModel(QAbstractTableModel):  # TODO Tables tables tables...
    def __init__(self, data, **kwargs):
        super().__init__()
        self._data = list(data.items())
        self._headers = kwargs.get('headers', [])
        print(self._data)

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role):
        print(index)
        print(value)
        return True

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                try:
                    return self._headers[section]
                except (KeyError, IndexError):
                    return None


class MainWindow(QMainWindow, GUICommon):
    def __init__(self, gui_root):
        QMainWindow.__init__(self)
        GUICommon.__init__(self, gui_root)
        self.populated_plan = None
        self.style_sheet_modified = []

        self.gui_root = gui_root
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.add_module_dialog = None

        self.ui.update_button.clicked.connect(self.update_populated_plan)
        self.ui.update_button.setEnabled(False)

        self.ui.revert_button.clicked.connect(self.revert_changes)
        # Until ui is cleaned..
        self.revert_changes()

        self.ui.new_button.clicked.connect(self.empty)
        self.ui.activate_button.clicked.connect(self.activate)
        self.ui.export_module_add_button.clicked.connect(self.add_export_module)
        self.bind_text_edit_slots()

    def bind_text_edit_slots(self):
        line_edits_upper = [
            'callsign',
            'departure',
            'destination',
            'alternate',
            'departure',
            'sid',
            'star',
            'destination',
            'aircraft',
            'airline',
            'flight_code',
            'equipment',
            'equipment_suffix',
            'pilot_base'
        ]

        line_edits_number = [
            'cruise_altitude',
            'cruise_speed',
            'distance',
            'pax',
            'cargo',
            'zfw',
            'block_fuel',
            'tow'
        ]

        for line_edit in line_edits_upper:
            ui_elem = getattr(self.ui, line_edit)
            ui_elem.textEdited.connect(partial(self.text_edited_upper, ui_elem))

        for line_edit in line_edits_number:
            ui_elem = getattr(self.ui, line_edit)
            ui_elem.textEdited.connect(partial(self.text_edited_number, ui_elem))

    def text_edited_upper(self, to, new_text):
        to.setText(new_text.upper())

    def text_edited_number(self, to, new_text):
        to.setText(re.sub(r"\D", "", new_text))

    def set_populated_plan(self, plan):
        self.populated_plan = plan
        if plan is None:
            self.ui.update_button.setEnabled(False)
            self.ui.activate_button.setEnabled(True)
            self.ui.top_label.setText('Creating New Flight Plan')
        else:
            self.ui.update_button.setEnabled(True)
            self.ui.activate_button.setEnabled(False)
            self.ui.top_label.setText(f"Active Plan: {plan['callsign']} - {plan['departure']} {plan['destination']}")

    def populate_plan(self, plan):
        # Written openly, without any clever mapping.
        self.ui.callsign.setText(plan.get('callsign', ''))

        self.ui.departure.setText(plan['departure'])
        self.ui.destination.setText(plan['destination'])
        self.ui.alternate.setText(plan.get('alternate', ''))

        now = datetime.utcnow()

        dep_time_h = plan.get_nested_dict('departure_time', 'hours', default=now.hour)
        dep_time_m = plan.get_nested_dict('departure_time', 'minutes', default=now.minute)
        dep_time = QTime(dep_time_h, dep_time_m)
        self.ui.departure_time.setTime(dep_time)

        dep_date_d = plan.get_nested_dict('departure_date', 'day', default=now.day)
        dep_date_m = plan.get_nested_dict('departure_date', 'month', default=now.month)
        dep_date_y = plan.get_nested_dict('departure_date', 'year', default=now.year)

        self.ui.departure_date.setDate(QDate(dep_date_y, dep_date_m, dep_date_d))

        self.ui.route.setPlainText(plan.route_to_str(include_sid_star=False))

        self.ui.departure_runway.setText(plan.get('departure_runway', ''))
        self.ui.sid.setText(plan.get_nested_dict('sid', 'name', default=''))
        self.ui.cruise_altitude.setText(str(plan.get('cruise_altitude', '')))
        self.ui.cruise_speed.setText(str(plan.get('cruise_speed', '')))
        self.ui.star.setText(plan.get_nested_dict('star', 'name', default=''))
        self.ui.destination_runway.setText(plan.get('destination_runway', ''))

        self.ui.aircraft.setText(plan.get('aircraft', ''))
        self.ui.airline.setText(plan.get('airline', ''))
        self.ui.flight_code.setText(plan.get('flight_code', ''))

        self.ui.distance.setText(str(plan.get('distance', '')))
        self.ui.block_time.setTime(QTime(plan.get_nested_dict('block_time', 'hours', default=0), plan.get_nested_dict('block_time', 'minutes', default=0)))

        self.ui.equipment.setText(plan.get('equipment', ''))
        self.ui.equipment_suffix.setText(plan.get('equipment_suffix', ''))

        self.ui.pax.setText(str(plan.get('pax', '')))
        self.ui.cargo.setText(str(plan.get('cargo', '')))
        self.ui.zfw.setText(str(plan.get('zfw', '')))

        self.ui.remarks.setPlainText(plan.get('remarks', ''))
        self.ui.fuel_endurance.setTime(QTime(plan.get_nested_dict('fuel_endurance', 'hours', default=00), plan.get_nested_dict('fuel_endurance', 'minutes', default=00)))
        self.ui.block_fuel.setText(str(plan.get('block_fuel', '')))

        self.ui.tow.setText(str(plan.get('tow', '')))

        pilot_name_def = self.gui_root.fslapp.settings.get('pilot', 'name')
        pilot_base_def = self.gui_root.fslapp.settings.get('pilot', 'base')
        self.ui.pilot_name.setText(plan.get_nested_dict('pilot', 'name', default=pilot_name_def))
        self.ui.pilot_base.setText(plan.get_nested_dict('pilot', 'base', default=pilot_base_def))

        model = AdditionalItemsTableModel({
            'air_time': plan.get('air_time', '')
        })
        self.ui.additional.setModel(model)

        self.set_populated_plan(plan)
        self.reset_style_sheets()

    def empty(self):
        self.ui.callsign.setText('')

        self.ui.departure.setText('')
        self.ui.destination.setText('')
        self.ui.alternate.setText('')

        now = datetime.utcnow()
        slight_future = now + timedelta(minutes=20)
        self.ui.departure_time.setTime(QTime(slight_future.hour, slight_future.minute))
        self.ui.departure_date.setDate(QDate(slight_future.year, slight_future.month, slight_future.day))

        self.ui.route.setPlainText('')

        self.ui.departure_runway.setText('')
        self.ui.sid.setText('')
        self.ui.cruise_altitude.setText('')
        self.ui.cruise_speed.setText('')
        self.ui.star.setText('')
        self.ui.destination_runway.setText('')

        self.ui.aircraft.setText('')
        self.ui.airline.setText('')
        self.ui.flight_code.setText('')

        self.ui.distance.setText('')
        self.ui.block_time.setTime(QTime(0, 0))

        self.ui.equipment.setText('')
        self.ui.equipment_suffix.setText('')

        self.ui.pax.setText('')
        self.ui.cargo.setText('')
        self.ui.zfw.setText('')

        self.ui.remarks.setPlainText('')
        self.ui.fuel_endurance.setTime(QTime(0, 0))
        self.ui.block_fuel.setText('')

        self.ui.tow.setText('')

        pilot_name = self.gui_root.fslapp.settings.get('pilot', 'name')
        pilot_base = self.gui_root.fslapp.settings.get('pilot', 'base')
        if pilot_name:
            self.ui.pilot_name.setText(pilot_name)
        else:
            self.ui.pilot_name.setText('')

        if pilot_base:
            self.ui.pilot_base.setText(pilot_base)
        else:
            self.ui.pilot_base.setText('')

        self.set_populated_plan(None)

    def update_populated_plan(self):
        self.update_plan(self.populated_plan)

    def update_plan(self, plan):
        if not plan:  # No plan populated yet. Or deleted.
            return

        fields = self.read_form_data()
        plan.update(fields)
        logger.debug(plan)

    def read_form_data(self):
        dep_time = self.ui.departure_time.time().toString('HH:mm')
        dep_date = self.ui.departure_date.date().toString('yyyy-MM-dd')
        block_time = self.ui.block_time.time().toString('HH:mm')
        fields = {
            'callsign': self.ui.callsign.text(),

            'departure': self.ui.departure.text(),
            'destination': self.ui.destination.text(),
            'alternate': self.ui.alternate.text(),

            'departure_time': dep_time,
            'departure_date': dep_date,

            'route': self.ui.route.toPlainText(),

            'departure_runway': self.ui.departure_runway.text(),
            'sid': {
                'name': self.ui.sid.text()
            },
            'cruise_altitude': self.ui.cruise_altitude.text(),
            'cruise_speed': self.ui.cruise_speed.text(),
            'star': {
                'name': self.ui.star.text()
            },
            'destination_runway': self.ui.destination_runway.text(),

            'aircraft': self.ui.aircraft.text(),
            'airline': self.ui.airline.text(),
            'flight_code': self.ui.flight_code.text(),

            'distance': self.ui.distance.text(),
            'block_time': block_time,

            'block_fuel': self.ui.block_fuel.text(),
            'equipment': self.ui.equipment.text(),
            'equipment_suffix': self.ui.equipment_suffix.text(),
            'pax': self.ui.pax.text(),
            'cargo': self.ui.cargo.text(),
            'zfw': self.ui.zfw.text(),
            'tow': self.ui.tow.text(),
            'remarks': self.ui.remarks.toPlainText()
        }

        filtered_fields = {}
        for key, field in fields.items():
            if field != '':
                filtered_fields[key] = field

        logger.debug(filtered_fields)
        return filtered_fields

    def revert_changes(self):
        if self.populated_plan:
            self.populate_plan(self.populated_plan)
        else:
            self.empty()

    def activate(self):
        form = self.read_form_data()
        try:
            new_plan = Plan(form, self.gui_root.fslapp.server)
            self.run_async(self.gui_root.fslapp.server.set_active_plan, new_plan)
            self.reset_style_sheets()
            self.populate_plan(new_plan)
        except server.exceptions.MissingField as exc:
            if exc.missing_key:
                self.reset_style_sheets()
                ui_elem_for_missing_key = getattr(self.ui, exc.missing_key)
                ui_elem_for_missing_key.setStyleSheet('border: 2px solid red;')
                self.style_sheet_modified.append(ui_elem_for_missing_key)
            logger.warning('No plan initiated.')
            return

    def reset_style_sheets(self):
        for ui_elem in self.style_sheet_modified:
            ui_elem.setStyleSheet('')
            self.style_sheet_modified.remove(ui_elem)

    def print_exporters(self):
        layout = self.ui.exporters_contents.layout()
        self.clear_layout(layout)

        for index, exporter in enumerate(self.gui_root.fslapp.server.exporters):
            exporter_ui_module = ExporterContainer(self.gui_root, exporter)
            layout.addWidget(exporter_ui_module)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def add_export_module(self):
        self.add_module_dialog = AddExporter(self.gui_root)
        print(self.add_module_dialog)
