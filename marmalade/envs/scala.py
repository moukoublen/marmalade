from subprocess import call
from marmalade.utils.env import Env
from marmalade.utils.version import Version
from marmalade.utils.remoteversiongetter import RemoteVersionResolverGitHub


class RemoteVersionResolverScala(RemoteVersionResolverGitHub):
    def __init__(self):
        super().__init__("scala/scala")

    def get_version_string(self, resp) -> Version:
        return resp["tag_name"][1:]


class EnvScala(Env):
    def __init__(self, envs_full_path: str):
        rvr = RemoteVersionResolverScala()
        super().__init__(name="scala",
                         envs_full_path=envs_full_path,
                         remote_version_resolver=rvr)
        self.__URL = \
            "https://downloads.lightbend.com/scala/{}/scala-{}.tgz"

    def get_download_link(self, version: Version) -> str:
        ver_str = version.get_version_string()
        return self.__URL.format(ver_str, ver_str)

    def install_file(self,
                     file_path_fp: str,
                     dest_dir_fp: str,
                     version: Version):
        call(["tar", "xf", file_path_fp, "--strip-components=1",
              "-C", dest_dir_fp])
