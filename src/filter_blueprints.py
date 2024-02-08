"""
Filter raw blueprint dicts.

Basic structure::

    {
        'blueprint_book': {
            'blueprints': [{
                'blueprint': {
                    'icons': [],
                    'entities': [],
                    'item': 'blueprint',
                    'label': 'Generic station, base',
                    'version': 281479276527617
                },
                'index': 0
            }, {
                'blueprint': {
                    'icons': [{
                    }],
                    'entities': [{
                    }],
                    'item': 'blueprint',
                    'label': 'Generic station, base, v2',
                    'version': 281479276527617
                },
                'index': 1
            }, {
"""
KNOWN_CONTAINERS = ('blueprint_book', 'blueprint', 'upgrade_planner', 'deconstruction_planner')
SET_KC = set(KNOWN_CONTAINERS)

class BlueprintFilter():
    def __init__(self, initial_blueprint:dict, objects_inclusive: tuple[str]=None, values_inclusive:tuple[str]=None):
        self.initial_data = initial_blueprint or {}
        self.objects_inclusive = objects_inclusive or ('blueprint_book', 'blueprint')
        self.values_inclusive = {'item'} # A set.  This value is always required.
        if values_inclusive is not None:
            self.values_inclusive.update(values_inclusive)

    # @snoop(depth=1)
    def filter(self)->dict:
        """
        Filter the current blueprint, keeping only the keys from keys_inclusive.  Keep the same hierarchy.
        """
        result = {}

        top_level_key = self._get_container_key(self.initial_data)

        if top_level_key in self.objects_inclusive:
            result[top_level_key] = self._filter_by_object_type(top_level_key, self.initial_data[top_level_key])

        return result

    def _filter_by_object_type(self, object_key:str, value:any)->any:
        """
        Given any kind of object, pass off to the correct parser.
        """
        result = None
        if object_key == 'blueprint_book':
            result = self._filter_bpb(value)
        elif object_key == 'blueprint':
            result = self._filter_bp(value)

        return result

    def _filter_by_container(self, container:dict)->any:
        result = None
        # Check the keys to determin the container type.
        if 'blueprint_book' in container:
            result = self._filter_bpb(container)
        elif 'blueprint' in container:
            result = self._filter_bp(container)

        return result


    def _filter_bpb(self, bpb:dict)->dict:
        result = {}
        if 'blueprints' in bpb:
            result['blueprints'] = []
        for container in bpb['blueprints']:
            # This is the *container* for the blueprint (or upgrade/deconstruction planner).
            # It will have an index which may signal how many blank spots are between it and the previous container.
            filtered_obj = self._filter_by_container(container)
            if filtered_obj is not None:
                result['blueprints'].append(filtered_obj)

        for val in self.values_inclusive:
            if val in bpb:
                result[val] = bpb[val]

        return result

    # @snoop(depth=1, watch=('result'))
    def _filter_bp(self, bp:dict)->dict:
        result = {}
        for k in self.values_inclusive:
            if k in bp:
                result[k] = bp.get(k)
        return result

    def _get_container_key(self, data:dict)->str:
        """
        Get an object type by finding any of the known containers in the keys.

        Fail out if not found - that signifies a change in format/error in data.
        """
        # set_keys = set(data.keys())
        common_keys = SET_KC.intersection(data.keys())
        assert len(common_keys) == 1

        return common_keys.pop()
