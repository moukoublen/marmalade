#  import argparse
from typing import List
import argparse
import re
from marmalade.utils.logger import LOG
from marmalade.main.commands import Command, UpdateCommand, InstallCommand
from marmalade.main.errors import Exceptions
from marmalade.envs import Environments
from marmalade.utils.env import Env
from marmalade.utils.version import Version


class _UpdateCommandParser():
    @classmethod
    def _get_envs_to_update(c, args: List[str]) -> List[Env]:
        if(len(args) == 0):
            return Environments.get_installed()
        else:
            return list(map(Environments, args))

    @classmethod
    def parse_update_command(c, args: List[str]) -> List[Command]:
        if not all(e in Environments for e in args):
            invalid = Environments.get_not_valid_names(args)
            raise Exceptions.envs_not_exist(invalid)
        envs_to_update = c._get_envs_to_update(args)
        return list(map(UpdateCommand, envs_to_update))


class _StrEnv:
    def __init__(self, env: str, version: str):
        self.env = env
        self.version = version


class _InstallCommandParser():
    r = re.compile(r"""([^@]*)(@([^$]+))?""")

    @classmethod
    def as_str_env(c, s: str) -> _StrEnv:
        m = c.r.match(s)
        return _StrEnv(m.group(1), m.group(3))

    @classmethod
    def as_command(c, e: _StrEnv) -> Command:
        env = Environments(e.env)
        version = None
        if e.version:
            version = Version(e.version)
        return InstallCommand(env, version)

    @classmethod
    def get_invalid_names(c, str_envs: List[_StrEnv]) -> List[str]:
        env_names = [a.env for a in str_envs]
        return Environments.get_not_valid_names(env_names)

    @classmethod
    def parse_install_command(c, args: List[str]) -> List[Command]:
        str_envs = [c.as_str_env(e) for e in args]
        invalid = c.get_invalid_names(str_envs)
        if len(invalid) > 0:
            raise Exceptions.envs_not_exist(invalid)
        return [c.as_command(e) for e in str_envs]


def _parse_command_data(command: str, args: List[str]) -> List[Command]:
    if command == "install":
        return _InstallCommandParser.parse_install_command(args)
    elif command == "update":
        return _UpdateCommandParser.parse_update_command(args)
    else:
        return list()


def _args_parse():
    parser = argparse.ArgumentParser(description="marmalade")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)"
    )
    parser.add_argument("command", choices=["install", "update"])
    args, restArgs = parser.parse_known_args()
    LOG.set_log_level(args.verbose)
    commands = _parse_command_data(args.command, restArgs)
    return {
        "command": args.command,
        "commands": commands
    }


def main(argv=None):
    args = _args_parse()
    for command in args["commands"]:
        command.execute()
