import json
import re
import builtins
from loguru import logger
import fsfplink.exceptions
from fsfplink.json import json_encoder

TIME_FORMAT_REG = r"^(\d*):(\d*)$"
DATE_FORMAT_REG = r"^(\d{4})-(\d{2})-(\d{2})$"


def time_format(time_str, **kwargs):
    matches = re.search(TIME_FORMAT_REG, time_str)
    if not matches:
        raise ValueError

    groups = matches.groups()
    return {
        'hours': groups[0],
        'minutes': groups[1]
    }


def date_format(date_str, **kwargs):
    matches = re.search(DATE_FORMAT_REG, date_str)
    if not matches:
        raise ValueError

    groups = matches.groups()
    return {
        'year': groups[0],
        'month': groups[1],
        'day': groups[2]
    }


"""
def route_format(route):
    if isinstance(route, list):
        wp_list = []
        for item in route:
            wp_list.append(Waypoint(item))
        return wp_list
    elif isinstance(route, str):
        return route

    raise TypeError
"""


def route_format(route, **kwargs):
    return Route(route, kwargs['server'])


def sid_star_format(sid_star, **kwargs):
    return {
        'name': sid_star['name'],
        'route': route_format(sid_star['route'], **kwargs)
    }


MODEL = {
    'air_time': {
        'format': time_format
    },
    'airac': 'int',
    'aircraft': 'str',
    'airline': 'str',
    'alternative': 'str',
    'block_fuel': 'int',
    'block_time': {
        'format': time_format
    },
    'callsign': {
        'type': 'str',
        'required': True
    },
    'cruise_altitude': 'int',
    'departure': {
        'type': 'str',
        'required': True
    },
    'departure_date': {
        'format': date_format
    },
    'departure_time': {
        'format': time_format
    },
    'departure_runway': {
        'type': 'str',
        'max': 3
    },
    'destination': {
        'type': 'str',
        'required': True,
        'min': 4,
        'max': 4
    },
    'destination_runway': {
        'type': 'str',
        'max': 3
    },
    'flight_no': 'str',
    'route': {
        'format': route_format,
        'required': True
    },
    'sid': {
        'format': sid_star_format
    },
    'star': {
        'format': sid_star_format
    },
    'cruise_speed': 'int',
    'tow': 'int',
    'units': 'str',
    'zfw': 'int',
    'remarks': 'str',
    'equipment': 'str',
    'type': 'str',
    'alternate': 'str',
    'equipment_suffix': 'str',
    'distance': 'int'
}

WAYPOINT_MODEL = {
    'name': 'str',
    'latitude': 'float',
    'longitude': 'float',
    'altitude': 'int',
    'speed': 'int'
}


def model_parser(data, model, **kwargs):
    formatted = {}
    errors = []
    # CHECK FOR REQUIRED FIELDS
    for key, value in model.items():
        if isinstance(value, dict) and 'required' in value and value['required']:
            if key not in data:
                error_msg = f'Missing required field {key}'
                logger.error(error_msg)
                raise fsfplink.exceptions.MissingField(error_msg)

    # FORMAT DATA PER MODEL
    for key, value in data.items():
        # CHECK IF SPEC EXISTS
        try:
            spec = model[key]
        except KeyError:
            errors.append({
                'key': key,
                'message': f'Spec not found {key}. Passing.'
            })
            continue

        # Only type.
        if isinstance(spec, str):
            try:
                formatted_value = getattr(builtins, spec)(value)
            except ValueError:
                errors.append({
                    'key': key,
                    'message': f'Input in wrong format or value for {key}. Passing.'
                })
                continue
        else:
            # Has an external formatter
            if 'format' in spec:
                try:
                    formatted_value = spec['format'](value, **kwargs)
                except ValueError:
                    errors.append({
                        'key': key,
                        'message': f'Input in wrong format or value for {key}. Passing.'
                    })
                    continue
            # Internal type and other attributes.
            else:
                try:
                    # type
                    formatted_value = getattr(builtins, spec['type'])(value)
                    if 'max' in spec and spec['max'] < len(value):
                        errors.append({
                            'key': key,
                            'message': f'Out of max value {key}. Passing.'
                        })
                        continue
                    if 'min' in spec and spec['min'] > len(value):
                        errors.append({
                            'key': key,
                            'message': f'Out of min value {key}. Passing.'
                        })
                        continue
                except KeyError:
                    errors.append({
                        'key': key,
                        'message': f'Spec does have type for {key}. Passing.'
                    })
                    continue
        formatted[key] = formatted_value

    if errors:
        logger.error(errors)

    return [formatted, errors]


class Waypoint:
    def __init__(self, waypoint, server):
        parsed = model_parser(waypoint, WAYPOINT_MODEL, server=server)
        self.waypoint = parsed[0]
        self.errors = parsed[1]

    def __str__(self):
        return self.waypoint['name']

    def toJSON(self):
        return self.waypoint


class Route:
    def __init__(self, route, server):
        self.waypoints = []
        if isinstance(route, list):
            for item in route:
                self.waypoints.append(Waypoint(item, server))
        else:
            self.route = route

    def __str__(self):
        if self.waypoints:
            return ' '.join(str(x) for x in self.waypoints)
        # No waypoints
        return self.route

    def toJSON(self):
        if self.waypoints:
            return self.waypoints

        return self.route


class Plan:
    def __init__(self, plan, server):
        parsed = model_parser(plan, MODEL, server=server)
        self.plan = parsed[0]
        self.errors = parsed[1]
        if self.errors:
            print(f'Parser errors: {self.errors}')

    def json(self):
        return json.dumps({
            'plan': self.plan,
            'errors': self.errors
        }, default=json_encoder)

    def toJSON(self):
        return {
            'parsed': self.plan,
            'parser_errors': self.errors
        }

    def get(self, key, default=None):
        return self.plan.get(key, default)

    def route_to_str(self, open_sid_star=False):
        points = []
        sid_star_field = 'name' if open_sid_star else 'route'
        if 'sid' in self.plan:
            points.append(str(self.plan['sid'][sid_star_field]))

        points.append(str(self.plan['route']))

        if 'star' in self.plan:
            points.append(str(self.plan['star'][sid_star_field]))

        return ' '.join(points)

    def get_nested_dict(self, *keys, default=None, convert=None):
        keys = list(keys)
        last_key = keys.pop()

        top = self.get(keys.pop(0), {})
        for key in keys:
            top = top.get(key, {})

        value = top.get(last_key, default)
        if not convert:
            return value
        else:
            return self.convert_to_internal(value, convert)

    def convert_to_internal(self, value, internal_type_str):
        return getattr(builtins, internal_type_str)(value)

    def __getitem__(self, key):
        try:
            return self.plan[key]
        except KeyError as exc:
            keys_model = MODEL.get(key)
            if keys_model:
                if keys_model['required']:
                    raise fsfplink.exceptions.MissingField(exc, key)
                else:
                    return None
            else:
                raise fsfplink.exceptions.FieldNotInModel(exc, key)

    def __contains__(self, key):
        return key in self.plan
