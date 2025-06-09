"""
Configuration section for treesync targets
"""
from typing import List, Optional
from sys_toolkit.configuration.base import ConfigurationSection
from ..target import Target
from .servers import ServersConfigurationSection

class TargetConfiguration(ConfigurationSection):
    """
    Loader for named targets in TargetSettings
    """
    source: str = ''
    destination: str = ''
    ignore_default_flags: bool = False
    ignore_default_excludes: bool = False
    excludes_file: str = None
    excludes: List[str] = []
    flags: List[str] = []
    iconv: Optional[str] = None
    __default_settings__ = {'ignore_default_flags': False, 'ignore_default_excludes': False, 'excludes': [], 'excludes_file': None, 'flags': [], 'iconv': None}
    __required_settings__ = ('source', 'destination')

    def __repr__(self) -> str:
        return f'{self.source} {self.destination}'

    @property
    def hostname(self) -> str:
        """
        Get hostname from target name (with host:target syntax)
        """
        try:
            host, _path = str(self.destination).split(':', 1)
            return host
        except ValueError:
            return None

    @property
    def destination_server_settings(self) -> Optional[ServersConfigurationSection]:
        """
        Return settings for destination server
        """
        if not self.hostname:
            return None
        return getattr(self.__config_root__.servers, self.hostname, None)

    @property
    def destination_server_flags(self) -> List[str]:
        """
        Return flags specific to destination server
        """
        flags = []
        settings = self.destination_server_settings
        if settings is not None:
            server_flags = settings.get('flags', [])
            if server_flags:
                flags.extend(server_flags)
            iconv = settings.get('iconv', None)
            if iconv is not None:
                flags.append(f'--iconv={iconv}')
            rsync_path = settings.get('rsync_path', None)
            if rsync_path is not None:
                flags.append(f'--rsync-path={rsync_path}')
        return flags

class TargetsConfigurationSection(ConfigurationSection):
    """
    Tree sync targets by name
    """
    __name__ = 'targets'
    __dict_loader_class__ = TargetConfiguration

    @property
    def names(self) -> List[str]:
        """
        Get configured target names
        """
        names = []
        for attr in vars(self):
            section = getattr(self, attr)
            if isinstance(section, self.__dict_loader_class__):
                names.append(attr)
        return names

    def __iter__(self):
        targets = [getattr(self, name) for name in self.names]
        return iter(targets)

    @property
    def sync_targets(self) -> List[Target]:
        """
        List of all sync targets
        """
        targets = []
        for name in self.names:
            targets.append(self.get(name))
        return targets

    def get(self, name) -> Target:
        """
        Get target by name
        """
        target_config = getattr(self, name, None)
        if target_config is None:
            raise ValueError(f'Invalid target name {name}')
        return Target(target_config.hostname, name, target_config.source, target_config.destination, target_config)