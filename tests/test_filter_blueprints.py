import pytest

import filter_blueprints

import helpers

class TestBlueprintSingle():
    """Test a single blueprint"""
    JSON_FILE = 'blueprint.single.json'

    @pytest.fixture
    def original_data(self):
        return helpers.load_json_by_name(self.JSON_FILE)
        
    def test_single_blueprint_default(self, original_data):
        """
        Test a single blueprint with default values for filter.
        
        ``label`` is NOT included by default.
        """
        filter_worker = filter_blueprints.BlueprintFilter(original_data)
        expected = {
          "blueprint": {
            "item": "blueprint"
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

class TestBlueprintBookSingleLevel():
    """
    Test a single blueprintbook with one level of children.

    ``blueprintbook.simple.json``: one blueprintbook containing 3 blueprints, each with a single assembler (levels 1-3) set to produce wood, iron, and steel chests
    """

    JSON_FILE = 'blueprintbook.simple.json'

    @pytest.fixture(scope="class")
    def original_data(self):
        return helpers.load_json_by_name(self.JSON_FILE)

    def test_single_blueprintbook_default(self, original_data):
        """Test a single blueprint book with default values."""
        filter_worker = filter_blueprints.BlueprintFilter(original_data)
        expected = {
            "blueprint_book": {
                "item": "blueprint-book",
                "blueprints": [
                    {"blueprint": {"item": "blueprint"} },
                    {"blueprint": {"item": "blueprint"} },
                    {"blueprint": {"item": "blueprint"} }
                ]
            }
        }

        assert filter_worker.filter() == expected

    # @pytest.mark.skip
    def test_single_blueprintbook_custom_value_keys(self, original_data, get_data):
        """Test a single blueprint book with custom values for filter."""
        filter_worker = filter_blueprints.BlueprintFilter(original_data, values_inclusive=('label', 'description', 'index', 'active_index'))
        expected = get_data('blueprintbook.simple.filtered.with-label-description.json')
        actual = filter_worker.filter()
        assert actual == expected
        print(f"{actual=}")
        assert 'entities' not in actual['blueprint_book']['blueprints'][0]['blueprint'].keys()

class TestBlueprintBookMultipleLevel():
    """
    Test a blueprint book containing a hierarchy of other blueprint books.
    """
    @pytest.mark.skip
    def test_multi_level_blueprintbook():
        """Test multiple levels of blueprintbooks."""
        assert False
