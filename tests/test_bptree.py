import pytest

import helpers

from bptree import BPTree

@pytest.fixture(scope="module", params=('blueprint.single.txt', 'blueprintbook.simple.txt', 'blueprintbook.less-simple.txt'))
def get_a_txt(request):
    return helpers.load_txt_by_name(request.param)

class TestBPTree():

    # @pytest.fixture(scope="class", autouse=True)
    # def get_txt(self):
    #     def _get_txt(file_name:str):
    #         return helpers.load_txt_by_name(file_name)

    #     return _get_txt

    def test_basics(self, get_a_txt):
        """Happy path."""
        bp_tree = BPTree(blueprint_string=get_a_txt)
        assert type(bp_tree.blueprint_data) is dict, "blueprint_data must always be a dict."
        assert len(bp_tree.blueprint_data.keys()) == 1, "blueprint_data must have only 1 key."

    @pytest.mark.skip
    def test_load_single_blueprint(self):
        pass

    @pytest.mark.skip
    def test_load_blueprintbook(self):
        pass

    @pytest.mark.skip
    def test_adjust_keys(self):
        pass

    @pytest.mark.skip
    def test_get_filtered_data(self):
        pass

    @pytest.mark.skip
    def test_get_root_key(self):
        pass
