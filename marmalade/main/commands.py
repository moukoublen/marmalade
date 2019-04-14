from marmalade.utils.logger import LOG
from marmalade.utils.env import Env
from marmalade.utils.version import Version
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class InstallCommand(Command):
    def __init__(self, env: Env, version: Version = None):
        self.env = env
        self.version = version

    def __str__(self):
        return "InstallCommand({}@{})".format(
            self.env.get_name(),
            str(self.version)
        )

    def is_latest_version(self) -> bool:
        return self.version is None

    def get_version_to_install(self) -> Version:
        if(self.is_latest_version()):
            return self.env.get_remote_version()
        else:
            return self.version

    def execute(self):
        ver_to_install = self.get_version_to_install()
        LOG.log_install_version_start(self.env, ver_to_install)
        if not self.env.is_version_installed(ver_to_install):
            self.env.install_version(ver_to_install)
        else:
            LOG.log_version_already_installed(self.env, ver_to_install)


class UpdateCommand(Command):
    def __init__(self, env: Env):
        self.env = env

    def __str__(self):
        return "UpdateCommand({})".format(self.env.get_name())

    def execute(self):
        self.env.update()
