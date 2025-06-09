import os
import shutil
from collections import defaultdict
from collections.abc import ItemsView, KeysView, ValuesView
from itertools import chain
from pathlib import Path
from typing import IO, Any, Dict, List, Union
from urllib.parse import urlparse
from astropy.coordinates import EarthLocation
from astropy.units import Quantity
from tomlkit.exceptions import ParseError
from . import environ
from .data_type import RichParameters, ValueRange
from .exceptions import NECSTConfigurationError, NECSTParameterNameError
from .files import read
from .inform import get_logger
DefaultNECSTRoot = Path.home() / '.necst'
DefaultsPath = Path(__file__).parent / '..' / 'defaults'
logger = get_logger(__name__)
parsers = dict(location=lambda x: EarthLocation(**x), antenna_drive_range_az=lambda x: ValueRange(*map(Quantity, x)), antenna_drive_range_el=lambda x: ValueRange(*map(Quantity, x)), antenna_drive_warning_limit_az=lambda x: ValueRange(*map(Quantity, x)), antenna_drive_warning_limit_el=lambda x: ValueRange(*map(Quantity, x)), antenna_drive_critical_limit_az=lambda x: ValueRange(*map(Quantity, x)), antenna_drive_critical_limit_el=lambda x: ValueRange(*map(Quantity, x)), antenna_pointing_parameter_path=Path)

class Configuration(RichParameters):
    _instances: Dict[Union[str, None], List['Configuration']] = {}

    def __new__(cls, *args, **kwargs):
        if len(cls._instances) == 0:
            cls._instances[None] = [super().__new__(cls)]
        return cls._instances[None][0]

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except NECSTParameterNameError as e:
            raise NECSTConfigurationError from e

    @classmethod
    def from_file(cls, __path: Union[os.PathLike, str, IO]):
        try:
            return super().from_file(__path)
        except ParseError as e:
            raise NECSTConfigurationError from e

    @property
    def _dotnecst(self) -> str:
        from urllib.parse import urlparse
        try:
            url = urlparse(self._metadata.get('path', ''))
            scheme = f'{url.scheme}://' if url.scheme else ''
            path = url.path
            path = path.decode('utf-8') if isinstance(path, bytes) else path
            return scheme + url.netloc + str(Path(path).parent)
        except Exception:
            return ''

    def reload(self):
        """Reload the configuration.

        This method is to reflect the changes made to the configuration file or the
        change of environment variables.

        """
        path = find_config()
        original_prefix = self._prefix
        new = self.__class__.from_file(path)
        try:
            new = new.get(original_prefix)
        except KeyError:
            new = self.__class__()
        slots = chain.from_iterable((getattr(cls, '__slots__', []) for cls in self.__class__.__mro__))
        for attr in slots:
            setattr(self, attr, getattr(new, attr))
        for (key, parser) in parsers.items():
            try:
                self.attach_parsers(**{key: parser})
            except NECSTParameterNameError:
                pass
        for subcls in self.__class__.__subclasses__():
            for children in subcls._instances.values():
                [child.reload() for child in children]

    @classmethod
    def configure(cls):
        """Copy default configuration files into your local file system.

        Important
        ---------
        The files would be placed in ``$HOME/.necst/``. The file contents MUST BE
        UPDATED accordingly, before using this software to actually drive your
        telescope.

        Caution
        -------
        Running this software with misconfigured parameter files could result in
        catastrophic damage to your telescope, by many possible cause. The consequence
        can include: 1) the antenna becomes uncontrollable because the commands are
        calculated in positive feedback, 2) damage your receivers with applying too
        large voltage, and so on.

        """
        DefaultNECSTRoot.mkdir(exist_ok=True)
        for file in DefaultsPath.glob('*.toml'):
            _target_path = DefaultNECSTRoot / file.name
            if _target_path.exists():
                logger.error(f"'{_target_path}' already exists, skipping...")
                continue
            shutil.copyfile(file, _target_path)
        cls().reload()

    @property
    def parameters(self) -> Dict[str, Any]:
        unwrapped = {}
        for (k, v) in self._parameters.items():
            parsed = v.parsed
            if isinstance(parsed, Path):
                if urlparse(self._dotnecst).scheme:
                    unwrapped[k] = os.path.join(self._dotnecst, parsed)
                else:
                    unwrapped[k] = Path(self._dotnecst) / parsed
            else:
                unwrapped[k] = parsed
        return unwrapped

    def keys(self) -> KeysView:
        prefix_length = len(self._prefix) + 1 if self._prefix else 0
        return KeysView({k[prefix_length:]: v for (k, v) in self.parameters.items()})

    def values(self) -> ValuesView:
        return self.parameters.values()

    def items(self) -> ItemsView:
        prefix_length = len(self._prefix) + 1 if self._prefix else 0
        return ItemsView({k[prefix_length:]: v for (k, v) in self.parameters.items()})

    def __getitem__(self, key: str, /):
        item = super().__getitem__(key)
        if isinstance(item, Path):
            if urlparse(self._dotnecst).scheme:
                item = os.path.join(self._dotnecst, item)
            else:
                item = Path(self._dotnecst) / item
        return item

    def __getattr__(self, key: str, /):
        attr = super().__getattr__(key)
        if isinstance(attr, Path):
            if urlparse(self._dotnecst).scheme:
                attr = os.path.join(self._dotnecst, attr)
            else:
                attr = Path(self._dotnecst) / attr
        return attr

    def __add__(self, other: Any, /):
        if other is None:
            return self
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self._prefix == other._prefix:
            parameters = {k: v.parsed for (k, v) in self._parameters.items()}
            for (k, v) in other._parameters.items():
                if k in parameters and parameters[k] != v:
                    raise KeyError(f'Conflicting values for {k!r} found: {parameters[k]} and {v}.')
                parameters[k] = v
            parameters.update(other._parameters)
            inst = self.__class__(self._prefix, **parameters)
            return inst
        length = len(self._prefix) + 1
        prefix_stripped = {k[length:]: v.parsed for (k, v) in self._parameters.items() if k.startswith(self._prefix)}
        length = len(other._prefix) + 1
        prefix_stripped_other = {k[length:]: v.parsed for (k, v) in other._parameters.items() if k.startswith(other._prefix)}
        for (k, v) in prefix_stripped_other.items():
            if k in prefix_stripped and prefix_stripped[k] != v:
                raise KeyError(f'Conflicting values for {k!r} found: {prefix_stripped[k]!r} and {v!r}.')
            prefix_stripped[k] = v
        return self.__class__(**prefix_stripped)
    __radd__ = __add__

