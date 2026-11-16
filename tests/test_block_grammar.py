import random
import sys

import pytest

from pylingual.control_flow_reconstruction.block_grammar import END, MAX_BLOCKS, BlockGrammar, Shape, consistent, shape_of
from pylingual.control_flow_reconstruction.model_view import line_kind
from pylingual.control_flow_reconstruction.skeleton import CLOSE, KEYWORD_TEXT, LOOP, OPEN, parse_ref, ref
from pylingual.utils.generate_bytecode import UV_VERSIONS, CompileError, PyenvError, _uv_python, compile_version
from pylingual.utils.version import PythonVersion

VERSIONS = [f"3.{minor}" for minor in range(6, 16)]
HOST = PythonVersion(sys.version_info[:2])

# (kind, translated line) of statements to build code objects from, with the version they need
PALETTE = [
    ("K_stmt", "x = 1", "3.6"),
    ("K_stmt", "f(x)", "3.6"),
    ("K_cond", "if x:", "3.6"),
    ("K_cond", "elif x:", "3.6"),
    ("K_cond", "while x:", "3.6"),
    ("K_while_true", "while True:", "3.6"),
    ("K_for", "for x in y:", "3.6"),
    ("K_with", "with x as y:", "3.6"),
    ("K_try", "try:", "3.6"),
    ("K_except", "except E:", "3.6"),
    ("K_except", "except E as e:", "3.6"),
    ("K_except", "except:", "3.6"),
    ("K_except", "except* E:", "3.11"),
    ("K_else", "else:", "3.6"),
    ("K_finally", "finally:", "3.6"),
    ("K_break", "break", "3.6"),
    ("K_continue", "continue", "3.6"),
    ("K_return", "return x", "3.6"),
    ("K_stmt", "if x: break", "3.6"),
    ("K_stmt", "if x: return", "3.6"),
    ("K_stmt", "for x in y: continue", "3.6"),
    ("K_stmt", "while x: x = 1", "3.6"),
    ("K_stmt", "try: x = 1", "3.6"),
    ("K_stmt", "except E: pass", "3.6"),
    ("K_stmt", "else: x = 1", "3.6"),
    ("K_stmt", "finally: pass", "3.6"),
    ("K_deco", "@d", "3.6"),
    ("K_def", "def f(): pass", "3.6"),
    ("K_def", "class C: pass", "3.6"),
    ("K_match", "match x:", "3.10"),
    ("K_case", "case 1:", "3.10"),
    ("K_case", "case 1 if x:", "3.10"),
    ("K_case", "case _:", "3.10"),
    ("K_case", "case y:", "3.10"),
    ("K_stmt", "case 2: x = 1", "3.10"),
]
OPENING = {OPEN, LOOP, "else", "try", "finally", "except", "while_true", "case_"}


def random_code_object(rng: random.Random, version: PythonVersion) -> tuple[list[str], list[Shape]]:
    palette = [(k, t) for k, t, v in PALETTE if version >= PythonVersion(v)]
    while True:
        picked = [rng.choice(palette) for _ in range(rng.randint(1, 10))]
        shapes = [shape_of(k, t) for k, t in picked]
        if consistent(shapes):
            return [t for _, t in picked], shapes


def random_skeleton(grammar: BlockGrammar, rng: random.Random, deep: bool) -> list[str]:
    """A random walk through the grammar, finished by `complete`. `deep` prefers tokens that open blocks."""
    state, out = grammar.start(), []
    for _ in range(rng.randint(0, 80 if deep else 30)):
        stmts, tokens = grammar.allowed(state)
        options = [ref(i) for i in range(grammar.n) if stmts >> i & 1] + [t for t in tokens if t != END]
        if not options:
            break
        weights = [8 if deep and (t in OPENING or (parse_ref(t) is not None and grammar.shapes[parse_ref(t)].opener and not grammar.shapes[parse_ref(t)].inline)) else 1 for t in options]
        token = rng.choices(options, weights)[0]
        out.append(token)
        state = grammar.step(state, token)
    out += grammar.complete(state)
    assert grammar.check(out) is None, (out, grammar.check(out))
    return out


