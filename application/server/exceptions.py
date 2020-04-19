
class HandledException(Exception):
    def __init__(self, exc, message, *args, **kwargs):
        self.message = message


class MissingField(HandledException):
    def __init__(self, missing_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.missing_key = missing_key

class FieldNotInModel(HandledException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
