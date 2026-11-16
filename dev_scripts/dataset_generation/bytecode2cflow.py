# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../", editable = true }
# ///
"""
Control flow model dataset: (input, gold skeleton) rows for the code objects of a compiled code dataset.
The gold skeleton is read from the source's AST, and every label is checked by recompiling it: a code object is kept
only if the source rendered from its gold skeleton compiles to equivalent bytecode.
"""

from __future__ import annotations

import ast
import json
import logging
import multiprocessing
import signal
import tempfile
from pathlib import Path

import tqdm

from pylingual.control_flow_reconstruction.model_view import cflow_request
from pylingual.control_flow_reconstruction.skeleton import BLOCK_KEYWORDS, ref
from pylingual.control_flow_reconstruction.source import SourceContext
from pylingual.control_flow_reconstruction.skeleton_template import SkeletonTemplate
from pylingual.editable_bytecode import EditableBytecode, PYCFile
from pylingual.equivalence_check import compare_pyc
from pylingual.masking.ast_masker import DUMMY_DECORATOR
from pylingual.utils.generate_bytecode import CompileError, compile_version


class Invalid(Exception):
    pass


def mark_line_starts(bc: EditableBytecode, lno_insts: dict, src_lines: list[str]):
    """Keep `starts_line` only on the first instruction of each line, like the segmentation model does."""
    merged: set[int] = set()
    for lno, insts in lno_insts.items():
        if lno in merged:
            for inst in insts:
                inst.starts_line = None
            continue
        insts[0].starts_line = lno
        for inst in insts[1:]:
            inst.starts_line = None
        # <= 3.7 gives a decorated definition the line of its first decorator
        if lno is not None and bc.version <= (3, 7) and src_lines[lno - 1].strip().startswith("@"):
            build = next((i for i in insts if i.opname == "LOAD_BUILD_CLASS"), None)
            cls = next((n for n in range(lno + 1, len(src_lines) + 1) if src_lines[n - 1].strip().startswith("class ")), None)
            if build is not None and cls is not None:
                # base classes load after the class body, so the class line starts at LOAD_BUILD_CLASS
                build.starts_line = cls
                merged.add(cls)
            elif lno + 1 not in lno_insts:
                bc.instructions[insts[0].offset // 2 + 1].starts_line = lno + 1


def assign_lines(pyc: PYCFile, src_lines: list[str]):
    """Mark line starts like the segmentation model does, after merging duplicated returns like the segmentation dataset (bytecode2csv.py)."""
    if pyc.version == (3, 10):
        pyc.replace_duplicated_returns10(src_lines)
    elif pyc.version >= (3, 12):
        pyc.replace_duplicated_returns12(src_lines)
    seen: set[int] = set()
    for bc in pyc.iter_bytecodes():
        if bc.is_comprehension:
            continue
        lno_insts = bc.get_lno_insts(previously_seen_lines=seen)
        mark_line_starts(bc, lno_insts, src_lines)
        seen.update(set(lno_insts) - {None})


class SkeletonBuilder:
    """Gold skeleton of an AST body; `line2idx` maps each source line to the statement that starts it."""

    def __init__(self, lines: list[str], line2idx: dict[int, int]):
        self.lines = lines
        self.line2idx = line2idx
        self.used: set[int] = set()

    def text(self, lno: int) -> str:
        return self.lines[lno - 1].strip()

    def ref(self, lno: int) -> str | None:
        """Reference to the statement starting at line `lno` (None if no statement does); each is used once."""
        i = self.line2idx.get(lno)
        if i is None:
            return None
        if i in self.used:
            raise Invalid(f"line {lno} used twice")
        self.used.add(i)
        return ref(i)

    def header(self, lno: int, keyword: str | None = None) -> list[str]:
        """A block header: its statement, or `keyword` if the line has no bytecode (`try:`, `else:`)."""
        r = self.ref(lno)
        if r is not None:
            return [r]
        if keyword is None:
            raise Invalid(f"header line {lno} has no bytecode: {self.text(lno)!r}")
        return [keyword]

    def find_line(self, start: int, end: int, word: str) -> int:
        """Line of a bare `else:` / `finally:` between `start` and `end`; the AST does not record it."""
        for lno in range(start, end):
            if self.text(lno).rstrip(":").strip() == word:
                return lno
        raise Invalid(f"no {word} line in {start}-{end}")

    def block(self, head: list[str], body: list[ast.stmt]) -> list[str]:
        inner = self.body(body)
        if not inner and head[0] in BLOCK_KEYWORDS:
            raise Invalid("empty keyword block")  # the decoding grammar never closes one
        return head + ["{", *inner, "}"]

    def subtree_empty(self, nodes: list[ast.stmt]) -> bool:
        """No statement in `nodes` has bytecode (dead code the compiler removed)."""
        return all(self.line2idx.get(n.lineno) is None and all(self.line2idx.get(c.lineno) is None for c in ast.walk(n) if isinstance(c, ast.stmt)) for n in nodes)

    def body(self, nodes: list[ast.stmt]) -> list[str]:
        out: list[str] = []
        for n in nodes:
            out += self.stmt(n)
        return out

    def stmt(self, n: ast.stmt) -> list[str]:
        if isinstance(n, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith, ast.Try, ast.Match)) or type(n).__name__ == "TryStar":
            # dead compound statements disappear from the bytecode
            if self.subtree_empty([n]):
                return []
        if isinstance(n, ast.If):
            return self.if_(n)
        if isinstance(n, ast.While):
            # `while cond:` has bytecode for its line; `while True:` usually has none
            test_true = isinstance(n.test, ast.Constant) and bool(n.test.value)
            head = ["loop", r] if (r := self.ref(n.lineno)) else (["while_true"] if test_true else None)
            if head is None:
                raise Invalid("while header without bytecode")
            return self.block(head, n.body) + self.orelse(n)
        if isinstance(n, (ast.For, ast.AsyncFor)):
            return self.block(self.header(n.lineno), n.body) + self.orelse(n)
        if isinstance(n, (ast.With, ast.AsyncWith)):
            return self.block(self.header(n.lineno), n.body)
        if isinstance(n, ast.Try) or type(n).__name__ == "TryStar":
            out = self.block(self.header(n.lineno, "try"), n.body)
            for h in n.handlers:
                out += self.block(self.header(h.lineno, "except" if h.type is None else None), h.body)
            out += self.orelse(n)
            if n.finalbody:
                prev = (n.orelse or n.handlers or n.body)[-1].end_lineno
                fl = self.find_line(prev + 1, n.finalbody[0].lineno, "finally")
                out += self.block(self.header(fl, "finally"), n.finalbody)
            return out
        if isinstance(n, ast.Match):
            out = self.header(n.lineno) + ["{"]
            for c in n.cases:
                default = isinstance(c.pattern, ast.MatchAs) and c.pattern.pattern is None and c.pattern.name is None and c.guard is None
                out += self.block(self.header(c.pattern.lineno, "case_" if default else None), c.body)
            return out + ["}"]
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # a definition's body is another code object; here it is its decorator and def lines
            first = min([d.lineno for d in n.decorator_list] + [n.lineno])
            return [r for lno in range(first, n.lineno + 1) if (r := self.ref(lno))]
        # a simple statement, possibly over several lines; a break / continue without bytecode becomes its keyword
        refs = [r for lno in range(n.lineno, (n.end_lineno or n.lineno) + 1) if (r := self.ref(lno))]
        if not refs and isinstance(n, ast.Break):
            return ["break"]
        if not refs and isinstance(n, ast.Continue):
            return ["continue"]
        return refs

    def if_(self, n: ast.If) -> list[str]:
        """`<if> { ... }`, with `elif` as `else { <if> { ... } }`."""
        out = self.block(self.header(n.lineno), n.body)
        if not n.orelse or self.subtree_empty(n.orelse):
            return out
        if len(n.orelse) == 1 and isinstance(n.orelse[0], ast.If) and self.text(n.orelse[0].lineno).startswith("elif "):
            return out + ["else", "{", *self.if_(n.orelse[0]), "}"]
        return out + self.orelse(n)

    def orelse(self, n) -> list[str]:
        if not n.orelse or self.subtree_empty(n.orelse):
            return []
        prev = (getattr(n, "handlers", None) or n.body)[-1].end_lineno
        el = self.find_line(prev + 1, n.orelse[0].lineno, "else")
        return self.block(self.header(el, "else"), n.orelse)


