from pathlib import Path
import sys, os
from aerosandbox.tools.python.io import convert_ipynb_to_py

def run_python_file(path: Path) -> None:
    """
    Executes a Python file from a path.
    Args:
        path: File path

    Returns: None

    """
    sys.path.append(str(path.parent))
    __import__(path.with_suffix('').name)

def run_all_python_files(path: Path, recursive=True, verbose=True) -> None:
    """
    Executes all Python files and Jupyter Notebooks in a directory.
    Args:
        path: A Path-type object (Path from built-in pathlib) representing a filepath
        recursive: Executes recursively (e.g. searches all subfolders too)

    Returns: None

    """
    if path == Path(os.path.abspath(__file__)):
        return
    if 'ignore' in str(path).lower():
        return
    if path.is_file():
        if path.suffix == '.py':
            if verbose:
                print(f'##### Running file: {path}')
            run_python_file(path)
        if path.suffix == '.ipynb':
            if verbose:
                print(f'##### Converting file: {path}')
            notebook = path
            python_file = path.with_suffix('.py')
            convert_ipynb_to_py(notebook, python_file)
            run_all_python_files(python_file, recursive=False, verbose=verbose)
    elif path.is_dir() and recursive:
        if verbose:
            print(f'##### Opening directory: {path}')
        for subpath in path.iterdir():
            run_all_python_files(subpath, recursive=recursive, verbose=verbose)