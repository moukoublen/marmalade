from abc import ABC, abstractmethod
import requests
from marmalade.utils.version import Version


class RemoteVersionResolver(ABC):
    @abstractmethod
    def get_latest_version(self) -> Version:
        pass

    @abstractmethod
    def get_latest_lts_version(self) -> Version:
        pass


class RemoteVersionResolverURL(RemoteVersionResolver):
    @abstractmethod
    def get_url(self) -> str:
        pass

    @abstractmethod
    def get_version_string(self, resp) -> str:
        pass

    def get_latest_version(self) -> Version:
        resp = requests.get(url=self.get_url()).json()
        str_ver = self.get_version_string(resp)
        return Version(str_ver)

    def get_latest_lts_version(self) -> Version:
        self.get_latest_version()


class RemoteVersionResolverGitHub(RemoteVersionResolverURL):
    __GITHUB_API = "https://api.github.com/repos/{}/releases/latest"

    def __init__(self, repo_path: str):
        self.url = RemoteVersionResolverGitHub.__GITHUB_API.format(repo_path)

    def get_version_string(self, resp) -> Version:
        return resp["name"]

    def get_url(self) -> Version:
        return self.url