def render(texts: list[str], shapes: list[Shape], tokens: list[str], depth: int) -> list[str]:
    """Source lines of a skeleton, written like skeleton_template.py does (but without elif)."""
    lines, loop = [], False
    for token in tokens:
        if token in (LOOP, OPEN, CLOSE):
            loop, depth = token == LOOP, depth + {OPEN: 1, CLOSE: -1}.get(token, 0)
            continue
        i = parse_ref(token)
        text = KEYWORD_TEXT[token] if i is None else texts[i]
        if i is not None and shapes[i].opener == "cond":
            text = ("while " if loop else "if ") + text.split(" ", 1)[1]
        lines.append("    " * depth + text)
        loop = False
    padded = []  # SourceContext writes pass in empty blocks
    for line, after in zip(lines, [*lines[1:], ""]):
        padded.append(line)
        if line.endswith(":") and len(after) - len(after.lstrip()) <= len(line) - len(line.lstrip()):
            padded.append(" " * (len(line) - len(line.lstrip()) + 4) + "pass")
    return padded


def compile_or_skip(path, version: PythonVersion):
    if version != HOST and version in UV_VERSIONS and _uv_python(version) is None:
        pytest.skip(f"Python {version} not available")
    try:
        compile_version(path, path.with_suffix(".pyc"), version)
    except PyenvError as e:
        pytest.skip(str(e))


@pytest.mark.filterwarnings("ignore::SyntaxWarning")
@pytest.mark.parametrize("version", VERSIONS)
def test_accepted_skeletons_compile(version, tmp_path):
    """Random skeletons the grammar accepts compile, nesting limits included."""
    version = PythonVersion(version)
    rng = random.Random(f"block-grammar-{version}")
    functions = []
    for n in range(300):
        texts, shapes = random_code_object(rng, version)
        grammar = BlockGrammar(shapes, version)
        tokens = random_skeleton(grammar, rng, deep=n % 4 == 0)
        functions.append((tokens, "\n".join([f"def _{n}():", *render(texts, shapes, tokens, 1)]) + "\n"))
    path = tmp_path / "skeletons.py"
    path.write_text("\n".join(src for _, src in functions))
    try:
        compile_or_skip(path, version)
    except CompileError:
        for tokens, src in functions:  # find the one that fails
            path.write_text(src)
            try:
                compile_version(path, path.with_suffix(".pyc"), version)
            except CompileError as e:
                pytest.fail(f"{' '.join(tokens)}\n{src}\n{e}")
        raise


def test_complete_from_any_state():
    """From any state a walk reaches, `complete` finishes the skeleton."""
    rng = random.Random("complete")
    for _ in range(2000):
        version = PythonVersion(rng.choice(VERSIONS))
        texts, shapes = random_code_object(rng, version)
        random_skeleton(BlockGrammar(shapes, version), rng, deep=rng.random() < 0.5)


def test_shapes():
    assert str(shape_of("K_cond", "elif x:")) == "cond"
    assert str(shape_of("K_except", "except:")) == "except+bare"
    assert str(shape_of("K_none", "except:")) == "except+bare" and str(shape_of("K_none", "while True:")) == "while"
    assert str(shape_of("K_except", "except* E:")) == "except*"
    assert str(shape_of("K_case", "case [x, *_]:")) == "case"
    assert str(shape_of("K_case", "case 1 | x:")) == "case+bare"
    assert str(shape_of("K_stmt", "if x: break")) == "inline:if+break"
    assert str(shape_of("K_stmt", "for x in y: break")) == "inline:for"  # breaks its own loop
    assert str(shape_of("K_stmt", "while x: return")) == "inline:while+return"
    assert str(shape_of("K_stmt", "f(lambda: x)")) == "stmt"
    assert str(shape_of("K_stmt", "case 2: x = 1")) == "inline:case"
    assert str(shape_of("K_continue", "continue")) == "stmt+continue"
    assert str(shape_of("K_stmt", "from __future__ import annotations")) == "prefix"
    for kind, text, _ in PALETTE:
        shape = shape_of(kind, text)
        assert Shape.parse(str(shape)) == shape


