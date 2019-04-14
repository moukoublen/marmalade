import sys
import logging
from logging import NullHandler


class LoggerWrapper(object):
    _LOG_LEVEL = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    _LOG_FORMAT = ("%(levelname)-6s %(message)s")

    @classmethod
    def _init_logger(c, logger):
        logger.addHandler(NullHandler())
        c._set_stdout_handler(logger)

    @classmethod
    def _set_stdout_handler(c, logger):
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LoggerWrapper._LOG_FORMAT))
        logger.addHandler(handler)

    def initalize_logger(self):
        LoggerWrapper._init_logger(self._log)

    def __init__(self):
        self._log = logging.getLogger("marmalade")

    def set_log_level(self, verbosity):
        if verbosity <= 0:
            verbosity = 0
        if verbosity > 3:
            verbosity = 3
        lvl = LoggerWrapper._LOG_LEVEL[verbosity]
        self._log.setLevel(lvl)
        self._log.debug("Log level set to %s", logging.getLevelName(lvl))

    def debug(self, msg, *args, **kwargs):
        self._log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log.error(msg, *args, **kwargs)

    def log_update_start(self, env, ver):
        self._log.debug("%s will be updated form %s to %s",
                        env.get_name(),
                        env.get_local_version().get_version_string(),
                        ver.get_version_string())

    def log_already_updated(self, env):
        self._log.debug("%s is already updated in latest version %s",
                        env.get_name(),
                        env.get_local_version().get_version_string())

    def log_downloading(self, link):
        self._log.debug("Donwloading %s", link)

    def log_file_download_complete(self, file_path, install_path):
        self._log.debug("File downloaded at %s. Installing to %s", 
                        file_path,
                        install_path)

    def log_install_complete(self, env, version):
        self._log.debug("%s version %s installation completed", 
                        env.get_name(),
                        str(env.get_local_version().get_version_string()))


LOG = LoggerWrapper()
