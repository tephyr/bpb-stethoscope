"""Blueprint info"""

import json
from pathlib import Path

import click

from draftsman import utils
from draftsman.blueprintable import BlueprintBook, Blueprint

import info


@click.group()
def cli():
    pass

@cli.command(help="See information about the items contained within this blueprint or blueprint book.")
@click.option('--debug', '-d', is_flag=True, default=False, help="Activate debug mode.")
@click.argument('bptext', type=click.Path(exists=True))
def blueprint_info(bptext:str, debug:bool=False):
    data = Path(bptext).read_text()

    bp_dict = utils.string_to_JSON(data)
    print(f'Keys in text: {bp_dict.keys()}')

    data = info.parse_and_report(data)
    info.report_hierarchy(data)

    if 'blueprint' in bp_dict.keys():
        # iterate through blueprint.
        pass
    elif 'blueprintbook' in bp_dict.keys():
        # Iterate through blueprint book.
        pass

        # for book in data['books']:
        #     print(f'BlueprintBook: {book["label"]}, icons: {",".join(book.get("icons", []))}')
        #     for bp in book.get('blueprints', []):
        #         iconsString = '' if 'icons' not in bp else 'icons:' + ','.join(bp['icons'])
        #         print(f'\tBlueprint: {bp["label"]}', iconsString, sep = ', ')
        #         # API: required; data: optional
        #         apiLine = f'\t\tAPI: {bp.get("api", "MISSING API")}'
        #         if bp.get('api', ['?'])[0] not in blueprints.BLUEPRINTS_BY_API:
        #             apiLine += ' [UNKNOWN API]'

        #         if 'data' in bp:
        #             apiLine += f' with {get_data_path(instructions, bp["data"])}'
        #         print(apiLine, '\n')


if __name__ == '__main__':
    cli()
