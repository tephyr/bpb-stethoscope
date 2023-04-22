"""Blueprint info"""

import json
import logging
from pathlib import Path

import click

from draftsman import utils
from draftsman.blueprintable import BlueprintBook, Blueprint

import info

## GLOBALS ##
logger = None

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

@cli.command(help="'Raw' representation of the blueprint.")
@click.option('--log-level', '-l',
    type=click.Choice(('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), case_sensitive=False),
    default="CRITICAL",
    help='Select a log level.')
@click.argument('bptext', type=click.Path(exists=True))
def blueprint_raw(bptext:str, log_level:str='CRITICAL'):
    _setup_logger(log_level)


def _setup_logger(log_level:str='CRITICAL', debug:bool=False):
    ## SETUP LOGGER ##
    global logger
    logger = logging.getLogger('bpi')
    if debug:
        print(f'{dry_run=}, {log_level=}, {debug=}')
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(log_level)
    bf = logging.Formatter('[{name}] {message}', style='{')
    handler = logging.StreamHandler()
    handler.setFormatter(bf)
    logger.addHandler(handler)
    ## END LOGGER SETUP ##

if __name__ == '__main__':
    cli()
