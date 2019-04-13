#  import argparse
from typing import List
import logging
import argparse
import marmalade
from marmalade.main.commands import Command, UpdateCommand, InstallCommand
from marmalade.main.errors import Exceptions
from marmalade.envs import Environments
from marmalade.utils.env import Env

LOG = logging.getLogger(__name__)


def _parse_single_update_command(env: str) -> UpdateCommand:
    if env in Environments:
        return UpdateCommand(Environments(env))
    else:
        raise Exceptions.single_env_not_exist(env)


def _get_envs_to_update(args: List[str]) -> List[Env]:
    if(len(args) == 0):
        return Environments.get_installed()
    else:
        return list(map(Environments, args))


def _parse_update_command(args: List[str]) -> List[Command]:
    if not all(e in Environments for e in args):
        not_valid = Environments.get_not_valid_names(args)
        raise Exceptions.envs_not_exist(not_valid)
    envs_to_update = _get_envs_to_update(args)
    return list(map(UpdateCommand, envs_to_update))


def _parse_install_command(args: List[str]) -> List[Command]:
    pass


def _parse_command_data(command: str, args: List[str]) -> List[Command]:
    if command == "install":
        return _parse_install_command(args)
    elif command == "update":
        return _parse_update_command(args)
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
    commands = _parse_command_data(args.command, restArgs)
    return {
        "command": args.command,
        "commands": commands,
        "verbose": args.verbose
    }


def main(argv=None):
    args = _args_parse()
    marmalade.configure_logging(args["verbose"])
    LOG.debug("Log level set to %s. Command (%s) rest args (%s)",
              args["verbose"],
              args["command"],
              args["commands"])
    print(args)
