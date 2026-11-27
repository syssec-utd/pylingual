import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from dataset_generation.bytecode2cflow import assign_lines
from pylingual.control_flow_reconstruction.block_grammar import BlockGrammar, shape_of
from pylingual.control_flow_reconstruction.model_view import CflowRequest, Statement, cflow_request, encode_code_object, line_kind, split_statements
from pylingual.control_flow_reconstruction.source import SourceContext
from pylingual.control_flow_reconstruction.skeleton_template import SkeletonTemplate, parse_skeleton
from pylingual.editable_bytecode import PYCFile
from pylingual.utils.generate_bytecode import _uv_python, compile_version
from pylingual.utils.version import PythonVersion

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = Path(__file__).parent / "data" / "cflow_golden.json"
FIXTURES = ["Conditional", "Exception", "Generator", "Loop", "Match", "With"]


def compile_marked(src: Path, tmp_path: Path, version: PythonVersion) -> tuple[PYCFile, list[str]]:
    """Compiled `src` with line starts marked as the segmentation model would give them."""
    pyc_path = tmp_path / f"{src.stem}.pyc"
    compile_version(src, pyc_path, version)
    pyc = PYCFile(str(pyc_path))
    lines = src.read_text().split("\n")
    assign_lines(pyc, lines)
    return pyc, lines


def encode_fixture(name: str, tmp_path: Path) -> list[dict]:
    pyc, lines = compile_marked(ROOT / "test" / f"{name}.py", tmp_path, PythonVersion("3.12"))
    out = []
    for bc in pyc.iter_bytecodes():
        if not bc.is_comprehension:
            stmts, tokens = encode_code_object(bc, lines)
            out.append({"name": bc.name, "n_stmts": len(stmts), "tokens": " ".join(tokens)})
    return out


def test_golden_encoding(tmp_path):
    if _uv_python(PythonVersion("3.12")) is None and sys.version_info[:2] != (3, 12):
        pytest.skip("Python 3.12 not available")
    golden = json.loads(GOLDEN.read_text())
    assert {name: encode_fixture(name, tmp_path) for name in FIXTURES} == golden


def test_rerender_after_update_lines(tmp_path):
    src = tmp_path / "f.py"
    src.write_text("def f(a):\n    if a:\n        print(1)\n    else:\n        print(2)\n    print(3)\n")
    pyc, lines = compile_marked(src, tmp_path, PythonVersion(sys.version_info[:2]))
    cfts = {bc.codeobj: SkeletonTemplate.for_request(bc, cflow_request(bc, lines)) for bc in pyc.iter_bytecodes()}
    f = next(bc for bc in pyc.iter_bytecodes() if bc.codeobj.co_name == "f")
    stmts = split_statements(f)
    assert len(stmts) == 4
    cfts[f.codeobj] = SkeletonTemplate(f, stmts, "<s0> { <s1> } else { <s2> } <s3>".split())
    ctx = SourceContext(pyc, lines, cfts)
    assert "    else:\n        print(2)" in str(ctx)
    snapshot = ctx.snapshot()
    ctx.update_lines([x.replace("print(2)", "print(5)") for x in lines])
    assert "    else:\n        print(5)" in str(ctx)
    skeleton = ctx.cfts[f.codeobj]
    ctx.update_cft(f, SkeletonTemplate.for_request(f, cflow_request(f, lines)))
    ctx.restore(snapshot)
    assert ctx.cfts[f.codeobj] is skeleton and "    else:\n        print(2)" in str(ctx)


def test_skeleton_headers(tmp_path):
    """A skeleton's code object keeps the lines the bytecode holds no statement for: its docstring and declarations."""
    src = tmp_path / "h.py"
    src.write_text('def f():\n    """doc"""\n    global g\n    g = 1\n')
    pyc, lines = compile_marked(src, tmp_path, PythonVersion(sys.version_info[:2]))
    cfts = {bc.codeobj: SkeletonTemplate.for_request(bc, cflow_request(bc, lines)) for bc in pyc.iter_bytecodes()}
    text = str(SourceContext(pyc, lines, cfts))
    assert '"""doc"""' in text and "global g" in text


def test_while_true_needs_a_loop(tmp_path):
    """A `while True:` line on code no loop jumps back to (as a docstring's NOP is often translated) is a plain statement."""
    if _uv_python(PythonVersion("3.12")) is None and sys.version_info[:2] != (3, 12):
        pytest.skip("Python 3.12 not available")
    src = tmp_path / "w.py"
    src.write_text('class C:\n    """doc"""\n    """more doc"""\n    x = 1\n    def f(self):\n        pass\n\ndef g(q):\n    while True:\n        if q.get():\n            break\n')
    pyc, lines = compile_marked(src, tmp_path, PythonVersion("3.12"))
    shapes = {}
    for bc in pyc.iter_bytecodes():
        stmts, _ = encode_code_object(bc, lines)
        mistranslated = [x if x.strip() != '"""more doc"""' else "    while True:" for x in lines]  # the NOP of the second string
        shapes[bc.codeobj.co_name] = [str(s) for s in cflow_request(bc, mistranslated).shapes] if stmts else []
    assert "while" not in shapes["C"]
    assert "while" in shapes["g"]


