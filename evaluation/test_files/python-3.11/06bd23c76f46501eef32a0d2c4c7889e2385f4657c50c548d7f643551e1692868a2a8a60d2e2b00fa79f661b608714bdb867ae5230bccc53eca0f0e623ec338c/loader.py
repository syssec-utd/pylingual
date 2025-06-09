from __future__ import annotations
import logging
import urllib
from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Optional, Union
from dissect.target.helpers.lazy import import_lazy
from dissect.target.helpers.loaderutil import extract_path_info
if TYPE_CHECKING:
    from dissect.target import Target
__all__ = ['open', 'Loader', 'RawLoader', 'register']
log = logging.getLogger(__name__)
LOADERS: list[Loader] = []
LOADERS_BY_SCHEME: dict[str, Loader] = {}
MODULE_PATH = 'dissect.target.loaders'
DirLoader: Loader = import_lazy('dissect.target.loaders.dir').DirLoader
'A lazy loaded :class:`dissect.target.loaders.dir.DirLoader`.'
RawLoader: Loader = import_lazy('dissect.target.loaders.raw').RawLoader
'A lazy loaded :class:`dissect.target.loaders.raw.RawLoader`.'

class Loader:
    """A base class for loading a specific path and coupling it to a :class:`Target <dissect.target.target.Target>`.

    Implementors of this class are responsible for mapping any type of source data
    to a :class:`Target <dissect.target.target.Target>`.
    Whether that's to map all VMDK files from a VMX or mapping the contents of a zip file to a virtual filesystem,
    if it's something that can be translated to a "disk", "volume" or "filesystem", you can write a loader that
    maps it into a target.

    You can do anything you want to manipulate the :class:`Target <dissect.target.target.Target>` object
    in your ``map`` function, but generally you do one of the following:

    * open a :class:`Container <dissect.target.container.Container>` and add it to ``target.disks``.
    * open a :class:`Volume <dissect.target.volume.Volume>` and add it to ``target.volumes``.
    * open a :class:`VirtualFilesystem <dissect.target.filesystem.VirtualFilesystem>`,    add your files into it and add it to ``target.filesystems``.

    You don't need to manually parse volumes or filesystems in your loader, just add the highest level object you have
    (e.g. a :class:`Container <dissect.target.container.Container>` of a VMDK file) to the target.
    However, sometimes you need to get creative.
    Take a look at the :class:`ITunesLoader <dissect.target.loaders.itunes.ITunesLoader>` and
    :class:`TarLoader <dissect.target.loaders.tar.TarLoader>` for some creative examples.

    Args:
        path: The target path to load.
    """

    def __init__(self, path: Path, **kwargs):
        self.path = path

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.path}')"

    @staticmethod
    def detect(path: Path) -> bool:
        """Detects wether this ``Loader`` class can load this specific ``path``.

        Args:
            path: The target path to check.

        Returns:
            ``True`` if the ``path`` can be loaded by a ``Loader`` instance. ``False`` otherwise.
        """
        raise NotImplementedError()

    @staticmethod
    def find_all(path: Path) -> Iterator[Path]:
        """Finds all targets to load from ``path``.

        This can be used to open multiple targets from a target path that doesn't necessarily map to files on a disk.
        For example, a wildcard in a hostname a loader that opens targets from an API or Unix socket,
        such as the Carbon Black loader.

        Args:
            path: The location to a target to try and open multiple paths from.

        Returns:
            All the target paths found from the source path.
        """
        yield path

    def map(self, target: Target) -> None:
        """Maps the loaded path into a ``Target``.

        Args:
            target: The target that we're mapping into.
        """
        raise NotImplementedError()

def register(module_name: str, class_name: str, internal: bool=True) -> None:
    """Registers a ``Loader`` class inside ``LOADERS``.

    This function registers a loader using ``modname`` relative to the ``MODULE_PATH``.
    It lazily imports the module, and retrieves the specific class from it.

    Args:
        module: The module where to find the loader.
        class_name: The class to load.
        internal: Whether it is an internal module or not.
    """
    if internal:
        module = '.'.join([MODULE_PATH, module_name])
    else:
        module = module_name
    loader = getattr(import_lazy(module), class_name)
    LOADERS.append(loader)
    LOADERS_BY_SCHEME[module_name] = loader

def find_loader(item: Path, parsed_path: Optional[urllib.parse.ParseResult]=None) -> Optional[Loader]:
    """Finds a :class:`Loader` class for the specific ``item``.

    This searches for a specific :class:`Loader` classs that is able to load a target pointed to by ``item``.
    Once it detects a suitable :class:`Loader` it immediately returns said :class:`Loader` class.
    It does this for all items inside the ``LOADER`` variable.

    The :class:`DirLoader <dissect.target.loaders.dir.DirLoader>` is used as the last entry
    due to how the detection methods function.

    Args:
        item: The target path to load.

    Returns:
        A :class:`Loader` class for the specific target if one exists.
    """
    if parsed_path:
        if (loader := LOADERS_BY_SCHEME.get(parsed_path.scheme)):
            return loader
    for loader in LOADERS + [DirLoader]:
        try:
            if loader.detect(item):
                return loader
        except ImportError as exception:
            log.warning('Failed to import %s', loader)
            log.debug('', exc_info=exception)

def open(item: Union[str, Path], *args, **kwargs):
    """Opens a :class:`Loader` for a specific ``item``.

    This instantiates a :class:`Loader` for a specific ``item``.
    The :class:`DirLoader <dissect.target.loaders.dir.DirLoader>` is used as the last entry
    due to how the detection methods function.

    Args:
        item: The target path to load.

    Returns:
        A :class:`Loader` class for the specific target if one exists.
    """
    item, parsed_path = extract_path_info(item)
    if (loader := find_loader(item, parsed_path=parsed_path)):
        kwargs['parsed_path'] = parsed_path
        return loader(item, *args, **kwargs)
register('local', 'LocalLoader')
register('remote', 'RemoteLoader')
register('asdf', 'AsdfLoader')
register('tar', 'TarLoader')
register('vmx', 'VmxLoader')
register('vmcx', 'VmcxLoader')
register('ovf', 'OvfLoader')
register('vbox', 'VBoxLoader')
register('ewf', 'EwfLoader')
register('vb', 'VBLoader')
register('xva', 'XvaLoader')
register('vma', 'VmaLoader')
register('kape', 'KapeLoader')
register('tanium', 'TaniumLoader')
register('itunes', 'ITunesLoader')
register('target', 'TargetLoader')
register('phobos', 'PhobosLoader')