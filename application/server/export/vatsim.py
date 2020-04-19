import urllib.parse
import webbrowser
import server.exceptions
import server.utility


class Vatsim:
    def __init__(self, parent, options):
        self.parent = parent
        self.options = options
        self.mapping = {
            '2': 'callsign',
            '3': {
                'merge': [
                    'aircraft',
                    'equipment_suffix'
                ],
                'join': '/'
            },
            '4': 'cruise_speed',
            '5': 'departure',
            '6': {
                'merge': [
                    {
                        'function': 'get_nested_dict',
                        'args': ['departure_time', 'hours']
                    },
                    {
                        'function': 'get_nested_dict',
                        'args': ['departure_time', 'minutes']
                    }
                ],
                'join': ''
            },
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
            '13': 'alternate',
            '14': {
                'function': 'get_pilot',
                'kwargs': {
                    'add_base': ' '
                }
            }
        }

    async def export(self, plan):
        mapped = server.utility.populate_with_map(plan, self.mapping, {}, ['departure', 'destination'], '')

        encoded = urllib.parse.urlencode(mapped)
        url = 'https://cert.vatsim.net/fp/file.php'
        webbrowser.open_new_tab(f"{url}?{encoded}")


ID = 'vatsim'
NAME = 'Vatsim'
CLASS = Vatsim
