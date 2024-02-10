"""Fixtures available for all tests"""
import pytest

from helpers import load_txt_by_name

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
