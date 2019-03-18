from marmalade.envs.docker import EnvDockerCompose, EnvDockerMachine
from marmalade.envs.gradle import EnvGradle
from marmalade.envs.node import EnvNode
from marmalade.main.config import ConfigStore


__config__ = ConfigStore.get_config()
__env_path__ = __config__.envs_path

ENVS_MAP = {
    "node": EnvNode(__env_path__),
    "gradle": EnvGradle(__env_path__),
    "docker-compose": EnvDockerCompose(__env_path__),
    "docker-machine": EnvDockerMachine(__env_path__)
}


def get_all_envs():
    return ENVS_MAP.values
