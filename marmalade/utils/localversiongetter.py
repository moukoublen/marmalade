from abc import ABC, abstractmethod
import os
from os.path import isdir, islink, join
from typing import List  # , Tuple
from marmalade.utils.version import Version, ZERO_VERSION


class LocalVersionResolver(ABC):
    @abstractmethod
    def get_local_latest_version(self):
        pass

    @abstractmethod
    def get_local_versions(self):
        pass


class DefaultLocalVersionResolver(LocalVersionResolver):
    def __init__(self, envs_abs_path, env_name):
        self._envs_abs_path = envs_abs_path
        self._env_name = env_name
        self._env_full_path = join(self._envs_abs_path, self._env_name)

    def __get_local_dirs__(self) -> List[str]:
        if isdir(self._env_full_path):
            return os.listdir(self._env_full_path)
        else:
            return []

    def get_local_versions(self) -> List[Version]:
        def fp(dir_name):
            return join(self._env_full_path, dir_name)

        def dir_and_not_link(dir_name):
            return (isdir(fp(dir_name)) and not(islink(fp(dir_name))))

        def local_dirs_only():
            return [i for i in self.__get_local_dirs__()
                    if dir_and_not_link(i)]

        versions = list(map(Version, local_dirs_only()))
        versions.sort(reverse=True)
        return versions

    def get_local_latest_version(self) -> Version:
        versions = self.get_local_versions()
        versions.append(ZERO_VERSION)
        return max(versions)

    def has_version_installed(self, v: Version) -> bool:
        loval_versions = self.get_local_versions()
        return v in loval_versions
