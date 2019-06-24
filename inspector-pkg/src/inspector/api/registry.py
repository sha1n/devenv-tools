class Registry:

    def __init__(self):
        self._collectors = {}
        self._validators = {}
        self._reactors = {}

    def register_collector(self, component_id, collector):
        self._collectors[component_id] = collector

    def register_validator(self, component_id, validator):
        self._validators[component_id] = validator

    def register_reactor(self, component_id, *reactors):
        existing_reactors = self._reactors.get(component_id, [])
        self._reactors[component_id] = existing_reactors + list(reactors)

    def component_ids(self):
        return self._collectors.keys()

    def find_collector(self, component_id):
        return self._collectors.get(component_id, None)

    def find_validator(self, component_id):
        return self._validators.get(component_id, None)

    def find_reactors(self, component_id):
        return self._reactors.get(component_id, [])
