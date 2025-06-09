"""The pathlib_fix module contains several pathlib fixes."""
from pathlib import Path

def path_resolve(path: Path) -> Path:
    """
    Fix/Workaround for bug https://bugs.python.org/issue38671.

    On Windows resolve will not return correct absolute paths for non-existing files
    (only for existing ones). This got fixed in python 3.10, however as we need to
    support older versions....
    """
    if path.is_absolute():
        return path
    maybe_absolute = path.resolve()
    if maybe_absolute.is_absolute():
        return maybe_absolute
    return Path().resolve() / maybe_absolute

def path_is_relative_to(path: Path, base: Path) -> bool:
    """
    Fix/Workaround for strange behavior in python 3.8.

    The issue is that Path.is_relative_to complains about PosixPath not having such an attribute in a
    foreign project.
    """
    absolute_base = path_resolve(base)
    absolute_path = path_resolve(path)
    return str(absolute_base) in str(absolute_path)