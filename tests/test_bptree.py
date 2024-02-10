import pytest

import helpers

from bptree import BPTree

@pytest.fixture(scope="module", params=('blueprint.single.txt', 'blueprintbook.simple.txt', 'blueprintbook.less-simple.txt'))
def get_every_txt(request):
    return helpers.load_txt_by_name(request.param)


class TestBPTree():

    def test_basics(self, get_every_txt):
        """Happy path."""
        bp_tree = BPTree(blueprint_string=get_every_txt)
        assert type(bp_tree.blueprint_data) is dict, "blueprint_data must always be a dict."
        assert len(bp_tree.blueprint_data.keys()) == 1, "blueprint_data must have only 1 key."

    def test_basic_requirements(self):
        """Throw an error if no file or string given."""
        with pytest.raises(RuntimeError):
            bp_tree = BPTree()

    def test_adjust_keys(self, get_every_txt):
        bp_tree = BPTree(blueprint_string=get_every_txt)
        original_value_keys_length = len(bp_tree._value_keys_to_use)
        # Send as list.
        bp_tree.adjust_keys_to_return(['foo'])
        assert len(bp_tree._value_keys_to_use) == original_value_keys_length + 1
        # Send as tuple.
        bp_tree.adjust_keys_to_return(('bar', ))
        assert len(bp_tree._value_keys_to_use) == original_value_keys_length + 2
        # Repeat inputs; should not change data.
        bp_tree.adjust_keys_to_return(('bar', 'foo'))
        assert len(bp_tree._value_keys_to_use) == original_value_keys_length + 2

    def test_remove_keys(self, get_a_txt):
        bp_tree = BPTree(blueprint_string=get_a_txt('blueprint.single.txt'))
        # Remove label.
        assert 'label' in bp_tree._value_keys_to_use
        bp_tree.adjust_keys_to_return(drop=['label'])
        assert 'label' not in bp_tree._value_keys_to_use

    def test_get_filtered_data(self, get_every_txt):
        bp_tree = BPTree(blueprint_string=get_every_txt)
        assert type(bp_tree.get_filtered_data()) is dict

    # @pytest.mark.skip
    def test_get_root_key(self, get_every_txt_labelled):
        bp_tree = BPTree(blueprint_string=get_every_txt_labelled[1])
        root_key = bp_tree.get_root_key()
        assert root_key == get_every_txt_labelled[0], f"Got {root_key} instead of {get_every_txt_labelled[0]}"
