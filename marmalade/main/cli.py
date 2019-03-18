#  import argparse
import logging
import argparse
import marmalade

LOG = logging.getLogger(__name__)


def _add_install_command_parser(subparsers):
    parser = subparsers.add_parser("install")
    parser.add_argument("install_env", type=str, help="env name")
    parser.add_argument("version",
                        type=str,
                        default=argparse.SUPPRESS,
                        help="env version (optional)")


def _add_update_command_parser(subparsers):
    parser = subparsers.add_parser("update")
    parser.add_argument("update_envs", type=str, nargs="*", help="env name")


def _args_parse():
    parser = argparse.ArgumentParser(description="marmalade")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")
    parser.add_argument("command", choices=["install", "update"])
    args, restArgs = parser.parse_known_args()
    return {
        "command": args.command,
        "restArgs": restArgs,
        "verbose": args.verbose
    }


def main(argv=None):
    args = _args_parse()
    marmalade.configure_logging(args["verbose"])
    LOG.debug("Log level set to %s. Command (%s) rest args (%s)",
              args["verbose"],
              args["command"],
              args["restArgs"])
    print(args)
