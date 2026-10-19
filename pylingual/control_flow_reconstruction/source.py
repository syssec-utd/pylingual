from __future__ import annotations

import itertools
import keyword
from collections import defaultdict
import inspect
import ast
import re

from typing import TYPE_CHECKING, Generator, NamedTuple
from xdis import Code3

from pylingual.editable_bytecode import PYCFile
from pylingual.editable_bytecode.EditableBytecode import EditableBytecode
from pylingual.utils.use_escape_sequences import use_escape_sequences
from pylingual.utils.version import PythonVersion

if TYPE_CHECKING:
    from pylingual.editable_bytecode import Inst
    from .cft import ControlFlowTemplate


def indent_lines(lines: list[SourceLine], i: int = 1) -> list[SourceLine]:
    return [SourceLine(x.line, x.indent + i, x.blame, x.child, x.meta) for x in lines]


class SourceLine(NamedTuple):
    line: str
    indent: int
    blame: Code3
    child: Code3 | None = None
    meta: bool = False

    def with_line(self, line: str):
        return SourceLine(line, self.indent, self.blame, self.child, self.meta)


# class bookkeeping the compiler generates; the model sometimes translates it into an assignment
compiler_generated_assignment = re.compile(r"(__static_attributes__|__firstlineno__|__classdictcell__|__classcell__)\s*=[^=]")


def sanitize_lines(lines: list[str]) -> list[str]:
    return ["" if x in ("break", "continue", "except:", "while True:", "try:") or compiler_generated_assignment.match(x) else x for x in (x[2:] if x.startswith("elif ") else x for x in (x.strip() for x in lines))]


def fake_header(co: Code3):
    name = co.co_name if co.co_name.isidentifier() and not keyword.iskeyword(co.co_name) else "_"
    if co.co_flags & inspect.CO_ASYNC_GENERATOR:
        return f"async def {name}():"
    if co.co_flags & inspect.CO_NEWLOCALS:
        return f"def {name}():"
    return f"class {name}:"


def valid_header(line: SourceLine, version: PythonVersion):
    try:
        ast.parse(line.line + "pass", feature_version=version.as_tuple())
        return True
    except Exception:
        return False