def test_soft_keywords():
    """match and case are keywords only in a match statement's headers; as names they start ordinary statements."""
    names = ["case = case.strip()", "case.run()", "case: int = 1", "case[0] += 1", "case, x = y", "case(x)",
             "match = re.match(p, s)", "match.group(1)", "match: re.Match = m", "match[0] = 1", "match(x)", "matches = 1", "cases = []"]
    for text in names:
        assert line_kind(text) == "K_stmt" and str(shape_of("K_stmt", text)) == "stmt", text
    assert str(shape_of("K_stmt", "case = x; break")) == "stmt+break"
    headers = {"match x:": "K_match", "match(x):": "K_match", "match[a, b]:": "K_match", "match -x:": "K_match",
               "case 1:": "K_case", "case(1):": "K_case", "case[x, *_]:": "K_case", "case{'k': v}:": "K_case"}
    for text, kind in headers.items():
        assert line_kind(text) == kind and str(shape_of(kind, text)) == kind.removeprefix("K_"), text
    assert str(shape_of("K_stmt", "case(1): x = 1")) == "inline:case"
    # a match whose body uses its soft keywords as names fits a skeleton
    lines = ["match(x):", "case[a, b]:", "case = a", "case _:", "match = b"]
    shapes = [shape_of(line_kind(t), t) for t in lines]
    assert consistent(shapes) and BlockGrammar(shapes, "3.12").accepts("<s0> { <s1> { <s2> } <s3> { <s4> } }".split())


def test_rules():
    stmt, deco, definition, prefix = Shape(), Shape(decorator=True), Shape(definition=True), Shape(prefix=True)
    brk, cont = Shape(jumps=frozenset({"break"})), Shape(jumps=frozenset({"continue"}))
    cond, try_, bare, finally_ = Shape("cond"), Shape("try"), Shape("except", bare=True), Shape("finally")
    assert BlockGrammar([stmt, prefix], "3.12").allowed(BlockGrammar([stmt, prefix], "3.12").start()) == (0b10, [])
    assert not BlockGrammar([deco, stmt, definition], "3.12").accepts("<s0> <s1> <s2>".split())
    assert BlockGrammar([deco, stmt, definition], "3.12").accepts("<s1> <s0> <s2>".split())
    assert not BlockGrammar([brk], "3.12").accepts(["<s0>"])
    assert BlockGrammar([brk], "3.12").accepts("while_true { <s0> }".split())
    assert BlockGrammar([cond, brk], "3.12").accepts("loop <s0> { <s1> }".split())
    assert not BlockGrammar([Shape("while"), brk], "3.12").accepts("<s0> { <s1> }".split())
    assert not BlockGrammar([cond, brk], "3.12").accepts("<s0> { <s1> }".split())
    assert not BlockGrammar([try_, stmt], "3.12").accepts("<s0> { } <s1>".split())
    assert BlockGrammar([try_, stmt], "3.12").accepts("<s0> { } except { <s1> }".split())
    assert not BlockGrammar([try_, bare, Shape("except")], "3.12").accepts("<s0> { } <s1> { } <s2> { }".split())
    in_finally = "while_true { try { } finally { <s0> } }".split()
    assert not BlockGrammar([cont], "3.7").accepts(in_finally) and BlockGrammar([cont], "3.8").accepts(in_finally)
    assert not BlockGrammar([try_, Shape("except*"), brk], "3.12").accepts("while_true { <s0> { } <s1> { <s2> } }".split())
    assert not BlockGrammar([finally_], "3.12").accepts("<s0> { }".split())
    deep = ["try", OPEN] * (MAX_BLOCKS // 2) + ["try", OPEN]
    assert "try" not in BlockGrammar([stmt], "3.12").allowed(_walk(BlockGrammar([stmt], "3.12"), deep[:-2]))[1]
    assert not BlockGrammar([stmt], "3.12").accepts(deep)


def _walk(grammar: BlockGrammar, tokens: list[str]):
    state = grammar.start()
    for token in tokens:
        state = grammar.step(state, token)
    return state
