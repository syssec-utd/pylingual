import random
import sys
from pathlib import Path

import pytest

from dataset_generation.bytecode2cflow import make_examples, render_with_skeletons
from dataset_generation.normalize_source import normalize_source
from pylingual.control_flow_reconstruction.model_view import CflowRequest
from pylingual.editable_bytecode import PYCFile
from pylingual.equivalence_check import compare_pyc
from pylingual.utils.generate_bytecode import UV_VERSIONS, CompileError, PyenvError, _uv_python, compile_version
from pylingual.utils.version import PythonVersion

from test_block_grammar import random_skeleton

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ["Conditional", "Exception", "Generator", "Loop", "Match", "NestedException", "With", "Python315"]
VERSIONS = [f"3.{minor}" for minor in range(6, 16)]
HOST = PythonVersion(sys.version_info[:2])


def compiled_fixture(fixture: str, version: PythonVersion, tmp_path: Path) -> tuple[str, Path]:
    """Normalized source of a fixture and its pyc compiled with `version`, or skip."""
    if version != HOST and version in UV_VERSIONS and _uv_python(version) is None:
        pytest.skip(f"Python {version} not available")
    try:
        src = normalize_source((ROOT / "test" / f"{fixture}.py").read_text(), version=version.as_tuple(), replace_docstrings=True)
    except SyntaxError as e:
        pytest.skip(f"host ast cannot parse {fixture} for {version}: {e}")
    py, pyc_path = tmp_path / f"{fixture}.py", tmp_path / f"{fixture}.pyc"
    py.write_text(src)
    try:
        compile_version(py, pyc_path, version)
    except (CompileError, PyenvError) as e:
        pytest.skip(f"{fixture} does not compile in {version}: {e}")
    return src, pyc_path


@pytest.mark.filterwarnings("ignore::SyntaxWarning")
@pytest.mark.parametrize("version", VERSIONS)
@pytest.mark.parametrize("fixture", FIXTURES)
def test_gold_skeleton_round_trip(fixture, version, tmp_path):
    """Every code object has a gold skeleton the block grammar accepts, and they recompile to equivalent bytecode."""
    version = PythonVersion(version)
    src, pyc_path = compiled_fixture(fixture, version, tmp_path)
    pyc = PYCFile(str(pyc_path))
    examples = make_examples(pyc, src)
    assert {e["name"] for e in examples} == {bc.name for bc in pyc.iter_bytecodes() if not bc.is_comprehension and any(i.starts_line for i in bc)}
    assert all(CflowRequest.from_row(e).grammar().accepts(e["target"].split()) for e in examples)
    restored = tmp_path / "restored.py"
    restored.write_text(render_with_skeletons(pyc, src.split("\n"), examples))
    compile_version(restored, restored.with_suffix(".pyc"), version)
    failed = [str(r) for r in compare_pyc(pyc_path, restored.with_suffix(".pyc")) if not r.success]
    assert not failed, restored.read_text()


@pytest.mark.filterwarnings("ignore::SyntaxWarning")
@pytest.mark.parametrize("version", VERSIONS)
@pytest.mark.parametrize("fixture", FIXTURES)
def test_any_accepted_skeleton_compiles(fixture, version, tmp_path):
    """Random skeletons the block grammar accepts, for every code object at once, render to source that compiles."""
    version = PythonVersion(version)
    src, pyc_path = compiled_fixture(fixture, version, tmp_path)
    pyc = PYCFile(str(pyc_path))
    examples = make_examples(pyc, src)
    rng = random.Random(f"{fixture}-{version}")
    for round in range(3):
        guesses = [e | {"target": " ".join(random_skeleton(CflowRequest.from_row(e).grammar(), rng, deep=round == 2))} for e in examples]
        guessed = tmp_path / f"guess{round}.py"
        guessed.write_text(render_with_skeletons(pyc, src.split("\n"), guesses))
        try:
            compile_version(guessed, guessed.with_suffix(".pyc"), version)
        except CompileError as e:
            pytest.fail(f"{e}\n" + "\n".join(f"{g['name']}: {g['target']}" for g in guesses))


@pytest.mark.parametrize("version", ["3.11", "3.12", "3.13", "3.14"])
def test_except_star_gold_round_trip(version, tmp_path):
    """try/except*/else/finally functions produce valid gold skeletons and round-trip to equivalent bytecode."""
    version = PythonVersion(version)
    if version != HOST and version in UV_VERSIONS and _uv_python(version) is None:
        pytest.skip(f"Python {version} not available")
    src = (
        "def f(a):\n"
        "    try:\n"
        "        g(a)\n"
        "    except* ValueError as e:\n"
        "        h(e)\n"
        "    except*(TypeError, KeyError) as e:\n"
        "        k(e)\n"
        "    else:\n"
        "        ok()\n"
        "    finally:\n"
        "        done()\n"
    )
    py, pyc_path = tmp_path / "exstar.py", tmp_path / "exstar.pyc"
    py.write_text(src)
    compile_version(py, pyc_path, version)
    pyc = PYCFile(str(pyc_path))
    examples = make_examples(pyc, src)
    assert "<module>.f" in {e["name"] for e in examples}
    assert all(CflowRequest.from_row(e).grammar().accepts(e["target"].split()) for e in examples)
    restored = tmp_path / "restored.py"
    restored.write_text(render_with_skeletons(pyc, src.split("\n"), examples))
    compile_version(restored, restored.with_suffix(".pyc"), version)
    failed = [str(r) for r in compare_pyc(pyc_path, restored.with_suffix(".pyc")) if not r.success]
    assert not failed, restored.read_text()


@pytest.mark.parametrize("version", ["3.6", "3.7", "3.8", "3.12"])
def test_non_jumping_while_gold_round_trip(version, tmp_path):
    """A while loop whose body always returns round-trips on both <=3.7 (SETUP_LOOP) and 3.8+ (equivalent to if)."""
    version = PythonVersion(version)
    if version != HOST and version in UV_VERSIONS and _uv_python(version) is None:
        pytest.skip(f"Python {version} not available")
    src = "def f(x):\n    while x:\n        return 1\n    return 0\n"
    py, pyc_path = tmp_path / "wret.py", tmp_path / "wret.pyc"
    py.write_text(src)
    try:
        compile_version(py, pyc_path, version)
    except PyenvError as e:
        pytest.skip(str(e))
    pyc = PYCFile(str(pyc_path))
    examples = make_examples(pyc, src)
    f_row = next((e for e in examples if e["name"] == "<module>.f"), None)
    assert f_row is not None
    assert CflowRequest.from_row(f_row).grammar().accepts(f_row["target"].split())
    if version <= (3, 7):
        assert 0 in f_row["loops"] and f_row["target"].startswith("loop ")
    restored = tmp_path / "restored.py"
    restored.write_text(render_with_skeletons(pyc, src.split("\n"), examples))
    compile_version(restored, restored.with_suffix(".pyc"), version)
    failed = [str(r) for r in compare_pyc(pyc_path, restored.with_suffix(".pyc")) if not r.success]
    assert not failed, restored.read_text()
