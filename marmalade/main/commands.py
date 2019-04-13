from marmalade.utils.env import Env
from marmalade.utils.version import Version
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class InstallCommand(Command):
    def __init__(self, env: Env, version: Version = None):
        self.env = env
        self.version = version

    def latest_version(self) -> bool:
        return self.version is None

    def get_version_to_install(self) -> Version:
        if(self.latest_version):
            return self.env.get_remote_version()
        else:
            return self.version

    def execute(self):
        ver_to_install = self.get_version_to_install()
        if not self.env.is_installed():
            self.env.install_version(ver_to_install)
        else:
            print("Env {} already instlled".format(self.env.get_name()))


class UpdateCommand(Command):
    def __init__(self, env: Env):
        self.env = env

    def execute(self):
        self.env.update()
