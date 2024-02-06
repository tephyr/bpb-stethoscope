from pathlib import Path

from draftsman import utils

from filter_blueprints import BlueprintFilter

IGNORE_KEYS = ('icons', 'entities', 'version', 'index', 'active_index', 'item', 'snap-to-grid', 'tiles', 'schedules')
VALUE_KEYS = ('blueprint', 'blueprint_book', 'label', 'active_index')
OBJECT_KEYS = ('blueprint_book', 'blueprint')

class BPTree:
    """
    Load, parse and make available a simplified and filtered tree of data from any blueprint/blueprintbook file.
    """

    def __init__(self, path_to_blueprint:str):
        self._path_to_blueprint = path_to_blueprint
        self._error_msg = None
        self._blueprint_text = None
        self.blueprint_data = {}
        self.load_blueprint()
        self._bp_filter = None # BlueprintFilter()
        self._value_keys_to_use = set(VALUE_KEYS)

    def load_blueprint(self):
        self._error_msg = None
        p = Path(self._path_to_blueprint).expanduser()
        if p.exists():
            self._blueprint_text = p.read_text()
            self.blueprint_data = utils.string_to_JSON(self._blueprint_text)
        else:
            self._error_msg = f'Failed to find this file: {self._path_to_blueprint}.'

    def adjust_keys_to_return(self, keep:list[str]=None, drop:list[str]=None)->None:
        """
        Add and/or remove keys to apply to the filter.
        """
        if keep is not None:
            self._value_keys_to_use.update(keep)
        if drop is not None:
            self._value_keys_to_use.difference_update(drop)

    def _run_filter(self):
        self._bp_filter = BlueprintFilter(self.blueprint_data, OBJECT_KEYS, self._value_keys_to_use)

    def get_error_msg(self):
        return self._error_msg

    def get_filtered_data(self)->dict:
        """
        Return a dict filtered by settings.

        TODO: add customizable settings.
        """
        self._run_filter()
        return self._bp_filter.filter()

    def get_root_key(self)->str:
        """
        Returns the key at the root of the *filtered* data.
        """
        if self._bp_filter is None:
            self._run_filter()
        root_keys = self._bp_filter.filter().keys()
        if len(root_keys) == 1:
            return list(root_keys)[0]
        else:
            self._error_msg = f"More than one root key: {root_keys}"