def code_object_body(tree: ast.Module, bc: EditableBytecode) -> list[ast.stmt] | None:
    """Find the AST body that compiles to `bc`, matching on the first line of the code object."""
    if bc.parent is None:
        return tree.body
    name = bc.codeobj.co_name
    first = bc.codeobj.co_firstlineno
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == name:
            if first in (node.lineno, *(d.lineno for d in node.decorator_list)):
                return node.body
    return None


def make_examples(pyc: PYCFile, src: str) -> list[dict]:
    """
    Examples for the code objects of `pyc`. An example is a dict with the request fields (CflowRequest.row), the gold
    skeleton as `target`, and the bytecode and statements (`_bc`, `_stmts`) for rendering. A gold skeleton must fit the
    block grammar, so a code object whose source the grammar does not describe is left out.
    """
    lines = src.split("\n")
    tree = ast.parse(src)
    assign_lines(pyc, lines)
    examples = []
    for bc in pyc.iter_bytecodes():
        request = cflow_request(bc, lines)
        body = code_object_body(tree, bc)
        if request is None or body is None:
            continue
        stmts = request.stmts
        line2idx = {s.insts[0].starts_line: s.index for s in stmts if s.insts[0].starts_line is not None}
        try:
            builder = SkeletonBuilder(lines, line2idx)
            target = builder.body(body)
            missing = set(line2idx.values()) - builder.used
            if missing:
                raise Invalid(f"unused statements {sorted(missing)}")
            if error := request.grammar().check(target):
                raise Invalid(f"gold skeleton outside the block grammar: {error}")
        except Invalid:
            continue
        examples.append({"name": bc.name, **request.row(), "target": " ".join(target), "_bc": bc, "_stmts": stmts})
    return examples


