"""Versioning."""
__all__ = ('__version__',)
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata
try:
    __version__ = importlib_metadata.version('py-check-updates')
except importlib_metadata.PackageNotFoundError:
    __version__ = None