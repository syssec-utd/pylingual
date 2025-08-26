#!/usr/bin/env python3

import subprocess
import sys
import py_compile
import platform
import os
import shutil

from pylingual.utils.version import PythonVersion


UV_VERSIONS = {PythonVersion((3, x)) for x in range(8, 14)}


class CompileError(Exception):
    success = False
    bc_a = None


class PyenvError(Exception):
    pass


def _compile_native(py_file: str, out_file: str):
    try:
        py_compile.compile(py_file, cfile=out_file, doraise=True, optimize=0)
    except py_compile.PyCompileError as e:
        raise CompileError(str(e))
    return


def _compile_uv(py_file: str, out_file: str, version: PythonVersion):
    compile_cmd = f"import py_compile, sys; assert sys.version_info[:2] == {version.as_tuple()!r}; py_compile.compile({py_file!r}, cfile={out_file!r})"

    cmd = ["uvx", "--python", version.as_str(), "python", "-c", compile_cmd]

    output = subprocess.run(cmd, shell=False, capture_output=True, text=True, env={**os.environ, "PYTHONWARNINGS": "ignore"})

    if output.stderr:
        raise CompileError(output.stderr)


def _compile_pyenv(py_file: str, out_file: str, version: PythonVersion):
    which_pyenv = shutil.which("pyenv")
    if not which_pyenv:
        raise PyenvError(f"Could not find pyenv installation to compile in version {version.as_str()}. Try running with --init-pyenv to enable verification for end-of-life Python versions.")

    version_win = None
    if platform.system() == "Windows":  # workaround for pyenv-win being bugged when passing versions like 3.x not 3.x.y

        def try_get_version_patch(version_str) -> int | None:
            try:
                return int(version_str.split(".", 2)[2])
            except IndexError:
                return None
            except ValueError:
                return None

        pyenv_versions_cmd = [which_pyenv, *"versions --bare".split()]
        pyenv_versions_output = subprocess.run(pyenv_versions_cmd, shell=False, capture_output=True, text=True)
        if pyenv_versions_output.stderr:
            raise CompileError(pyenv_versions_output.stderr)
        # get lastest pyenv version for the correct major.minor version
        pyenv_version_strings = list(filter(lambda x: x.startswith(f"{version.as_str()}"), pyenv_versions_output.stdout.splitlines()))
        if not any(x == version.as_str() for x in pyenv_version_strings):
            pyenv_real_versions = list(filter(lambda x: x is not None, map(try_get_version_patch, pyenv_version_strings)))
            if len(pyenv_real_versions) == 0:
                raise PyenvError(f"Could not find pyenv version for {version.as_str()}")
            version_win = f"{version.as_str()}.{max(pyenv_real_versions)}"

    compile_cmd = f"import py_compile, sys; assert sys.version_info[:2] == {version.as_tuple()!r}; py_compile.compile({py_file!r}, cfile={out_file!r})"

    cmd = [which_pyenv, *"exec python -c".split(), compile_cmd]

    output = subprocess.run(cmd, shell=False, capture_output=True, text=True, env={**os.environ, "PYENV_VERSION": version_win if version_win else version.as_str(), "PYTHONWARNINGS": "ignore"})

    if output.stderr:
        raise CompileError(output.stderr)


def compile_version(py_file, out_file, version):
    py_file = str(py_file)
    out_file = str(out_file)
    version = PythonVersion(version)

    if version == sys.version_info:
        _compile_native(py_file=py_file, out_file=out_file)
    elif version in UV_VERSIONS:
        _compile_uv(py_file=py_file, out_file=out_file, version=version)
    else:
        _compile_pyenv(py_file=py_file, out_file=out_file, version=version)
    
    