def test_while_needs_a_jump_back(tmp_path):
    """A condition heads a while loop only if a loop jumps back to it or its first statement."""
    if _uv_python(PythonVersion("3.12")) is None and sys.version_info[:2] != (3, 12):
        pytest.skip("Python 3.12 not available")
    src = tmp_path / "c.py"
    src.write_text("def f(a, b):\n    if a:\n        b()\n    while b:\n        a()\n    return a\n")
    pyc, lines = compile_marked(src, tmp_path, PythonVersion("3.12"))
    f = next(bc for bc in pyc.iter_bytecodes() if bc.codeobj.co_name == "f")
    request = cflow_request(f, lines)
    assert [str(s) for s in request.shapes] == ["cond", "stmt", "cond", "stmt", "stmt+return"]
    grammar = request.grammar()
    assert grammar.accepts("<s0> { <s1> } loop <s2> { <s3> } <s4>".split())
    assert not grammar.accepts("loop <s0> { <s1> } loop <s2> { <s3> } <s4>".split())  # nothing jumps back to the if
    # row() / from_row() preserve loops; rows without "loops" stay backward-compatible (loops=None)
    row = request.row()
    assert row["loops"] == sorted(request.loops) and 2 in row["loops"] and 0 not in row["loops"]
    restored = CflowRequest.from_row(row)
    assert restored.loops == request.loops
    assert not restored.grammar().accepts("loop <s0> { <s1> } loop <s2> { <s3> } <s4>".split())
    row.pop("loops")
    assert CflowRequest.from_row(row).loops is None


def test_loop_ok_for_inline_break(tmp_path):
    """Inline `if b: break` in a non-back-edge loop still marks the while header loop-eligible."""
    if _uv_python(PythonVersion("3.12")) is None and sys.version_info[:2] != (3, 12):
        pytest.skip("Python 3.12 not available")
    src = tmp_path / "b.py"
    src.write_text("def f(a, b):\n    while a:\n        if b: break\n        return 1\n    return 0\n")
    pyc, lines = compile_marked(src, tmp_path, PythonVersion("3.12"))
    f = next(bc for bc in pyc.iter_bytecodes() if bc.codeobj.co_name == "f")
    req = cflow_request(f, lines)
    assert 0 in req.loops and req.grammar().accepts("loop <s0> { <s1> <s2> } <s3>".split())


def test_except_star_renders_without_orphan():
    class Inst:
        opname = "NOP"

        def __init__(self, line):
            self.starts_line = line

    co = compile("def f(): pass", "<test>", "exec").co_consts[0]
    bc = SimpleNamespace(codeobj=co, globals=[], nonlocals=[], parent=None)
    texts = ["try:", "g()", "except*(ValueError, TypeError) as e:", "h(e)"]
    stmts = [Statement(i, [Inst(i + 1)], kind=line_kind(t), text=t) for i, t in enumerate(texts)]
    shapes = [shape_of(s.kind, s.text) for s in stmts]
    assert [str(s) for s in shapes] == ["try", "stmt", "except*", "stmt"]
    skeleton = "<s0> { <s1> } <s2> { <s3> }".split()
    assert BlockGrammar(shapes, "3.12").accepts(skeleton)
    pyc = SimpleNamespace(codeobj=co, version=(3, 12), iter_bytecodes=lambda: iter([bc]))
    assert str(SourceContext(pyc, texts, {co: SkeletonTemplate(bc, stmts, skeleton)})).strip() == "try:\n    g()\nexcept*(ValueError, TypeError) as e:\n    h(e)"


def test_parse_skeleton_tolerates_bad_tokens():
    tree = parse_skeleton("<s0> { <s1> <s1> <s9> } } else { <s2> loop".split(), 3)
    assert [n.sid for n in tree] == [0, None]
    assert [n.sid for n in tree[0].children] == [1]
    assert tree[1].keyword == "else"
    assert [n.sid for n in tree[1].children] == [2]


@pytest.mark.parametrize(
    "texts, skeleton, expected",
    [
        (["try:", "x = 1", "except E: x = 2"], "<s0> { <s1> } <s2>", "try:\n    x = 1\nexcept E: x = 2"),
        (["try:", "x = 1", "finally: x = 2"], "<s0> { <s1> } <s2>", "try:\n    x = 1\nfinally: x = 2"),
        (["if x: y()", "z()"], "<s0> else { <s1> }", "if x: y()\nelse:\n    z()"),
        (["if x: y()", "elif z: q()"], "<s0> <s1>", "if x: y()\nelif z: q()"),
    ],
)
def test_inline_headers_take_clauses(texts, skeleton, expected):
    """A header with its body on the same line (`if x: y()`) is a whole block: the clauses after it attach to it."""

    class Inst:
        opname = "NOP"

        def __init__(self, line):
            self.starts_line = line

    co = compile("def f(): pass", "<test>", "exec").co_consts[0]
    bc = SimpleNamespace(codeobj=co, globals=[], nonlocals=[], parent=None)
    stmts = [Statement(i, [Inst(i + 1)], kind=line_kind(t), text=t) for i, t in enumerate(texts)]
    assert BlockGrammar([shape_of(s.kind, s.text) for s in stmts], "3.12").accepts(skeleton.split())
    pyc = SimpleNamespace(codeobj=co, version=(3, 12), iter_bytecodes=lambda: iter([bc]))
    assert str(SourceContext(pyc, texts, {co: SkeletonTemplate(bc, stmts, skeleton.split())})).strip() == expected
