from subprocess import call
import requests
from ..env import Env
from ..version import Version
from ..remoteversiongetter import RemoteVersionResolver


class RemoteVersionResolverNodeJS(RemoteVersionResolver):
    def __init__(self):
        self.url = "https://nodejs.org/dist/index.json"

    def get_latest_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        versions = map(Version, [item["version"][1:] for item in resp])
        return max(versions)

    def get_latest_lts_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        versions = map(
            Version,
            [item["version"][1:] for item in resp if item["lts"]]
        )
        return max(versions)


class EnvNode(Env):
    def __init__(self, envs_full_path: str):
        super().__init__(name="node",
                         envs_full_path=envs_full_path,
                         remote_version_resolver=RemoteVersionResolverNodeJS())
        self.__NODE_REL = "https://nodejs.org/dist/v{}/node-v{}-linux-x64.tar.xz"

    def get_download_link(self, version: Version) -> str:
        ver_str = version.get_version_string()
        return self.__NODE_REL.format(ver_str, ver_str)

    def install_file(self,
                     file_path_fp: str,
                     dest_dir_fp: str,
                     version: Version):
        call(["tar", "xf", file_path_fp, "--strip-components=1",
              "-C", dest_dir_fp])
