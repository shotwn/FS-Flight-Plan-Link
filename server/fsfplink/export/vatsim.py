import urllib.parse
import webbrowser
import fsfplink.exceptions
import fsfplink.utility


class Vatsim:
    def __init__(self, parent, options):
        self.parent = parent
        self.options = options
        self.mapping = {
            '2': 'callsign',
            '4': 'cruise_speed',
            '5': 'departure',
            '7': 'cruise_altitude',
            '8': {
                'function': 'route_to_str'
            },
            '9': 'destination',
            '10a': {
                'function': 'get_nested_dict',
                'args': ['air_time', 'hours'],
            },
            '10b': {
                'function': 'get_nested_dict',
                'args': ['air_time', 'minutes'],
            },
            '11': 'remarks',
            '12a': {
                'function': 'get_nested_dict',
                'args': ['block_time', 'hours'],
            },
            '12b': {
                'function': 'get_nested_dict',
                'args': ['block_time', 'minutes'],
            },
            '13': 'alternate'
        }

    async def export(self, plan):
        mapped = fsfplink.utility.populate_with_map(plan, self.mapping, {}, ['departure', 'destination'])
        if 'aircraft' in plan and 'equipment_suffix' in plan:
            mapped['3'] = f"{plan['aircraft']}{plan['equipment_suffix']}"

        if 'departure_time' in plan:
            mapped['6'] = f"{plan['departure_time']['hours']}{plan['departure_time']['minutes']}"

        if 'pilot' in plan:
            mapped['14'] = f"{self.settings.get('pilot', 'name')} {self.settings.get('pilot', 'base')}"

        encoded = urllib.parse.urlencode(mapped)
        url = 'https://cert.vatsim.net/fp/file.php'
        webbrowser.open_new_tab(f"{url}?{encoded}")


ID = 'vatsim'
NAME = 'Vatsim'
CLASS = Vatsim
