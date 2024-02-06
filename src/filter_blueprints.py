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

class BlueprintFilter():
    def __init__(self, initial_blueprint:dict, objects_inclusive: tuple[str], values_inclusive:tuple[str]):
        self.initial_data = initial_blueprint or {}
        self.objects_inclusive = objects_inclusive or ('blueprint_book', 'blueprint')
        self.values_inclusive = {'item'} # A set.  This value is always required.
        if values_inclusive is not None:
            self.values_inclusive.update(values_inclusive)

    # @snoop(depth=1)
    def filter(self)->dict:
        """
        Filter the current blueprint, keeping only the keys from keys_inclusive.
        """
        result = {}
        for object_key, value in self.initial_data.items():
            if object_key in self.objects_inclusive:
                result[object_key] = self._filter_by_object_type(object_key, value)
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
        if 'blueprints' in bpb:
            result['blueprints'] = []
        for bp in bpb['blueprints']:
            for key_x, val_x in bp.items():
                filtered_obj = self._filter_by_object_type(key_x, val_x)
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

