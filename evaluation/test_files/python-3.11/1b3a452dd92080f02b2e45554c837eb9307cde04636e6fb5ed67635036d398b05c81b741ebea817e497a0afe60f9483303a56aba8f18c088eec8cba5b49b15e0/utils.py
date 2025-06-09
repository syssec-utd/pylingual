from os import getpid
from pathlib import Path
from select import select
from sys import stdin
from psutil import Process
from . import DATA_DIRS

def find_data(subdir, filename):
    """
    Search through all the data directories for the filename.
    Return the absolute path if found. Precedence is:
    1) absolute path provided
    2) STARFIT_DATA env var (set in __init__.py)
    3) Installation DATA_DIR (set in __init__.py)
    """
    if subdir is None:
        return filename
    if not isinstance(subdir, (str, Path)):
        raise ValueError(f'invalid subdir={subdir!r}')
    if isinstance(filename, (list, tuple)) and len(filename) == 1:
        filename = filename[0]
    try:
        fullpath = Path(filename).expanduser().resolve()
        if fullpath.is_file():
            return fullpath
    except:
        pass
    for data_dir in DATA_DIRS:
        try:
            fullpath = (Path(data_dir) / subdir / filename).expanduser().resolve()
            if fullpath.is_file():
                return fullpath
        except:
            pass
    raise IOError(f'file {filename} not found')

def find_all(subdir, pattern, complete=False):
    """
    Search through all the data directories for the filename.
    Return the absolute path of all files
    - in the first directory one is found if complete is False
    - in all subdirectories if complete is True
    Search precedence is:
    1) absolute path if provided
    2) STARFIT_DATA env var (set in __init__.py)
    3) Installation DATA_DIR (set in __init__.py)
    """
    if subdir is None:
        fullpath = Path(pattern)
        filenames = list(fullpath.parent.glob(fullpath.name))
        files = list()
        for file in filenames:
            file = Path(file)
            try:
                if file.is_file():
                    files.append(file)
            except:
                pass
        return files
    if not isinstance(subdir, (str, Path)):
        raise ValueError(f'invalid subdir={subdir!r}')
    files = list()
    try:
        fullpath = Path(pattern).expanduser().resolve()
        filenames = list(fullpath.parent.glob(fullpath.name))
        for file in filenames:
            file = Path(file)
            try:
                if file.is_file():
                    files.append(file)
            except:
                raise ()
                pass
        if len(files) > 0 and (not complete):
            return files
    except:
        pass
    for data_dir in DATA_DIRS:
        try:
            fullpath = (Path(data_dir) / subdir / pattern).expanduser().resolve()
            filenames = list(fullpath.parent.glob(fullpath.name))
            for file in filenames:
                file = Path(file)
                try:
                    if file.is_file():
                        files.append(file)
                except:
                    pass
        except:
            pass
        if len(files) > 0 and (not complete):
            return files
    if len(files) > 0:
        return files
    raise IOError(f'pattern {pattern} not found')

def set_priority(value: int):
    p = Process(getpid())
    p.nice(value)

def getch():
    try:
        i, o, e = select([stdin], [], [], 0)
        if i:
            ch = stdin.read(1)
        else:
            ch = ''
    except:
        ch = ''
    return ch