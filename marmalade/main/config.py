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
    def __init_config():
        ConfigStore.config = MarmaladeConfig()
        ConfigStore.config.envs_path = str(Path.home()) + "/.marmalade.envs"

    @staticmethod
    def get_config() -> MarmaladeConfig:
        if ConfigStore.is_empty:
            ConfigStore.__init_config()
        return ConfigStore.config
