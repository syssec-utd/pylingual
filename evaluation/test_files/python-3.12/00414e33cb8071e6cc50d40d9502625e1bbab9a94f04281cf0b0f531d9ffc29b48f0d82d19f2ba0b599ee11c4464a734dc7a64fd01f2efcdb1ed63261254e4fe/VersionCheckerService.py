from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from dataclasses_json import config, dataclass_json
from injector import inject
from packaging.version import Version
from mobt.Cache.CacheInterface import CacheInterface
from mobt.JsonSerializer.JsonSerializerInterface import JsonSerializerInterface
from mobt.VersionChecker import version_checker_logger
from mobt.VersionChecker.Suppliers.LocalInstallation import LocalInstallation
from mobt.VersionChecker.Suppliers.PyPi import PyPi

def _version_encoder(version: Version) -> str:
    return str(version)

def _version_decoder(version: str) -> Version:
    return Version(version)

@dataclass_json
@dataclass(frozen=True)
class NewVersionAvailable:
    last_available_version: Version = field(metadata=config(encoder=_version_encoder, decoder=_version_decoder))
    installed_version: Version = field(metadata=config(encoder=_version_encoder, decoder=_version_decoder))
_cache_id = 'version_checker'

@inject
@dataclass(frozen=True)
class VersionCheckerService:
    cache: CacheInterface
    pypi_supplier: PyPi
    local_supplier: LocalInstallation
    json: JsonSerializerInterface

    def get_new_version_available(self) -> Optional[NewVersionAvailable]:
        new_available_version = self._try_get_available_version_from_cache()
        if not new_available_version:
            new_available_version = self._get_available_version_from_suppliers()
            if not new_available_version:
                return None
            _12_hours_in_the_future = datetime.now() + timedelta(hours=12)
            self.cache.save(_cache_id, self.json.to_json(new_available_version), _12_hours_in_the_future)
        if new_available_version.last_available_version > new_available_version.installed_version:
            version_checker_logger().debug(f'Never version available: "{new_available_version.last_available_version}, installed version: "{new_available_version.installed_version}"')
            return new_available_version
        version_checker_logger().debug(f'You have the last version available installed: "{new_available_version.installed_version}"')
        return None

    def _try_get_available_version_from_cache(self) -> Optional[NewVersionAvailable]:
        cache_entry = self.cache.get(_cache_id)
        if not cache_entry:
            return None
        return self.json.from_json(NewVersionAvailable, cache_entry.content)

    def _get_available_version_from_suppliers(self) -> Optional[NewVersionAvailable]:
        last_available_version = self.pypi_supplier.get_version()
        installed_version = self.local_supplier.get_version()
        if last_available_version is None or installed_version is None:
            version_checker_logger().debug(f'''Could not load the available versions. Last available version: "{last_available_version or 'None'}", installed version: "{installed_version or 'None'}"''')
            return None
        return NewVersionAvailable(last_available_version=last_available_version, installed_version=installed_version)