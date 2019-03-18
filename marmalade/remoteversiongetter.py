from abc import ABC, abstractmethod
import requests
from .version import Version


class RemoteVersionResolver(ABC):
    @abstractmethod
    def get_latest_version(self) -> Version:
        pass

    @abstractmethod
    def get_latest_lts_version(self) -> Version:
        pass


class RemoteVersionResolverGitHub(RemoteVersionResolver):
    __GITHUB_API = "https://api.github.com/repos/{}/releases/latest"

    def __init__(self, repo_path: str):
        self.url = RemoteVersionResolverGitHub.__GITHUB_API.format(repo_path)

    def get_latest_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        return Version(resp["name"])

    def get_latest_lts_version(self) -> Version:
        self.get_latest_version()
