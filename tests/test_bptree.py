import pytest
import snoop

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
        original_value_keys_length = len(bp_tree.get_current_filter_keys())

        # Send as list.
        bp_tree.adjust_keys_to_return(['foo'])
        assert len(bp_tree.get_current_filter_keys()) == original_value_keys_length + 1

        # Send as tuple.
        bp_tree.adjust_keys_to_return(('bar', ))
        assert len(bp_tree.get_current_filter_keys()) == original_value_keys_length + 2

        # Repeat inputs; should not change data.
        bp_tree.adjust_keys_to_return(('bar', 'foo'))
        assert len(bp_tree.get_current_filter_keys()) == original_value_keys_length + 2

        # Keep should overwrite drop in same call.
        bp_tree.adjust_keys_to_return(keep=['first', 'second'], drop=['second', 'third'])
        assert 'first' in bp_tree.get_current_filter_keys()
        assert 'second' in bp_tree.get_current_filter_keys(), "'second' should still be in list: keep overrides drop"

    def test_remove_keys(self, get_a_txt):
        bp_tree = BPTree(blueprint_string=get_a_txt('blueprint.single.txt'))
        # Remove label.
        assert 'label' in bp_tree.get_current_filter_keys()
        bp_tree.adjust_keys_to_return(drop=['label'])
        assert 'label' not in bp_tree.get_current_filter_keys()

    def test_get_filtered_data_blueprint(self, get_a_txt):
        bp_tree = BPTree(blueprint_string=get_a_txt('blueprint.single.txt'))
        assert type(bp_tree.get_filtered_data()) is dict
        # Ignore entities.
        bp_tree.adjust_keys_to_return(drop=['entities'])
        print(f'{bp_tree.get_current_filter_keys()=}')
        data = bp_tree.get_filtered_data()
        assert data['blueprint'].get('item') == 'blueprint'
        print(f'{data.keys()=}')
        assert 'entities' not in data['blueprint'].keys(), 'entities should have been filtered out of blueprint.'

    def test_get_filtered_data_blueprintbook(self, get_a_txt):
        """Filter a simple blueprintbook by adjusting the keys to keep ``index`` & drop ``entities``."""
        bp_tree = BPTree(blueprint_string=get_a_txt('blueprintbook.simple.txt'))
        data = bp_tree.get_filtered_data()
        assert type(data) is dict

        # Ignore entities.
        bp_tree.adjust_keys_to_return(keep=['index'], drop=['entities'])
        print(f'{bp_tree.get_current_filter_keys()=}')

        # Second call to .get_filtered_data().
        data = bp_tree.get_filtered_data()

        # Get first blueprint.
        filtered_bp = data['blueprint_book']['blueprints'][0]['blueprint']
        assert filtered_bp.get('item') == 'blueprint'

        snoop.pp(filtered_bp)
        # print(f'{data=}')
        print(f'{filtered_bp.keys()=}')

        for key in ['label']:
            assert key in filtered_bp.keys(), f'"{key}" should be in filtered blueprint.'
        assert 'entities' not in filtered_bp.keys(), 'entities should have been filtered out of blueprint.'


    # @pytest.mark.skip
    def test_get_root_key(self, get_every_txt_labelled):
        bp_tree = BPTree(blueprint_string=get_every_txt_labelled[1])
        root_key = bp_tree.get_root_key()
        assert root_key == get_every_txt_labelled[0], f"Got {root_key} instead of {get_every_txt_labelled[0]}"
