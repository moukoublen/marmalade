from subprocess import call
from os.path import join
from marmalade.utils.env import Env
from marmalade.utils.version import Version
from marmalade.utils.download import github_download_link
from marmalade.utils.remoteversiongetter import RemoteVersionResolverGitHub


class _EnvDockerModules(Env):
    def __init__(self,
                 name: str,
                 envs_full_path: str,
                 repo: str,
                 download_link_postfix: str,
                 filename: str):
        rvr = RemoteVersionResolverGitHub(repo)
        super().__init__(name=name,
                         envs_full_path=envs_full_path,
                         remote_version_resolver=rvr)
        self._repo = repo
        self._download_link_postfix = download_link_postfix
        self._filename = filename

    def get_download_link(self, version: Version) -> str:
        ver_str = version.get_version_string()
        return github_download_link(
            repo=self._repo,
            postfix_file=self._download_link_postfix.format(ver_str)
        )

    def install_file(self,
                     file_path_fp: str,
                     dest_dir_fp: str,
                     version: Version):
        dst_file = join(dest_dir_fp, self._filename)
        call(["cp", file_path_fp, dst_file])
        call(["chmod", "+x", dst_file])


class EnvDockerCompose(_EnvDockerModules):
    def __init__(self, envs_full_path: str):
        super().__init__(
            name="compose",
            envs_full_path=envs_full_path,
            repo="docker/compose",
            download_link_postfix="{}/docker-compose-Linux-x86_64",
            filename="docker-compose"
        )


class EnvDockerMachine(_EnvDockerModules):
    def __init__(self, envs_full_path: str):
        super().__init__(
            name="docker-machine",
            envs_full_path=envs_full_path,
            repo="docker/machine",
            download_link_postfix="{}/docker-machine-Linux-x86_64",
            filename="docker-machine"
        )
