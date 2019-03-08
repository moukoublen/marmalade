"""Top-level module for marmalade.

This module

- initializes logging for the command-line tool
- provides a way to configure logging for the command-line tool

"""
import logging
import sys
from logging import NullHandler

# Default null log config
LOG = logging.getLogger(__name__)
LOG.addHandler(NullHandler())
del NullHandler

_LOG_LEVEL = {
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO,
    3: logging.DEBUG,
}

# LOG_FORMAT = ('%(name)-25s %(levelname)-8s %(message)s')


def configure_logging(verbosity):
    if verbosity <= 0:
        verbosity = 0
    if verbosity > 3:
        verbosity = 3
    handler = logging.StreamHandler(sys.stdout)
    # handler.setFormatter(logging.Formatter(LOG_FORMAT))
    LOG.addHandler(handler)
    LOG.setLevel(_LOG_LEVEL[verbosity])
