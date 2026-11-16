import shutil
import subprocess
import sys

import pytest

from pylingual.utils import generate_bytecode
from pylingual.utils.generate_bytecode import CompileError, compile_version
from pylingual.utils.version import PythonVersion

SOURCES = {
    "ok": "def f(x):\n    if x:\n        return 1\n    return 2\n",
    "syntax": "def f(x):\n    if x\n        return 1\n",
    "indent": "def f(x):\n    if x:\n    return 1\n",
    "orphan": "else:\n    pass\n",
    "null": "x = 1\0\n",
}


def available(version: str) -> bool:
    """A Python of `version` other than this one, which compile_version runs in this process instead."""
    v = PythonVersion(version)
    if v == sys.version_info:
        return False
    if v in generate_bytecode.UV_VERSIONS:
        return generate_bytecode._uv_python(v) is not None
    return shutil.which("pyenv") is not None and subprocess.run(["pyenv", "prefix", version], capture_output=True).returncode == 0


def compile_both(src, tmp_path, version: str, name: str):
    """(outcome through the compile server, outcome through a subprocess per file): pyc bytes or the CompileError text."""
    outcomes = []
    for served in (True, False):
        out = tmp_path / f"{name}-{served}.pyc"
        original = generate_bytecode._served
        if not served:
            generate_bytecode._served = lambda *args: None
        try:
            compile_version(src, out, version)
            outcomes.append(out.read_bytes())
        except CompileError as e:
            outcomes.append(str(e))
        finally:
            generate_bytecode._served = original
    return outcomes


@pytest.mark.parametrize("version", ["3.6", "3.7", "3.8", "3.11", "3.12", "3.13", "3.14"])
def test_compile_server_matches_a_subprocess_per_file(version, tmp_path):
    """The compile server gives the same pyc bytes and the same compile error text as one interpreter per file."""
    if not available(version):
        pytest.skip(f"no Python {version} here")
    for name, text in SOURCES.items():
        src = tmp_path / f"{name}.py"
        src.write_text(text)
        served, separate = compile_both(src, tmp_path, version, name)
        assert served == separate, name
        assert isinstance(served, bytes) == (name == "ok")


def test_compile_server_restarts_after_a_failure(tmp_path):
    """A server that dies is replaced on the next compile."""
    version = next((v for v in ("3.12", "3.13", "3.11") if available(v)), None)
    if version is None:
        pytest.skip("no uv Python here")
    src = tmp_path / "ok.py"
    src.write_text(SOURCES["ok"])
    compile_version(src, tmp_path / "a.pyc", version)
    server = next(s for key, s in generate_bytecode._servers.items() if key[0] == "uv" and key[1] == generate_bytecode._uv_python(PythonVersion(version)))
    server.process.kill()
    server.process.wait()
    compile_version(src, tmp_path / "b.pyc", version)
    assert (tmp_path / "a.pyc").read_bytes() == (tmp_path / "b.pyc").read_bytes()
