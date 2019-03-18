from abc import ABC, abstractmethod
from distutils.version import LooseVersion  # , StrictVersion


class _VersionComparable(ABC):
    @abstractmethod
    def get_version_string(self):
        pass

    def as_comparable(self):
        return LooseVersion(self.get_version_string())

    def __lt__(self, other):
        return self.as_comparable() < other.as_comparable()

    def __le__(self, other):
        return self.as_comparable() <= other.as_comparable()

    def __gt__(self, other):
        return self.as_comparable() > other.as_comparable()

    def __ge__(self, other):
        return self.as_comparable() >= other.as_comparable()

    def __eq__(self, other):
        return self.as_comparable() == other.as_comparable()

    def __ne__(self, other):
        return self.as_comparable() != other.as_comparable()


class Version(_VersionComparable):
    def __init__(self, version_string):
        self.__version_string = version_string

    def get_version_string(self):
        return self.__version_string

    def __str__(self):
        return "Version({})".format(self.get_version_string())

    def __repr__(self):
        return self.__str__()


ZERO_VERSION = Version("0.0.0")
