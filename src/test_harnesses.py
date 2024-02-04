"""
Test harnesses.
"""
import logging
import pprint
import sys

import click
import snoop
snoop.install()

from bptree import BPTree
import filter_blueprints

logger = None

@click.group()
def cli():
    pass

@cli.command()
@click.argument('blueprint_path', type=click.Path(exists=True))
def debug_filter_blueprints(blueprint_path:str):
    """
    Read a filtered blueprint.
    """
    _setup_logger('DEBUG')
    logger.debug('START debug_filter_blueprints')

    # Load data.
    bp_tree = BPTree(blueprint_path)
    if bp_tree.get_error_msg():
        logger.warning(bp_tree.get_error_msg())
    pp = pprint.PrettyPrinter(indent=0)
    if True:
        logger.info(bp_tree.blueprint_data)
    else:
        logger.info(pp.pformat(bp_tree.blueprint_data))

    keys_to_keep = ('blueprint_book', 'blueprint', 'blueprints', 'label', 'description')
    if False:
        bp_filtered_tree = filter_blueprints.filter_blueprints(bp_tree.blueprint_data, keys_to_keep)
        worker = filter_blueprints.BlueprintFilter(bp_tree.blueprint_data, None, ('label', 'description'))
        bp_filtered_tree = worker.filter()
        logger.info("Filtered tree:")
        logger.info(pp.pformat(bp_filtered_tree))
        logger.debug('END debug_filter_blueprints')
    else:
        logger.info("Filtered tree:")
        logger.info(pp.pformat(bp_tree.get_filtered_data()))
        logger.debug('END debug_filter_blueprints')


def _setup_logger(log_level:str='CRITICAL'):
    ## SETUP LOGGER ##
    global logger
    logger = logging.getLogger('stethoscope.tests')
    logger.setLevel(log_level)
    bf = logging.Formatter('[{name}] {message}', style='{')
    handler = logging.StreamHandler()
    handler.setFormatter(bf)
    logger.addHandler(handler)
    ## END LOGGER SETUP ##

if __name__ == '__main__':
    cli()
