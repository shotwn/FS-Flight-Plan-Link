import os.path
from pathlib import Path
import xml.etree.ElementTree as ET
import server.exceptions
import server.utility
from server.export._exporter import Exporter


class VPilot(Exporter):
    id = 'vpilot'
    name = 'vPilot'
    method = 'File'

    def __init__(self, parent, options):
        super().__init__(parent, options)
        self.parent = parent
        self.options = options
        self.mapping = {
            'FlightType': 'type',
            'Equipment': 'equipment',
            'CruiseAltitude': 'cruise_altitude',
            'CruiseSpeed': 'cruise_speed',
            'DepartureAirport': 'departure',
            'DestinationAirport': 'destination',
            'AlternateAirport': 'alternate',
            'Remarks': 'remarks',
            'EquipmentSuffix': 'equipment_suffix'
        }
        self.defaults = {
            'FlightType': 'IFR'
        }

    async def export(self, plan):
        mapped = server.utility.populate_with_map(plan, self.mapping, self.defaults)

        xml = ET.Element('FlightPlan')
        for key, value in mapped.items():
            try:
                xml.set(key, str(value))
            except (TypeError, KeyError) as exc:
                raise server.exceptions.MissingField(exc, f'Missing Field: {key}')

        # print(plan.plan)
        xml.set('Route', str(plan['route']))

        if 'departure_time' in plan:
            xml.set('DepartureTime', f"{plan['departure_time']['hours']}{plan['departure_time']['minutes']}")

        if 'air_time' in plan:
            xml.set('EnrouteHours', plan.get_nested_dict('block_time', 'hours', convert='str'))
            xml.set('EnrouteMinutes', plan.get_nested_dict('block_time', 'minutes', convert='str'))

        if 'block_time' in plan:
            xml.set('FuelHours', plan.get_nested_dict('fuel_endurance', 'hours', convert='str'))
            xml.set('FuelMinutes', plan.get_nested_dict('fuel_endurance', 'minutes', convert='str'))

        # print(ET.tostring(xml))
        directory = os.path.join(self.options['export_dir'].get('dir', self.options['export_dir'].get('default', '')))
        Path(directory).mkdir(parents=True, exist_ok=True)

        src = os.path.join(directory, f"{plan['departure']}{plan['destination']}.vfp")

        with open(src, 'wb+') as plan_xml:
            plan_xml.write(ET.tostring(xml))

    @staticmethod
    def default_options(options={}):
        my_documents = server.utility.get_my_documents_dir()
        module_defaults = {
            'export_dir': {
                'type': 'folder',
                'default': os.path.join(my_documents, 'vPilot Files', 'FSLink'),
                'label': 'Export Path'
            }
        }
        options.update(module_defaults)
        return options


CLASS = VPilot
