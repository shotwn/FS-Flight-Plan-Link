from loguru import logger
import server.exceptions


def populate_with_map(source, mapping, defaults, required=[], replace_none=None):
    mapped = {}
    for key, value in mapping.items():
        """
        Call a function in target
            {
                'function': 'name',
                'args': [],
                'kwargs': {}
            }
        Nest and merge, str.join the result
            {
                'merge': [
                    {
                        'function': 'name',
                        'args': [],
                        'kwargs': {}
                    },
                    'pilot_name'
                ],
                'join': ':'
            }
        Static
            {
                'static': 'I am a static value'
            }
        """
        if isinstance(value, dict):
            if 'static' in value:
                mapped[key] = value['static']
            elif 'function' in value:
                func = getattr(source, value['function'], None)
                args = value.get('args', [])
                kwargs = value.get('kwargs', {})
                mapped[key] = func(*args, **kwargs)
            elif 'merge' in value:
                collected = populate_with_map(source, dict(zip(range(len(value['merge'])), value['merge'])), defaults, required, replace_none)  # Send as dict.
                collected = filter(None, collected.values())  # Back to list. None values are gone.
                collected = [f'{x}' for x in collected]  # All to string before join
                mapped[key] = value['join'].join(collected)
            else:
                logger.warn('Passing on a dict in the map.')
                logger.warn(value)
        else:
            try:
                mapped[key] = source[value]
            except (TypeError, KeyError) as exc:
                if key in defaults:
                    mapped[key] = defaults[key]
                else:
                    if key in required:
                        raise server.exceptions.MissingField(exc, f'Missing Field: {key}')
                    else:
                        mapped[key] = None

        if mapped[key] is None:
            mapped[key] = replace_none

    return mapped


def convert_lat(ddmmssH):
    deg = int(ddmmssH[0:2])
    mins = int(ddmmssH[2:4])
    secs = int(ddmmssH[4:6])
    hem = ddmmssH[6:7]
    hem_sign = 1 if hem == 'N' else -1
    all_deg = deg + mins / 60 + secs / 3600 * hem_sign
    return format(all_deg, '.10f')


def convert_lon(dddmmssH):
    deg = int(dddmmssH[0:3])
    mins = int(dddmmssH[3:5])
    secs = int(dddmmssH[5:7])
    hem = dddmmssH[7:8]
    hem_sign = 1 if hem == 'E' else -1
    all_deg = deg + mins / 60 + secs / 3600 * hem_sign
    return format(all_deg, '.10f')
