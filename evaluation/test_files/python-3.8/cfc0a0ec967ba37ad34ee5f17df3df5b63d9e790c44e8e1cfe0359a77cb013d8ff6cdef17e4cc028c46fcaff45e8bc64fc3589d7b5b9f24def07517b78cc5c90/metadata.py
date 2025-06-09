"""
Save project version number.

https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
"""
import sys
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata
__version__ = metadata.version('doti')
__project__ = 'doti'
__config_file__ = __project__ + '.cfg'