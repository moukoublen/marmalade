from abc import ABC, abstractmethod
import os
from os.path import islink, join, exists
from marmalade.utils.logger import LOG
from marmalade.utils.download import get_file
from marmalade.utils.version import Version, ZERO_VERSION
from marmalade.utils.remoteversiongetter import RemoteVersionResolver
from marmalade.utils.localversiongetter import LocalVersionResolver
from marmalade.utils.localversiongetter import DefaultLocalVersionResolver


class Env(ABC):
    def __init__(self,
                 name: str,
                 envs_full_path: str,
                 remote_version_resolver: RemoteVersionResolver):
        self._name = name
        self._envs_full_path = envs_full_path
        self._rvr = remote_version_resolver
        self._lvr = self.__create_lvr__()

    def get_name(self) -> str:
        return self._name

    def is_installed(self) -> bool:
        return self.get_local_version() != ZERO_VERSION

    def is_version_installed(self, v: Version):
        return self._lvr.has_version_installed(v)

    def __create_lvr__(self) -> LocalVersionResolver:
        return DefaultLocalVersionResolver(
            envs_abs_path=self._envs_full_path,
            env_name=self._name
        )

    def get_env_full_path(self) -> str:
        return join(self._envs_full_path, self._name)

    def create_env_local_dir(self):
        if not(exists(self.get_env_full_path())):
            os.makedirs(self.get_env_full_path())

    def create_version_local_dir(self, ver: Version):
        full_path = self.get_dir_for_version_fp(ver)
        if not(exists(full_path)):
            os.makedirs(full_path)
        return full_path

    def get_env_default_dir_link_fp(self) -> str:
        return join(self.get_env_full_path(), "default")

    def get_dir_for_version_fp(self, version: Version) -> str:
        return join(self.get_env_full_path(), version.get_version_string())

    def get_local_version(self) -> Version:
        return self._lvr.get_local_latest_version()

    def get_remote_version(self) -> Version:
        return self._rvr.get_latest_version()

    def is_update_available(self) -> bool:
        return self.get_remote_version() > self.get_local_version()

    def update(self):
        if(not(self.is_update_available())):
            LOG.log_already_updated(self)
            return False
        latest_version = self.get_remote_version()
        LOG.log_update_start(self, latest_version)
        self.install_version(latest_version)
        self.make_default(latest_version)
        return True

    def install_version(self, version: Version):
        self.create_env_local_dir()
        dnl_link = self.get_download_link(version)
        LOG.log_downloading(dnl_link)
        downloaded_file_path = get_file(self.get_download_link(version))
        install_path = self.create_version_local_dir(version)
        LOG.log_file_download_complete(downloaded_file_path, install_path)
        self.install_file(downloaded_file_path,
                          install_path,
                          version)
        os.remove(downloaded_file_path)
        LOG.log_install_complete(self, version)

    def make_default(self, version: Version) -> bool:
        default = self.get_env_default_dir_link_fp()
        if exists(default) and islink(default):
            os.unlink(default)
        version_fp = self.get_dir_for_version_fp(version)
        if exists(version_fp):
            os.symlink(version_fp, default)
            return True
        return False

    # Abstract Methods #
    @abstractmethod
    def get_download_link(self, version: Version) -> str:
        pass

    @abstractmethod
    def install_file(self,
                     file_path_fp: str,
                     dest_dir_fp: str,
                     version: Version):
        pass
