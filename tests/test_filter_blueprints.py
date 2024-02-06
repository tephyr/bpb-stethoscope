import pytest

import filter_blueprints

import helpers

class TestBlueprintSingle():
    """Test a single blueprint"""
    JSON_FILE = 'blueprint.single.json'

    @pytest.fixture
    def original_data(self):
        return helpers.load_json_by_name('blueprint.single.json')
        
    def test_single_blueprint_default(self, original_data):
        """Test a single blueprint with default values for filter."""
        filter_worker = filter_blueprints.BlueprintFilter(original_data)
        expected = {
          "blueprint": {
            "item": "blueprint",
            # "label": "Single blueprint" # This is NOT included by default.
          }
        }
        assert filter_worker.filter() == expected

    def test_single_blueprint_custom_value_keys(self, original_data):
        """Test a single blueprint with custom values for filter."""
        filter_worker = filter_blueprints.BlueprintFilter(original_data, values_inclusive=('version', 'label'))
        expected = {
          "blueprint": {
            "item": "blueprint",
            "version": 281479274299391,
            "label": "Single blueprint"
          }
        }
        assert filter_worker.filter() == expected

# def test_single_blueprintbook():
#     """Test a single blueprintbook with only direct blueprint children."""
#     assert False

# def test_multi_level_blueprintbook():
#     """Test multiple levels of blueprintbooks."""
#     assert False

