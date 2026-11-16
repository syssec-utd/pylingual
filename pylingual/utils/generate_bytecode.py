#!/usr/bin/env python3

import functools
import json
import subprocess
import sys
import py_compile
import platform
import os
import re
import shutil


from pylingual.utils.version import PythonVersion


UV_VERSIONS = {PythonVersion((3, x)) for x in range(8, 16)}


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


@functools.lru_cache(maxsize=None)
def _uv_python(version: PythonVersion) -> str | None:
    """Resolve the interpreter uvx would use, so repeated compiles can skip uvx's per-call resolution."""
    try:
        found = subprocess.run(["uv", "python", "find", version.as_str()], shell=False, capture_output=True, text=True)
        path = found.stdout.strip()
        if found.returncode != 0 or not path:
            return None
        # confirm the version before trusting it, otherwise a bad resolve turns every compile into a CompileError
        check = subprocess.run([path, "-c", "import sys; print('%d.%d' % sys.version_info[:2])"], shell=False, capture_output=True, text=True)
        return path if check.stdout.strip() == version.as_str() else None
    except Exception:
        return None


# Compiles files sent on stdin, one JSON [source, out] per line, and answers each with the JSON of what py_compile wrote
# to stderr: the same as the stderr of a `python -c "py_compile.compile(...)"` run (py_compile reports every compile
# failure there itself), without starting an interpreter for each file. Runs on every supported version (3.6+).
_SERVER = """
import contextlib, io, json, py_compile, sys
assert sys.version_info[:2] == {version!r}
for line in sys.stdin:
    py_file, out_file = json.loads(line)
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        py_compile.compile(py_file, cfile=out_file)
    sys.stdout.write(json.dumps(err.getvalue()) + "\\n")
    sys.stdout.flush()
"""


class _CompileServer:
    """One long-lived interpreter that compiles files for this process; restarted after any failure."""

    def __init__(self, cmd: list[str], env: dict):
        self.cmd, self.env = cmd, env
        self.process = None
        self.pid = None

    def compile(self, py_file: str, out_file: str) -> str | None:
        """py_compile's stderr for the file, or None when the server cannot answer (the caller compiles another way)."""
        if self.process is None or self.process.poll() is not None or self.pid != os.getpid():
            # a forked child must not share its parent's pipes
            self.process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", env=self.env)
            self.pid = os.getpid()
        try:
            self.process.stdin.write(json.dumps([py_file, out_file]) + "\n")
            self.process.stdin.flush()
            reply = self.process.stdout.readline()
            if not reply:
                raise EOFError("compile server exited")
            return json.loads(reply)
        except BaseException:
            # a request cut off (a timeout alarm, a crash) leaves the protocol out of step: start again next time
            self.close()
            raise

    def close(self):
        if self.process is not None:
            self.process.kill()
            self.process.wait()
        self.process = None


_servers: dict[tuple, _CompileServer] = {}


def _served(key: tuple, cmd_prefix: list[str], env: dict, version: PythonVersion, py_file: str, out_file: str) -> str | None:
    """Compile through the server for `key`; None if it is unavailable, so the caller compiles the file itself."""
    server = _servers.get(key)
    if server is None:
        server = _servers[key] = _CompileServer([*cmd_prefix, "-c", _SERVER.format(version=version.as_tuple())], env)
    try:
        return server.compile(py_file, out_file)
    except TimeoutError:  # an OSError, but a deadline: it must reach the caller
        raise
    except (OSError, EOFError, ValueError):
        return None


def _compile_uv(py_file: str, out_file: str, version: PythonVersion):
    compile_cmd = f"import py_compile, sys; assert sys.version_info[:2] == {version.as_tuple()!r}; py_compile.compile({py_file!r}, cfile={out_file!r})"

    python = _uv_python(version)
    env = {**os.environ, "PYTHONWARNINGS": "ignore"}
    if python:
        stderr = _served(("uv", python), [python], env, version, py_file, out_file)
        if stderr is not None:
            if stderr:
                raise CompileError(stderr)
            return
    cmd = [python, "-c", compile_cmd] if python else ["uvx", "--no-config", "--python", version.as_str(), "python", "-c", compile_cmd]

    output = subprocess.run(cmd, shell=False, capture_output=True, text=True, env=env)

    # Ignore stderr messages from uv downloading versions on demand
    stderr = re.sub(r"\s*Download(ing|ed)\s.+\n", "", output.stderr)
    # Ignore stderr messages from uv logging that compilation occurred
    stderr = re.sub(r"\s*Bytecode compiled \d+ files? in \d+ms\n", "", stderr)
    if stderr:
        raise CompileError(stderr)


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

    env = {**os.environ, "PYENV_VERSION": version_win if version_win else version.as_str(), "PYTHONWARNINGS": "ignore"}
    stderr = _served(("pyenv", env["PYENV_VERSION"]), [which_pyenv, "exec", "python"], env, version, py_file, out_file)
    if stderr is not None:
        if stderr:
            raise CompileError(stderr)
        return

    cmd = [which_pyenv, *"exec python -c".split(), compile_cmd]

    output = subprocess.run(cmd, shell=False, capture_output=True, text=True, env=env)

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
