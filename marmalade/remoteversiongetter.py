from abc import ABC, abstractmethod
import requests
from .version import Version

GITHUB_API = 'https://api.github.com/repos/{}/releases/latest'


class RemoteVersionResolver(ABC):
    @abstractmethod
    def get_latest_version(self) -> Version:
        pass

    @abstractmethod
    def get_latest_lts_version(self) -> Version:
        pass


class RemoteVersionResolverGitHub(RemoteVersionResolver):
    def __init__(self, repo_path: str):
        self.url = GITHUB_API.format(repo_path)

    def get_latest_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        return Version(resp['name'])

    def get_latest_lts_version(self) -> Version:
        self.get_latest_version()


class RemoteVersionResolverNodeJS(RemoteVersionResolver):
    def __init__(self):
        self.url = 'https://nodejs.org/dist/index.json'

    def get_latest_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        versions = map(Version, [item['version'][1:] for item in resp])
        return max(versions)

    def get_latest_lts_version(self) -> Version:
        resp = requests.get(url=self.url).json()
        versions = map(
            Version,
            [item['version'][1:] for item in resp if item['lts']]
        )
        return max(versions)
