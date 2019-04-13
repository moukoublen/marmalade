from typing import List


class Exceptions():
    @classmethod
    def single_env_not_exist(c, env: str) -> Exception:
        return Exception("Environment {} does not exist".format(env))

    @classmethod
    def envs_not_exist(c, envs: List[str]) -> Exception:
        return Exception("Environments {} do not exist".format(str(envs)))
