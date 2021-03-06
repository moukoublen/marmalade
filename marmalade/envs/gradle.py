from subprocess import call
from os import system
from marmalade.utils.env import Env
from marmalade.utils.version import Version
from marmalade.utils.remoteversiongetter import RemoteVersionResolverGitHub


class EnvGradle(Env):
    def __init__(self, envs_full_path: str):
        rvr = RemoteVersionResolverGitHub("gradle/gradle")
        super().__init__(name="gradle",
                         envs_full_path=envs_full_path,
                         remote_version_resolver=rvr)
        self.__URL = \
            "https://services.gradle.org/distributions/gradle-{}-bin.zip"

    def get_download_link(self, version: Version) -> str:
        ver_str = version.get_version_string()
        return self.__URL.format(ver_str, ver_str)

    def install_file(self,
                     file_path_fp: str,
                     dest_dir_fp: str,
                     version: Version):
        unziped_folder = dest_dir_fp + "/gradle-" + \
                         version.get_version_string()
        call(["unzip", "-qq", file_path_fp, "-d", dest_dir_fp])
        system("mv " + unziped_folder + "/* " + dest_dir_fp)
        call(["rm", "-rf", unziped_folder])
