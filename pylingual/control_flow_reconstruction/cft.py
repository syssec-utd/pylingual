from __future__ import annotations

from pylingual.control_flow_reconstruction.source import SourceLine, SourceContext
from pylingual.editable_bytecode import EditableBytecode, Inst
from pylingual.editable_bytecode.utils import comprehension_names

import networkx as nx

from abc import ABC, abstractmethod
from types import NoneType
from typing import TYPE_CHECKING, TypeAlias, override
from collections import defaultdict
from enum import Enum

from xdis import Code3, iscode

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG

    CFT: TypeAlias = "ControlFlowTemplate"


def indent_str(string: str, tabs: int = 1) -> str:
    return "\n".join("\t" * tabs + line.rstrip() for line in string.split("\n") if line)


class EdgeKind(Enum):
    Fall = "natural"
    Jump = "jump"
    TrueJump = "true_jump"
    FalseJump = "false_jump"
    Exception = "exception"
    Meta = "meta"

    def prop(self):
        return {"kind": self}

    def __str__(self):
        return self.value


class EdgeCategory(Enum):
    Natural = "natural"
    Conditional = "conditional"
    Exception = "exception"
    Meta = "meta"

    @staticmethod
    def from_kind(kind: EdgeKind):
        kind = EdgeKind(kind)
        if kind in [EdgeKind.Fall, EdgeKind.Jump]:
            return EdgeCategory.Natural
        if kind in [EdgeKind.TrueJump, EdgeKind.FalseJump]:
            return EdgeCategory.Conditional
        return EdgeCategory(kind.value)


def out_edge_dict(cfg: CFG, node: CFT) -> dict[EdgeCategory, CFT | None]:
    d: dict[EdgeCategory, CFT | None] = defaultdict(NoneType)
    for _, dst, prop in cfg.out_edges(node, data=True):
        d[EdgeCategory.from_kind(prop["kind"])] = dst
    return d


class ControlFlowTemplate(ABC):
    """Part of a code object (an instruction, a basic block, a whole code object's skeleton) that renders as source."""

    offset: int
    header_lines: list[SourceLine]
    blame: Code3

    @abstractmethod
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        """
        Returns the source code for this template, recursively calling into its children to create the full source code.
        """
        ...

    @abstractmethod
    def get_instructions(self) -> list[Inst]: ...

    def line(self, s: str, i: int = 0, child: Code3 | None = None, meta: bool = False):
        assert s
        return [SourceLine(s, i, self.blame, child, meta)]

    def add_header(self, s: str, meta: bool = False):
        self.header_lines.extend(self.line(s, meta=meta))


class InstTemplate(ControlFlowTemplate):
    def __init__(self, inst: Inst):
        self.inst = inst
        self.offset = self.inst.offset
        self.blame = inst.bytecode.codeobj
        self.header_lines = []

    @staticmethod
    def match_all(cfg):
        mapping = {node: InstTemplate(node) for node in cfg.nodes if isinstance(node, Inst)}
        nx.relabel_nodes(cfg, mapping, copy=False)

    @override
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        line = source.line_of(self.inst)
        lines = self.line(line) if line else []
        if self.inst.opname == "LOAD_CONST" and iscode(self.inst.argval):
            if self.inst.argval in source.cfts and self.inst.argval.co_name not in comprehension_names:  # type: ignore
                lines.append(SourceLine("", 1, self.inst.argval, self.inst.argval))
        return lines

    @override
    def get_instructions(self):
        return [self.inst]

    @override
    def __repr__(self):
        x = None
        if self.inst.arg is None:
            x = f"<{self.inst.offset}: {self.inst.opname}>"
        elif not self.inst.argrepr:
            x = f"<{self.inst.offset}: {self.inst.opname} {self.inst.arg}>"
        elif self.inst.opname == "LOAD_CONST":
            arg = self.inst.bytecode.co_consts[self.inst.arg]  # type: ignore
            if isinstance(arg, EditableBytecode):
                x = f"<{self.inst.offset}: {self.inst.opname} {self.inst.arg} ({arg.name})>"
        if x is None:
            x = f"<{self.inst.offset}: {self.inst.opname} {self.inst.arg} ({self.inst.argrepr})>"
        if self.inst.starts_line is not None:
            return f"[{self.inst.starts_line}] {x}"
        return x


class MetaTemplate(ControlFlowTemplate):
    def __init__(self, name: str, blame: Code3):
        self.name = name
        self.offset = -1
        self.header_lines = []
        self.blame = blame

    @override
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        return self.line(f"# meta: {self.name}", meta=True)

    @override
    def get_instructions(self):
        return []

    @override
    def __repr__(self):
        return f"MetaTemplate[{self.name}]"
