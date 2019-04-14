"""Top-level module for marmalade.

This module

- initializes logging for the command-line tool
- provides a way to configure logging for the command-line tool
- Initializes the main configuration

"""
import logging
import sys
from logging import NullHandler
from marmalade.main.config import ConfigStore
from marmalade.utils.logger import LoggerWrapper

_LOG_LEVEL = {
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO,
    3: logging.DEBUG,
}

_LOG_FORMAT = ("%(name)-10s %(levelname)-6s %(message)s")


def _set_stdout_handler(logger):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    logger.addHandler(handler)


def _init_logger():
    logger = logging.getLogger(__name__)
    logger.addHandler(NullHandler())
    _set_stdout_handler(logger)
    return logger


_LOG = _init_logger()

LOG = LoggerWrapper(_LOG)


def set_log_level(verbosity):
    if verbosity <= 0:
        verbosity = 0
    if verbosity > 3:
        verbosity = 3
    _LOG.setLevel(_LOG_LEVEL[verbosity])
    _LOG.debug("Log level set to %s",
               logging.getLevelName(_LOG_LEVEL[verbosity]))


ConfigStore.init_config()
