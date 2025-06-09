from importlib_metadata import version
try:
    __version__ = version('servicefoundry')
except Exception:
    __version__ = 'NA'