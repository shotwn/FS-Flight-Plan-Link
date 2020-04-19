import os.path
import xml.etree.ElementTree as ET
import server.exceptions
import server.utility


class VPilot:
    def __init__(self, parent, options):
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
        pass

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
            xml.set('EnrouteHours', plan.get_nested_dict('air_time', 'hours', convert='str'))
            xml.set('EnrouteMinutes', plan.get_nested_dict('air_time', 'minutes', convert='str'))

        if 'block_time' in plan:
            xml.set('FuelHours', plan['block_time']['hours'])
            xml.set('FuelMinutes', plan['block_time']['minutes'])

        # print(ET.tostring(xml))
        directory = os.path.join(self.options['export_dir'])
        src = os.path.join(directory, f"{plan['departure']}{plan['destination']}.vfp")

        with open(src, 'wb+') as plan_xml:
            plan_xml.write(ET.tostring(xml))


def default_options(options):
    module_defaults = {
        'export_dir': '.\\'
    }
    module_defaults.update(options)
    return module_defaults


ID = 'vpilot'
NAME = 'vPilot'
CLASS = VPilot
