from typing import List
from marmalade.main.config import ConfigStore
from marmalade.utils.env import Env

from marmalade.envs.docker import EnvDockerCompose, EnvDockerMachine
from marmalade.envs.gradle import EnvGradle
from marmalade.envs.node import EnvNode
from marmalade.envs.maven import EnvMaven
from marmalade.envs.scala import EnvScala


def _create_envs(*env_constructor):
    path = ConfigStore.config.envs_path
    lst_envs = [ec(path) for ec in list(env_constructor)]
    return dict((e.get_name(), e) for e in lst_envs)


def _default_envs():
    return _create_envs(
        EnvNode,
        EnvGradle,
        EnvDockerCompose,
        EnvDockerMachine,
        EnvMaven,
        EnvScala
    )


class _Environments_MetaClass(type):
    def __getitem__(c, name):
        return c.all[name]

    def __call__(c, name):
        return c.all[name]

    def __contains__(c, elem):
        if type(elem) == str:
            return elem in c.all.keys()
        return False

    def __len__(c):
        return len(c.all.values())

    def __iter__(c):
        for v in c.all.values():
            yield v


class Environments(metaclass=_Environments_MetaClass):
    all = _default_envs()

    @classmethod
    def is_name_valid(c, name: str) -> bool:
        return name in c.all.keys()

    @classmethod
    def get_not_valid_names(c, names: List[str]) -> List[str]:
        return list(filter(lambda e: not c.is_name_valid(e), names))

    @classmethod
    def get_installed(c) -> List[Env]:
        return list(filter(lambda e: e.is_installed(), c))
