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
    print(f'Keys in text: {bp_dict.keys()}; using file {bptext}')

    data = info.parse_text(data, debug)
    print()
    info.report_hierarchy(data)

if __name__ == '__main__':
    cli()
