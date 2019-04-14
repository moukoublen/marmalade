from subprocess import call
import requests
import urllib.parse
from marmalade.utils.env import Env
from marmalade.utils.version import Version
from marmalade.utils.remoteversiongetter import RemoteVersionResolver


class RemoteVersionResolverMaven(RemoteVersionResolver):
    _params = {
        "q": "g:org.apache.maven AND a:maven",
        "wt": "json",
        "start": 0,
        "rows": 1
    }

    def __init__(self):
        self.url = "https://search.maven.org/solrsearch/select?" + \
                   urllib.parse.urlencode(RemoteVersionResolverMaven._params)

    def get_latest_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        version = resp["response"]["docs"][0]["latestVersion"]
        return Version(version)

    def get_latest_lts_version(self) -> Version:
        return self.get_latest_version()


class EnvMaven(Env):
    def __init__(self, envs_full_path: str):
        super().__init__(name="maven",
                         envs_full_path=envs_full_path,
                         remote_version_resolver=RemoteVersionResolverMaven())
        self.__MVN_REL = \
            "http://www-us.apache.org/dist/maven/maven-3/{}/binaries/apache-maven-{}-bin.tar.gz"

    def get_download_link(self, version: Version) -> str:
        ver_str = version.get_version_string()
        return self.__MVN_REL.format(ver_str, ver_str)

    def install_file(self,
                     file_path_fp: str,
                     dest_dir_fp: str,
                     version: Version):
        call(["tar", "xf", file_path_fp, "--strip-components=1",
              "-C", dest_dir_fp])
