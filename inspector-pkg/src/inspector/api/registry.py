from inspector.api.platformcompatibility import Platform, CURRENT_PLATFORM


class Registry:

    def __init__(self):
        self._collectors = {}
        self._validators = {}
        self._reactors = {}

    def register_collector(self, component_id, collector):
        Registry._register_platform_compatible(self._collectors, component_id, collector)

    def register_validator(self, component_id, validator):
        Registry._register_platform_compatible(self._validators, component_id, validator)

    def register_reactor(self, component_id, *reactors):
        existing_reactors = self._reactors.get(component_id, [])
        self._reactors[component_id] = \
            existing_reactors + \
            list(r for r in reactors if Registry._is_platform_compatible(r))

    def component_ids(self):
        return self._collectors.keys()

    def find_collector(self, component_id):
        return self._collectors.get(component_id, None)

    def find_validator(self, component_id):
        return self._validators.get(component_id, None)

    def find_reactors(self, component_id):
        return self._reactors.get(component_id, [])

    @staticmethod
    def _is_platform_compatible(obj):
        target_platform = getattr(obj, "target_platform", Platform.UNDEFINED)
        return target_platform == Platform.UNDEFINED or target_platform == CURRENT_PLATFORM

    @staticmethod
    def _register_platform_compatible(collection, component_id, obj):
        if Registry._is_platform_compatible(obj):
            collection[component_id] = obj
