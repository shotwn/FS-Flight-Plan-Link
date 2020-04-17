from loguru import logger
import fslink.exceptions


def populate_with_map(source, mapping, defaults, required=[]):
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
                collected = populate_with_map(source, dict(zip(range(len(value['merge'])), value['merge'])), defaults, required)  # Send as dict.
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
                        raise fslink.exceptions.MissingField(exc, f'Missing Field: {key}')
                    else:
                        mapped[key] = None

    return mapped
