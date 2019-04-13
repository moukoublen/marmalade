from pathlib import Path


class MarmaladeConfig(object):
    def __init__(self):
        self.envs_path = ""


class ConfigStore():
    config = None

    @staticmethod
    def is_empty() -> bool:
        return ConfigStore.config is None

    @staticmethod
    def init_config():
        ConfigStore.config = MarmaladeConfig()
        ConfigStore.config.envs_path = str(Path.home()) + "/.marmalade.envs"
