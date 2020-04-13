def json_encoder(class_instance):
    if hasattr(class_instance, 'toJSON'):
        return class_instance.toJSON()
    else:
        class_instance.__dict__
