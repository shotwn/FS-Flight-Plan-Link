from datetime import datetime


def json_encoder(class_instance):
    if hasattr(class_instance, 'toJSON'):
        return class_instance.toJSON()
    elif isinstance(class_instance, datetime):
        return class_instance.isoformat()
    else:
        return class_instance.__dict__
