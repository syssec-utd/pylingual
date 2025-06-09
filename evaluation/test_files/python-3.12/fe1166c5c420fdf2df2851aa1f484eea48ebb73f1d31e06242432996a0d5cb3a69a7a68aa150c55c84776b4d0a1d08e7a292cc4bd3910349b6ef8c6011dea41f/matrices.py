from pathlib import Path
import numpy as np
from scipy.io import loadmat, mmread, mmwrite, savemat
from scipy.sparse import issparse
from pymor.core.logger import getLogger

def _loadmat(path, key=None):
    try:
        data = loadmat(path, mat_dtype=True)
    except Exception as e:
        raise IOError(e) from e
    if key:
        try:
            return data[key]
        except KeyError as e:
            raise IOError(f'"{key}" not found in MATLAB file {path}') from e
    data = [v for v in data.values() if isinstance(v, np.ndarray) or issparse(v)]
    if len(data) == 0:
        raise IOError(f'No matrix data contained in MATLAB file {path}')
    elif len(data) > 1:
        raise IOError(f'More than one matrix object stored in MATLAB file {path}')
    else:
        return data[0]

def _savemat(path, matrix, key=None):
    if key is None:
        raise IOError('"key" must be specified for MATLAB file')
    try:
        savemat(path, {key: matrix})
    except Exception as e:
        raise IOError(e) from e

def _mmread(path, key=None):
    if key:
        raise IOError('Cannot specify "key" for Matrix Market file')
    try:
        matrix = mmread(path)
        if issparse(matrix):
            matrix = matrix.tocsc()
        return matrix
    except AttributeError:
        return _mmread(path=str(path), key=key)
    except Exception as e:
        raise IOError(e) from e

def _mmwrite(path, matrix, key=None):
    if key:
        raise IOError('Cannot specify "key" for Matrix Market file')
    try:
        if path.suffix != '.gz':
            open_file = open
        else:
            import gzip
            open_file = gzip.open
        with open_file(path, 'wb') as f:
            mmwrite(f, matrix)
    except AttributeError:
        return _mmwrite(path=str(path), matrix=matrix, key=key)
    except Exception as e:
        raise IOError(e) from e

def _load(path, key=None):
    try:
        data = np.load(path)
    except Exception as e:
        raise IOError(e) from e
    if isinstance(data, (dict, np.lib.npyio.NpzFile)):
        if key:
            try:
                matrix = data[key]
            except KeyError as e:
                raise IOError(f'"{key}" not found in NPY file {path}') from e
        elif len(data) == 0:
            raise IOError(f'No data contained in NPY file {path}')
        elif len(data) > 1:
            raise IOError(f'More than one object stored in NPY file {path} for key {key}')
        else:
            matrix = next(iter(data.values()))
    else:
        matrix = data
    if not isinstance(matrix, np.ndarray) and (not issparse(matrix)):
        raise IOError(f'Loaded data is not a matrix in NPY file {path}')
    return matrix

def _save(path, matrix, key=None):
    if key:
        raise IOError('Cannot specify "key" for NPY file')
    try:
        np.save(path, matrix)
    except Exception as e:
        raise IOError(e) from e

def _savez(path, matrix, key=None):
    try:
        if key is None:
            np.savez(path, matrix)
        else:
            np.savez(path, **{key: matrix})
    except Exception as e:
        raise IOError(e) from e

def _loadtxt(path, key=None):
    if key:
        raise IOError('Cannot specify "key" for TXT file')
    try:
        return np.loadtxt(path)
    except Exception as e:
        raise IOError(e) from e

def _savetxt(path, matrix, key=None):
    if key:
        raise IOError('Cannot specify "key" for TXT file')
    try:
        return np.savetxt(path, matrix)
    except Exception as e:
        raise IOError(e) from e

def _get_file_extension(path):
    suffix_count = len(path.suffixes)
    if suffix_count and len(path.suffixes[-1]) == 4:
        extension = path.suffixes[-1].lower()
    elif path.suffixes[-1].lower() == '.gz' and suffix_count >= 2 and (len(path.suffixes[-2]) == 4):
        extension = ''.join(path.suffixes[-2:]).lower()
    else:
        extension = ''
    return extension

def load_matrix(path, key=None):
    """Load matrix from file.

    Parameters
    ----------
    path
        Path to the file (`str` or `pathlib.Path`).
    key
        Key of the matrix (only for NPY, NPZ, and MATLAB files).

    Returns
    -------
    matrix
        |NumPy array| of |SciPy spmatrix|.

    Raises
    ------
    IOError
        If loading fails.
    """
    logger = getLogger('pymor.tools.io.load_matrix')
    logger.info('Loading matrix from file %s', path)
    path = Path(path)
    extension = _get_file_extension(path)
    file_format_map = {'.mat': ('MATLAB', _loadmat), '.mtx': ('Matrix Market', _mmread), '.mtz.gz': ('Matrix Market', _mmread), '.npy': ('NPY/NPZ', _load), '.npz': ('NPY/NPZ', _load), '.txt': ('Text', _loadtxt)}
    if extension in file_format_map:
        file_type, loader = file_format_map[extension]
        logger.info(file_type + ' file detected.')
        return loader(path, key)
    logger.warning('Could not detect file format. Trying all loaders ...')
    loaders = [_loadmat, _mmread, _loadtxt, _load]
    for loader in loaders:
        try:
            return loader(path, key)
        except IOError:
            pass
    raise IOError(f'Could not load file {path} (key = {key})')

def save_matrix(path, matrix, key=None):
    """Save matrix to file.

    Parameters
    ----------
    path
        Path to the file (`str` or `pathlib.Path`).
    matrix
        Matrix to save.
    key
        Key of the matrix (only for NPY, NPZ, and MATLAB files).

    Raises
    ------
    IOError
        If saving fails.
    """
    logger = getLogger('pymor.tools.io.save_matrix')
    logger.info('Saving matrix to file %s', path)
    path = Path(path)
    extension = _get_file_extension(path)
    file_format_map = {'.mat': ('MATLAB', _savemat), '.mtx': ('Matrix Market', _mmwrite), '.mtz.gz': ('Matrix Market', _mmwrite), '.npy': ('NPY', _save), '.npz': ('NPZ', _savez), '.txt': ('Text', _savetxt)}
    if extension in file_format_map:
        file_type, saver = file_format_map[extension]
        logger.info(file_type + ' file detected.')
        return saver(path, matrix, key)
    raise IOError(f'Unknown extension "{extension}"')