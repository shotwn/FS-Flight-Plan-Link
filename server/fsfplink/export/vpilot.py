import os.path
import xml.etree.ElementTree as ET
import fsfplink.exceptions
import fsfplink.utility

NAME = 'vPilot'
CLASSNAME = 'VPilot'


class VPilot:
    def __init__(self, server):
        self.settings = server.settings
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
        mapped = fsfplink.utility.populate_with_map(plan, self.mapping, self.defaults)

        xml = ET.Element('FlightPlan')
        for key, value in mapped.items():
            try:
                xml.set(key, str(value))
            except (TypeError, KeyError) as exc:
                raise fsfplink.exceptions.MissingField(exc, f'Missing Field: {key}')

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
        directory = os.path.join(self.settings.get('vPilot', 'export_dir'))
        src = os.path.join(directory, f"{plan['departure']}{plan['destination']}.vfp")

        with open(src, 'wb+') as plan_xml:
            plan_xml.write(ET.tostring(xml))
