class Exporter:
    description = ''

    def __init__(self, parent, options):
        self.parent = parent
        self.options = options
        self.auto = False
        self.nickname = options.get('nickname', '')

    def update_options(self, options):
        self.options = options
        self.parent.events.run_observers_for('exporter_options_updated', self)

    @classmethod
    def initial_options(cls, options):
        module_defaults = {
            'nickname': {
                'type': 'str',
                'default': '',
                'label': 'Name'
            }
        }
        module_defaults.update(options)
        return cls.default_options(module_defaults)

    @staticmethod
    def default_options(options):
        return options