def render_with_skeletons(pyc: PYCFile, lines: list[str], examples: list[dict]) -> str:
    """Source of `pyc` with the gold skeletons of `examples`; other code objects get their statements in order."""
    by_bc = {e["_bc"]: e for e in examples}
    cfts = {}
    for bc in pyc.iter_bytecodes():
        e = by_bc.get(bc)
        if e is None:
            cfts[bc.codeobj] = SkeletonTemplate.for_request(bc, cflow_request(bc, lines))
        else:
            cfts[bc.codeobj] = SkeletonTemplate(bc, e["_stmts"], e["target"].split())
    return str(SourceContext(pyc, lines, cfts))


def load_pair(py_path: Path, pyc_path: Path, tmp: Path) -> tuple[str, PYCFile, Path]:
    """Source, pyc and pyc path of a dataset file as the decompiler sees it."""
    src = py_path.read_text()
    pyc = PYCFile(pyc_path)
    if pyc.version <= (3, 7):
        # drop the dummy decorators create_code_dataset added; the decompiler never sees them
        src = "\n".join(line for line in src.split("\n") if line.strip() != f"@{DUMMY_DECORATOR}")
        py_path = tmp / "source.py"
        py_path.write_text(src)
        pyc_path = py_path.with_suffix(".pyc")
        compile_version(py_path, pyc_path, pyc.version)
        pyc = PYCFile(pyc_path)
    return src, pyc, pyc_path


def equivalent_names(pyc: PYCFile, pyc_path: Path, src: str, examples: list[dict], out: Path) -> set[str] | None:
    """
    Names of the code objects that recompile to equivalent bytecode with the skeletons of `examples` (written to
    `out`), or None if the source does not compile.
    """
    out.write_text(render_with_skeletons(pyc, src.split("\n"), examples))
    try:
        compile_version(out, out.with_suffix(".pyc"), pyc.version)
    except CompileError:
        return None
    results = compare_pyc(pyc_path, out.with_suffix(".pyc"))
    # code objects can share a name (a property and its setter), so a name passes only if all of them do
    return {r.name_a for r in results if r.success} - {r.name_a for r in results if not r.success}


def bytecode2cflow(py_path: Path, pyc_path: Path) -> list[dict]:
    """Rows for the code objects of one file whose gold skeleton recompiles to equivalent bytecode."""
    with tempfile.TemporaryDirectory() as tmp:
        src, pyc, pyc_path = load_pair(py_path, pyc_path, Path(tmp))
        examples = make_examples(pyc, src)
        ok = equivalent_names(pyc, pyc_path, src, examples, Path(tmp) / "gold.py") if examples else None
    return [{k: v for k, v in e.items() if k != "name" and not k.startswith("_")} | {"file": str(py_path)} for e in examples if ok and e["name"] in ok]


def _timeout(*_):
    raise TimeoutError("file took over 60s")


def bytecode2cflow_exception_wrapper(paths: tuple[Path, Path]) -> list[dict] | Exception:
    # a huge file can take minutes; skip it instead of stalling the pool
    signal.signal(signal.SIGALRM, _timeout)
    signal.alarm(60)
    try:
        return bytecode2cflow(*paths)
    except Exception as error:
        return Exception(f"{type(error)}: {error} in file {paths}")
    finally:
        signal.alarm(0)


def write_cflow(source_path: Path, out_jsonl: Path, logger: logging.Logger):
    """Write the rows of every file in `source_path` (one directory per file) to `out_jsonl`, without duplicates."""
    pairs = [(py, py.with_suffix(".pyc")) for d in sorted(source_path.iterdir()) if (py := next(d.glob("*.py"), None)) and py.with_suffix(".pyc").exists()]
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    num_fails = 0
    with out_jsonl.open("w") as out, multiprocessing.Pool(maxtasksperchild=100) as pool, tqdm.tqdm(total=len(pairs)) as progress_bar:
        for result in pool.imap_unordered(bytecode2cflow_exception_wrapper, pairs):
            progress_bar.update()
            if isinstance(result, Exception):
                num_fails += 1
                logger.debug(result)
                continue
            for row in result:
                if (row["input"], row["target"]) not in seen:
                    seen.add((row["input"], row["target"]))
                    out.write(json.dumps(row) + "\n")
    logger.info(f"{out_jsonl}: {len(seen)} rows from {len(pairs)} files, {num_fails} failed")


def create_cflow_dataset(code_dir: Path, cflow_dir: Path, logger: logging.Logger):
    for split in ("train", "test", "valid"):
        if (code_dir / split).exists():
            write_cflow(code_dir / split, cflow_dir / f"{split}.jsonl", logger)
