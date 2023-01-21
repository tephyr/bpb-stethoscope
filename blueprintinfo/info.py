from operator import itemgetter
import warnings

from draftsman.blueprintable import BlueprintBook, Blueprint, get_blueprintable_from_string
from draftsman.warning import RailAlignmentWarning

TRAILING_PRINT = '----------'

def parse_and_report(bp_str:str, debug:bool=False):
    """Basic info about the given blueprint."""
    bp = None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RailAlignmentWarning)

        bp = get_blueprintable_from_string(bp_str)

        if debug:
            print(f'type(bp): {type(bp)}')

        if is_blueprint(bp):
            print('instance of Blueprint')
        elif is_blueprintbook(bp):
            print('instance of BlueprintBook')
        else:
            print('unhandled instance')

        return bp

def parse_text(bp_str:str, debug:bool=False):
    """Parse into a blueprint/blueprintbook only."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RailAlignmentWarning)

        return get_blueprintable_from_string(bp_str)


def report_hierarchy(data):
    print('\n'.join(report_metadata(data)))

def report_metadata(data) -> list:
    """Report on title, description, icons."""
    result = []
    if is_blueprint(data):
        result.extend(get_blueprintable_metadata(data))
        result.append(f'# of entities: {len(data.entities)}')
        for ent, count in sort_entities_by_count(report_entities(data)):
            result.append(f'{ent}: {count}')

    elif is_blueprintbook(data):
        result.extend(get_blueprintable_metadata(data))
        result.append(f'# of blueprints: {len(data.blueprints)}')
        for bp in data.blueprints:
            result.extend(report_metadata(bp))


    if len(result) and result[-1] != TRAILING_PRINT:
        result.append(TRAILING_PRINT)
    return result

def get_blueprintable_metadata(data) -> list:
    result = []
    if data.label is None:
        result.append(f'{stringify_type(data)}: no label')
    else:
        result.append(f'{stringify_type(data)}: {data.label}')
    if data.description and len(data.description):
        result.append(f'{data.description}')
    if data.icons and len(data.icons):
        result.append(f"icons: {', '.join(simplify_icons(data.icons))}")
    return result

def report_entities(data):
    result = {}
    for e in data.entities:
        # Ignore hidden items/entities
        if e.hidden:
            continue
        if e.type in result:
            result[e.type] += 1
        else:
            result[e.type] = 1

    return result

def is_blueprint(data):
    return True if isinstance(data, Blueprint) else False

def is_blueprintbook(data):
    return True if isinstance(data, BlueprintBook) else False

def simplify_icons(icon_list:list):
    if len(icon_list):
        return [f'{x["signal"]["name"]}' for x in icon_list]

def stringify_type(data) -> str:
    if is_blueprint(data):
        return 'Blueprint'
    elif is_blueprintbook(data):
        return 'BlueprintBook'
    else:
        return 'Unknown'

def sort_entities_by_count(entities:dict) -> list:
    result = sorted(entities.items(), key=itemgetter(1), reverse=True)
    return result
