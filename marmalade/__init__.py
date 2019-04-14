"""Top-level module for marmalade.

This module

- initializes logging for the command-line tool
- provides a way to configure logging for the command-line tool
- Initializes the main configuration

"""
from marmalade.utils.logger import LOG
from marmalade.main.config import ConfigStore

LOG.initalize_logger()
LOG.debug("Initializing")
ConfigStore.init_config()
