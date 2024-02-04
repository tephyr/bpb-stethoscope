"""Blueprint info"""

import json
import logging
from pathlib import Path
import pprint

import click

from draftsman import utils
from draftsman.blueprintable import BlueprintBook, Blueprint

import info
import totals_reporter

## GLOBALS ##
logger = None

@click.group()
def cli():
    pass

@cli.command()
@click.option('--debug', '-d', is_flag=True, default=False, help="Activate debug mode.")
@click.argument('blueprint_path', type=click.Path(exists=True))
def blueprint_info(blueprint_path:str, debug:bool=False):
    """
    See information about the items contained within this blueprint or blueprint book.

    BLUEPRINT_PATH: full path to blueprint file.
    """
    _setup_logger(debug=debug)
    data = Path(blueprint_path).read_text()

    bp_dict = utils.string_to_JSON(data)
    logger.debug(f'Keys in text: {bp_dict.keys()}; using file {blueprint_path}')

    data = info.parse_text(data, debug)
    info.report_hierarchy(data)

@cli.command()
@click.option('--totals', '-t', is_flag=True, default=False, help="Show totals.")
@click.option('--log-level', '-l',
    type=click.Choice(('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), case_sensitive=False),
    default="CRITICAL",
    help='Log level.')
@click.option('--debug', '-d', is_flag=True, default=False, help="Activate debug mode (overrides --log-level).")
@click.argument('blueprint_path', type=click.Path(exists=True))
def blueprint_raw(blueprint_path:str, totals:bool=False, log_level:str='CRITICAL', debug:bool=False):
    """
    'Raw' representation of the blueprint.

    BLUEPRINT_PATH: full path to blueprint file.
    """
    _setup_logger(log_level, debug)

    data = Path(blueprint_path).read_text()
    size_in_kb = Path(blueprint_path).stat().st_size / 1024
    size_in_kb_hr = f'{size_in_kb:,.1f}'
    logger.info('Printing blueprint "%s", size %skb', blueprint_path, size_in_kb_hr)
    bp_dict = utils.string_to_JSON(data)

    if totals:
        for item in totals_reporter.count_items_and_report(bp_dict):
            logger.info('%s: %s', item[0], item[1])
    else:
        logger.info(pprint.pprint(bp_dict))


def _setup_logger(log_level:str='CRITICAL', debug:bool=False):
    ## SETUP LOGGER ##
    global logger
    logger = logging.getLogger('bpi')
    if debug:
        # print(f'{log_level=}, {debug=}')
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