def find_config() -> str:
    """Look for the configuration file from environment variables and defaults."""
    root_candidates = [str(DefaultNECSTRoot)]
    specified = environ.necst_root.get()
    if specified is not None:
        root_candidates.insert(0, specified)
    config_file_name = 'config.toml'
    candidates = map(lambda x: os.path.join(x, config_file_name), root_candidates)
    for path in candidates:
        try:
            read(path)
            logger.info(f'Importing configuration from {path!r}')
            return path
        except FileNotFoundError:
            logger.debug(f'Config file not found at {path!r}')
    logger.error('Config file not found, using the default parameters. To create the file with default parameters, run `neclib.configure()`.')
    config_path = str(DefaultsPath / 'config.toml')
    return str(config_path)

class ConfigurationView(Configuration):
    """Sliced configuration."""
    __slots__ = ()
    _instances: Dict[str, List['ConfigurationView']] = defaultdict(list)

    def __new__(cls, prefix: str='', /, **kwargs):
        if prefix == '':
            return object().__new__(cls)
        if prefix not in cls._instances:
            new = object().__new__(cls)
            cls._instances[prefix].append(new)
            return new
        return cls._instances[prefix][0]

    def reload(self) -> None:
        try:
            filtered = self._metadata['parent'].get(self._prefix)
            self._parameters = filtered._parameters
            self._aliases = filtered._aliases
        except KeyError:
            self._metadata.pop('parent', None)
Configuration._view_class = ConfigurationView
config = Configuration()
'Collection of system-wide configurations.'
config.reload()
configure = Configuration.configure