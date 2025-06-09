from __future__ import annotations
from enum import Enum
from typing import Dict, List, Set
from .mod_loaders import ModLoaders
from .sites import Sites

class Stabilities(Enum):
    release = 'release'
    beta = 'beta'
    alpha = 'alpha'
    unknown = 'unknown'

    @staticmethod
    def from_name(name: str) -> Stabilities:
        for stability in Stabilities:
            if stability.value.lower() == name.lower():
                return stability
        return Stabilities.unknown

class VersionInfo:

    def __init__(self, stability: Stabilities, mod_loaders: Set[ModLoaders], site: Sites, upload_time: int, minecraft_versions: List[str], download_url: str, number: str, filename: str='', mod_name: str='', dependencies: Dict[Sites, List[str]]={}) -> None:
        self.stability = stability
        self.mod_loaders = mod_loaders
        self.site_name = site
        self.upload_time = upload_time
        self.minecraft_versions = minecraft_versions
        self.download_url = download_url
        self.number = number
        self.filename = filename
        self.name = mod_name
        self.dependencies = dependencies

    def __str__(self) -> str:
        return f'{self.minecraft_versions}; uploaded {self.upload_time}'

    def __repr__(self) -> str:
        return str(self.__members())

    def __members(self):
        return (self.stability, self.mod_loaders, self.site_name, self.upload_time, self.minecraft_versions, self.download_url, self.number, self.filename, self.name, self.dependencies)

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return self.__members() == other.__members()
        return False

    def __hash__(self):
        return hash(self.__members())

    def __lt__(self, other: VersionInfo) -> bool:
        if self.upload_time < other.upload_time:
            return True
        if self.name < other.name:
            return True
        if self.site_name.value < other.site_name.value:
            return True
        return False

    def __le__(self, other: VersionInfo) -> bool:
        if self.upload_time <= other.upload_time:
            return True
        if self.name <= other.name:
            return True
        if self.site_name.value <= other.site_name.value:
            return True
        return False

    def __gt__(self, other: VersionInfo) -> bool:
        return not self.__le__(other)

    def __ge__(self, other: VersionInfo) -> bool:
        return not self.__lt__(other)