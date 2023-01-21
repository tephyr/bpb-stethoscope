from draftsman.blueprintable import BlueprintBook, Blueprint, get_blueprintable_from_string

def parse_and_report(bp_str:str):
    """Basic info about the given blueprint."""
    bp = get_blueprintable_from_string(bp_str)
    print(f'type(bp): {type(bp)}')

    if is_blueprint(bp):
        print('instance of Blueprint')
    elif is_blueprintbook(bp):
        print('instance of BlueprintBook')
    else:
        print('unhandled instance')

    return bp

def report_hierarchy(data):
    print('\n'.join(report_metadata(data)))

def report_metadata(data) -> list:
    """Report on title, description, icons."""
    result = []
    if is_blueprint(data):
        result.append(f'label: {data.label}')
        if data.description and len(data.description):
            result.append(f'{data.description}')
        if data.icons and len(data.icons):
            result.append(f"icons: {', '.join(simplify_icons(data.icons))}")

        result.append(f'# of entities: {len(data.entities)}')
        for k, v in report_entities(data).items():
            result.append(f'{k}: {v}')
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
