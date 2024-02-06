"""
Test helpers
"""
import json
from pathlib import Path

def load_json_by_name(file_name:str)->dict:
    """
    Load a JSON file into a dict & return it.

    Assumes all paths are relative to ./data/.
    """
    # print(f'{__name__=}, {__file__=}')
    # print(f'{__name__=}, {__path__=}')
    test_root = Path(__file__).parent
    path_data = test_root / 'data' / file_name
    # print(f'{path_data=}')
    # print(path_data.read_text())
    return json.loads(path_data.read_text())
