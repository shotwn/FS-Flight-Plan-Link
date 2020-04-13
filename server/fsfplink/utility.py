import fsfplink.exceptions


def populate_with_map(source, mapping, defaults, required=[]):
    mapped = {}
    for key, value in mapping.items():
        """
        Call a function in target {'function': 'name', 'args': [], 'kwargs': {}}
        """
        if isinstance(value, dict):
            func = getattr(source, value['function'])
            args = value.get('args', [])
            kwargs = value.get('kwargs', {})
            mapped[key] = func(*args, **kwargs)
        else:
            try:
                mapped[key] = source[value]
            except (TypeError, KeyError) as exc:
                if key in defaults:
                    mapped[key] = defaults[key]
                else:
                    if key in required:
                        raise fsfplink.exceptions.MissingField(exc, f'Missing Field: {key}')
                    else:
                        mapped[key] = None

    return mapped
