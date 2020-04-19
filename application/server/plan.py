import json
import re
import builtins
from datetime import datetime
from loguru import logger
import server.exceptions
from server.json import json_encoder

TIME_FORMAT_REG = r"^(\d*):(\d*)$"
DATE_FORMAT_REG = r"^(\d{4})-(\d{2})-(\d{2})$"


def time_format(time_str, **kwargs):
    matches = re.search(TIME_FORMAT_REG, time_str)
    if not matches:
        raise ValueError

    groups = matches.groups()
    return {
        'hours': int(groups[0]),
        'minutes': int(groups[1])
    }


def date_format(date_str, **kwargs):
    matches = re.search(DATE_FORMAT_REG, date_str)
    if not matches:
        raise ValueError

    groups = matches.groups()
    return {
        'year': int(groups[0]),
        'month': int(groups[1]),
        'day': int(groups[2])
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
    sid_star_construct = {
        'name': sid_star['name']
    }
    if 'route' in sid_star:
        sid_star_construct['route'] = route_format(sid_star['route'], **kwargs)

    return sid_star_construct


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
    'flight_code': 'str',
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
    'distance': 'int',
    'fuel_endurance': {
        'format': time_format
    },
    'pax': 'int',
    'cargo': 'int'
}

WAYPOINT_MODEL = {
    'name': 'str',
    'latitude': 'float',
    'longitude': 'float',
    'altitude': 'int',
    'speed': 'int'
}


def model_parser(data, model, **kwargs):
    """Parse input data according to a model.

    Args:
        data (Dict): Input data
        model (Dict): Input model

    Raises:
        server.exceptions.MissingField: Raises when required field is missing or badly formatted.

    Returns:
        List: [parsed_data, parse_errors]
    """
    formatted = {}
    errors = []

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
                    'message': f'Input {value} in wrong format or value for {key}. Passing.'
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
                        'message': f'Input {value} in wrong format or value for {key}. Passing.'
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

    # CHECK FOR REQUIRED FIELDS
    for key, value in model.items():
        if isinstance(value, dict) and 'required' in value and value['required']:
            if key not in formatted:
                error_msg = f'Missing required field {key}'
                logger.error(error_msg)
                raise server.exceptions.MissingField(key, None, error_msg)

    if errors:
        logger.warning(errors)

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
        self.server = server
        parsed = model_parser(plan, MODEL, server=server)
        self.plan = parsed[0]
        self.errors = parsed[1]
        if self.errors:
            print(f'Parser errors: {self.errors}')

        if 'created_datetime' not in self.plan:
            self.plan['created_datetime'] = datetime.utcnow()

    def update(self, plan_data):
        logger.debug('Plan Update Called:')
        logger.debug(plan_data)

        parsed = model_parser(plan_data, MODEL, server=server)
        parsed_data = parsed[0]
        self.errors = parsed[1]
        if self.errors:
            logger.warning(self.errors)

        self.plan.update(parsed_data)
        self.plan['updated_datetime'] = datetime.utcnow()

        return parsed[1]

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

    def route_to_str(self, include_sid_star=True, open_sid_star=False):
        points = []
        sid_star_field = 'route' if open_sid_star else 'name'
        if 'sid' in self.plan and include_sid_star:
            points.append(str(self.get_nested_dict('sid', sid_star_field)))

        points.append(str(self.plan['route']))

        if 'star' in self.plan and include_sid_star:
            points.append(str(self.get_nested_dict('star', sid_star_field)))

        return ' '.join(points)

    def get_pilot(self, add_base=False):
        pilot = self.server.settings.get('pilot', 'name')
        if add_base is not False:
            pilot += add_base + self.server.settings.get('pilot', 'base')

        return pilot

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
                    raise server.exceptions.MissingField(key, exc, key)
                else:
                    return None
            else:
                raise server.exceptions.FieldNotInModel(exc, key)

    def __contains__(self, key):
        return key in self.plan
