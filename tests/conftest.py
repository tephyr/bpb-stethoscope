"""Fixtures available for all tests"""
import pytest

from helpers import load_json_by_name, load_txt_by_name

LABELLED_TXT = (
    ('blueprint', 'blueprint.single.txt'),
    ('blueprint_book', 'blueprintbook.simple.txt'),
    ('blueprint_book', 'blueprintbook.less-simple.txt')
)

@pytest.fixture
def get_data():
    def _get_data(file_name:str):
        return load_json_by_name(file_name)

    return _get_data

@pytest.fixture
def get_a_txt():
    """
    Load a text file by name.

    Usage in test: ``get_a_txt('filename')`` 

    # Must add this fixture as an argument.
    """
    def _get_a_txt(file_name:str):
        return load_txt_by_name(file_name)

    return _get_a_txt

@pytest.fixture(params=LABELLED_TXT)
def get_every_txt_labelled(request):
    """
    Return a tuple of root_key, blueprint text.
    """
    return (request.param[0], load_txt_by_name(request.param[1]))
