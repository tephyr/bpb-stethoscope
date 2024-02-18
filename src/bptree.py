from pathlib import Path

from draftsman import utils

from filter_blueprints import BlueprintFilter

VALUE_KEYS_STD = ('blueprint_book', 'blueprint', 'label', 'active_index')
OBJECT_KEYS = ('blueprint_book', 'blueprint') # Should only ever be keys from constants.KNOWN_CONTAINERS.

class BPTree:
    """
    Load, parse and make available a simplified and filtered tree of data from any blueprint/blueprintbook file.
    """

    def __init__(self, path_to_blueprint:str=None, blueprint_string:str=None):
        self._path_to_blueprint = path_to_blueprint
        self._blueprint_string = blueprint_string
        self._error_msg = None
        self.blueprint_data = {}
        if path_to_blueprint is None:
            if blueprint_string is None:
                raise RuntimeError("Either path or blueprint string must be provided.")
        self.load_blueprint()
        self._bp_filter = None # BlueprintFilter()
        self._value_keys_to_use = set(VALUE_KEYS_STD)

    def load_blueprint(self):
        self._error_msg = None
        if self._path_to_blueprint:
            p = Path(self._path_to_blueprint).expanduser()
            if p.exists():
                self._blueprint_string = p.read_text()
                self.blueprint_data = utils.string_to_JSON(self._blueprint_string)
            else:
                self._error_msg = f'Failed to find this file: {self._path_to_blueprint}.'
        else:
            self.blueprint_data = utils.string_to_JSON(self._blueprint_string)

    def adjust_keys_to_return(self, keep:list[str]=None, drop:list[str]=None)->None:
        """
        Add and/or remove keys to apply to the filter.

        NOTE: this is a whitelist: only the keys in this list are returned.  See ``VALUE_KEYS_STD`` for a standard **whitelist** of keys.
        """
        if type(keep) not in [list, tuple] and type(drop) not in [list, tuple]:
            raise RuntimeError("Either keep or drop must be given; both must be lists.")
        print(f'adjust_keys_to_return {keep=} {drop=}')
        if drop is not None:
            self._value_keys_to_use.difference_update(drop)
        if keep is not None:
            self._value_keys_to_use.update(keep)

    def _prep_filter(self):
        # print(f'Current self._bp_filter: {self._bp_filter}')
        self._bp_filter = BlueprintFilter(self.blueprint_data, OBJECT_KEYS, self._value_keys_to_use)
        # print(f'New self._bp_filter: {self._bp_filter}; created with values_inclusive=={self._value_keys_to_use}')

    def get_current_filter_keys(self):
        return self._value_keys_to_use

    def get_error_msg(self):
        return self._error_msg

    def get_filtered_data(self)->dict:
        """
        Return a dict filtered by settings.

        TODO: add customizable settings.
        """
        self._prep_filter()
        return self._bp_filter.filter()

    def get_root_key(self)->str:
        """
        Returns the key at the root of the *filtered* data.
        """
        self._prep_filter()
        root_keys = self._bp_filter.filter().keys()
        if len(root_keys) == 1:
            return list(root_keys)[0]
        else:
            self._error_msg = f"More than one root key: {root_keys}"
