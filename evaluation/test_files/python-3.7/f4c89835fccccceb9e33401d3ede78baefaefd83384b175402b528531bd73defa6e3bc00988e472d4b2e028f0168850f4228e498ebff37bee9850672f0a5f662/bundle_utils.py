import hashlib
import logging
from pathlib import Path
import shutil
import toml
log = logging.getLogger('scan')
archivedir = Path('archivedPDFs')

def make_base_directories():
    """Make various directories that bundle uploading will need.

    TODO: not needed?  bundle and archive codes make their own
    """
    archivedir.mkdir(exist_ok=True)
    Path('bundles').mkdir(exist_ok=True)

def make_bundle_dir(bundledir):
    """Make various subdirectories that processing/uploading will need.

    args:
        bundledir (pathlib.Path): the path to the bundle, either relative
            to the CWD or a full path.
    """
    for d in ('pageImages', 'scanPNGs', 'decodedPages', 'unknownPages', 'uploads/sentPages', 'uploads/discardedPages', 'uploads/collidingPages', 'uploads/sentPages/unknowns', 'uploads/sentPages/collisions'):
        (bundledir / d).mkdir(parents=True, exist_ok=True)

def get_bundle_dir(bundle_name, *, basedir=Path('.')):
    """Make a filesystem for processing/uploading a bundle.

    args:
        bundle_name (str): the name of the bundle (not a path).

    kwargs:
        basedir (pathlib.Path): default's to the current working
            directory.

    The bundle directory `bundle_dir` will be basedir / bundles / bundle_name.

    returns:
        pathlib.Path: `bundle_dir`, the bundle directory, something
            like `<basedir>/bundles/<bundle_name>`.
    """
    bundle_dir = basedir / 'bundles' / bundle_name
    make_bundle_dir(bundle_dir)
    return bundle_dir

def bundle_name_from_file(filename):
    """Return the bundle name for a file.

    Args:
        filename (str/pathlib.Path): name of file, typically a PDF file.

    Returns
        str: Currently bundle name is the file name (including extension) with
            some input sanitizing such as spaces replaced with underscores.
    """
    filename = Path(filename)
    return filename.name.replace(' ', '_')

def bundle_name_and_md5_from_file(filename):
    """Return the bundle name and md5sum checksum for a file.

    Args:
        filename (str/Path): name of file.

    Returns
        tuple: (str, str) for bundle_name and md5sum.

    Exceptions:
        FileNotFoundError: file does not exist.
    """
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError('not found or not a file/symlink')
    bundle_name = bundle_name_from_file(filename)
    with open(filename, 'rb') as fh:
        md5 = hashlib.md5(fh.read()).hexdigest()
    return (bundle_name, md5)

def _archiveBundle(filename, *, basedir=Path('.'), subdir=Path('.')):
    """Archive the bundle pdf.

    The bundle.pdf is moved into the archive directory, or a subdir
    The archive.toml file is updated with the file name and md5sum.
    """
    with open(filename, 'rb') as fh:
        md5 = hashlib.md5(fh.read()).hexdigest()
    (basedir / archivedir).mkdir(exist_ok=True)
    (basedir / archivedir / subdir).mkdir(exist_ok=True)
    move_to = subdir / Path(filename).name
    shutil.move(filename, basedir / archivedir / move_to)
    try:
        arch = toml.load(basedir / archivedir / 'archive.toml')
    except FileNotFoundError:
        arch = {}
    arch[md5] = str(move_to)
    with open(basedir / archivedir / 'archive.toml', 'w') as fh:
        toml.dump(arch, fh)

def archiveHWBundle(file_name, *, basedir=Path('.')):
    """Archive a hw-pages bundle pdf"""
    log.debug(f'Archiving homework bundle {file_name}')
    _archiveBundle(file_name, basedir=basedir, subdir=Path('HW'))

def archiveTBundle(file_name):
    """Archive a test-pages bundle pdf"""
    log.debug(f'Archiving test-page bundle {file_name}')
    _archiveBundle(file_name)