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
from copy import deepcopy

from constants import KNOWN_CONTAINERS

SET_KC = set(KNOWN_CONTAINERS)

class BlueprintFilter():
    """
    Filter Factorio blueprints.

    By default, only ``blueprint`` and ``blueprint_book`` containers will be retained, with their ``item`` keys.
    """
    def __init__(self, initial_blueprint:dict, objects_inclusive: tuple[str]=None, values_inclusive:tuple[str]=None):
        """
        Prep a blueprint filter.

        :param dict initial_blueprint: Blueprint dict to filter.
        :param tuple[str] objects_inclusive: Optional object names to retain.  Defaults to 'blueprint_book', 'blueprint'.
        :param tuple[str] values_inclusive: Keys *within objects* to retain.  Defaults to ``item``, which is always required.
        """
        self.initial_data = deepcopy(initial_blueprint or {})
        self.objects_inclusive = objects_inclusive or ('blueprint_book', 'blueprint')
        self.values_inclusive = {'item'} # A set.  ``item`` is always required.
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

    def _filter_bpb(self, bpb:dict)->dict:
        result = {}
        if 'blueprints' in bpb and type(bpb['blueprints']) is list:
            result['blueprints'] = []

            # Go depth-first.
            for container in bpb['blueprints']:
                # This is the *container* for the blueprint (or upgrade/deconstruction planner).
                # It has an index value which signals the order of appearance, and how many blank spots are between it and the previous container.
                container_key = self._get_container_key(container)
                filtered_obj = self._filter_by_object_type(container_key, container[container_key])
                if filtered_obj is not None:
                    result['blueprints'].append({container_key: filtered_obj})
                    # Check for additional keys to copy over at this level (other container keys).
                    for val in self.values_inclusive:
                        if val in container and val not in filtered_obj:
                            result['blueprints'][-1][val] = container[val]

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
        assert len(common_keys) == 1, f"Not enough or too many keys (should be only 1: {common_keys=}, {data.keys()=})"

        return common_keys.pop()
