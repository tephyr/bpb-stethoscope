from draftsman.blueprintable import BlueprintBook, Blueprint, get_blueprintable_from_string

def parse_and_report(bp_str):
    """Basic info about the given blueprint."""
    bp = get_blueprintable_from_string(bp_str)
    print(f'type(bp): {type(bp)}')

    if isinstance(bp, Blueprint):
        print('instance of Blueprint')
    elif isinstance(bp, BlueprintBook):
        print('instance of BlueprintBook')
    else:
        print('unhandled instance')

def report_hierarchy(data):
    pass