class SourceContext:
    def __init__(self, pyc: PYCFile, lines: list[str], cfts: dict[Code3, ControlFlowTemplate]):
        self.pyc = pyc
        self.lines = sanitize_lines(lines)
        self.cfts = cfts
        self.cache: dict[ControlFlowTemplate, list[SourceLine]] = {}
        # lines read while rendering each code object's templates, so cached sources can be kept when other lines change
        self.reads: dict[Code3, dict[Inst, str | None]] = defaultdict(dict)
        self.rendering: list[Code3] = []
        self.header_lines: list[SourceLine] = []
        self.purged_cfts: list[ControlFlowTemplate] = []
        self.init_header()

    def init_header(self):
        for bc in self.pyc.iter_bytecodes():
            cft = self.cfts[bc.codeobj]
            if bc.codeobj.co_flags & inspect.CO_NEWLOCALS:
                has_docstring_314 = bool(bc.codeobj.co_flags & 2**26) # inspect.CO_HAS_DOCSTRING flag introduced in Python 3.14
                if (self.pyc.version < (3, 14) or has_docstring_314) and bc.codeobj.co_consts and isinstance(bc.codeobj.co_consts[0], str):
                    doc = use_escape_sequences(bc.codeobj.co_consts[0])
                    cft.add_header(f'"""{doc}"""')
            if bc.codeobj.co_flags & (inspect.CO_GENERATOR | inspect.CO_ASYNC_GENERATOR):
                line_nos = [i.starts_line - 1 for i in cft.get_instructions() if i.starts_line is not None]
                if not any(self.lines[n].strip().startswith("yield ") or self.lines[n].strip() == "yield" for n in line_nos):
                    # the model sometimes translates the fake yield to a bare "if False:"
                    if_false = next((n for n in line_nos if self.lines[n].strip() == "if False:"), None)
                    if if_false is not None:
                        self.lines[if_false] = "if False: yield"
                    else:
                        cft.add_header("if False: yield")
            for global_var in bc.globals:
                cft.add_header(f"global {global_var}")
            parent_nonlocal = set()
            parent = bc.parent
            while parent:
                parent_nonlocal |= parent.nonlocals
                parent = parent.parent
            for nonlocal_var in bc.nonlocals:
                if nonlocal_var in parent_nonlocal:
                    cft.add_header(f"nonlocal {nonlocal_var}")

    def __getitem__(self, template: ControlFlowTemplate | tuple[ControlFlowTemplate, int]):
        if isinstance(template, tuple):
            template, indent = template
        else:
            indent = 0
        if self.rendering and template.blame is not self.rendering[-1]:
            # reads would be blamed on the wrong code object, so don't cache
            self.rendering.append(template.blame)
            try:
                src = template.to_indented_source(self)
            finally:
                self.rendering.pop()
        else:
            if template not in self.cache:
                self.rendering.append(template.blame)
                try:
                    self.cache[template] = template.to_indented_source(self)
                finally:
                    self.rendering.pop()
            src = self.cache[template]
        if indent:
            return indent_lines(template.header_lines + src, indent)
        return template.header_lines + src

    def line_of(self, inst: Inst) -> str | None:
        line = None if inst.starts_line is None else self.lines[inst.starts_line - 1]
        for co in set(self.rendering):
            self.reads[co][inst] = line
        return line

    def source_lines_of(self, co: Code3, i=0) -> Generator[SourceLine]:
        lines = self[self.cfts[co], i]
        purged = self.cfts[co] in self.purged_cfts
        prev = None
        for line in lines:
            if line.child:
                if purged:
                    if prev and valid_header(prev, self.pyc.version):
                        yield prev
                    else:
                        yield SourceLine(fake_header(line.child), line.indent - 1, line.child)
                yield from self.source_lines_of(line.child, line.indent)
            elif purged:
                # keep imports, 3.12+ children compile differently without them
                if line.indent == i and not line.meta and line.line.startswith(("import ", "from ")):
                    yield line
            else:
                # filter out returns in top level codeobjs and classes
                if not co.co_flags & (inspect.CO_NEWLOCALS | inspect.CO_GENERATOR | inspect.CO_ASYNC_GENERATOR):
                    if line.line in ("return", "return None"):
                        yield line.with_line("pass")
                    elif line.line.startswith("return "):
                        yield SourceLine("# " + line.line, line.indent, line.blame, meta=True)
                    else:
                        yield line
                else:
                    yield line
            prev = line

    def purge(self, co: Code3):
        self.purged_cfts.append(self.cfts[co])

    def source_lines(self):
        def is_doc(x: SourceLine):
            return x.line.startswith(('__doc__ = "', "__doc__ = '", '"""'))

        def is_prefix(x: SourceLine):
            return is_doc(x) or x.line.startswith(("from __future__ import ", "global ", "nonlocal "))

        def priority(x: SourceLine):
            if is_doc(x):
                return 0
            if x.line.startswith("from __future__ import "):
                return 1
            return 2

        # the docstring and __future__ imports must stay first, ahead of header lines like `global x`
        # the leading comment lines are skipped so they don't stop the reordering
        lines = self.header_lines + list(self.source_lines_of(self.pyc.codeobj))
        start = len(self.header_lines)
        prefix = [x.with_line(x.line[10:]) if x.line.startswith("__doc__ = ") else x for x in sorted(itertools.takewhile(is_prefix, lines[start:]), key=priority)]
        lines[start : start + len(prefix)] = prefix

        # insert pass in empty blocks
        colon_line = None
        new_lines = []
        for x in lines:
            if colon_line is not None:
                if x.indent <= colon_line.indent:
                    new_lines.append(SourceLine("pass", colon_line.indent + 1, colon_line.blame))
                if not x.meta:
                    colon_line = None
            if x.line.endswith(":"):
                colon_line = x
            new_lines.append(x)
        if colon_line is not None:
            new_lines.append(SourceLine("pass", colon_line.indent + 1, colon_line.blame))

        return new_lines

    def __str__(self):
        return "\n".join("    " * x.indent + x.line for x in self.source_lines())

    def update_cft(self, bc: EditableBytecode, template: ControlFlowTemplate):
        x = bc
        while x.parent is not None:
            del self.cache[self.cfts[x.codeobj]]
            x = x.parent
        self.cfts[bc.codeobj] = template

    def update_lines(self, lines: list[str]):
        self.lines = sanitize_lines(lines)
        # only rebuild the sources of code objects that read a line that changed
        changed = {co for co, reads in self.reads.items() if any((None if inst.starts_line is None else self.lines[inst.starts_line - 1]) != line for inst, line in reads.items())}
        for co in changed:
            del self.reads[co]
        for template in [t for t in self.cache if t.blame in changed]:
            del self.cache[template]

    def snapshot(self):
        return self.lines, self.cache.copy(), {co: reads.copy() for co, reads in self.reads.items()}

    def restore(self, snapshot):
        self.lines, cache, reads = snapshot
        self.cache.clear()
        self.cache.update(cache)
        self.reads.clear()
        self.reads.update(reads)
