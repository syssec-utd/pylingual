from __future__ import annotations

from pylingual.control_flow_reconstruction.source import SourceLine, SourceContext
from pylingual.editable_bytecode import EditableBytecode, Inst
from pylingual.editable_bytecode.utils import comprehension_names

import networkx as nx

from abc import ABC, abstractmethod
from types import NoneType
from typing import TYPE_CHECKING, Callable, TypeAlias, TypeVar, override
from collections import defaultdict
from enum import Enum

from xdis import Code3, iscode

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG

    CFT: TypeAlias = "ControlFlowTemplate"
    C = TypeVar("C", bound=ControlFlowTemplate)


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

    def color(self):
        return {
            EdgeKind.Fall: "black",
            EdgeKind.Jump: "black",
            EdgeKind.TrueJump: "green",
            EdgeKind.FalseJump: "green",
            EdgeKind.Exception: "red",
            EdgeKind.Meta: "blue",
        }[self]


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


class NodeMatcher(ABC):
    name: str

    @abstractmethod
    def try_match(self, cfg: CFG, node: CFT | None) -> tuple[CFT | None, list[tuple[str, CFT | None]] | None]:
        """
        Checks if the node `node` is valid for this matcher.
        If successful, returns `node` (possible modified) and a list of `(name, node)` pairs to check, otherwise `None`.
        """
        ...


class EdgeMatcher(ABC):
    name: str

    @abstractmethod
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        """
        Checks if the edge `(node_a, node_b)` is valid for this matcher.
        If successful, returns `node_b` (could be different) and the name of the node that should be checked with it or `''` if no node should be matched, otherwise `None`.
        """
        ...


def out_edge_dict(cfg: CFG, node: CFT) -> dict[EdgeCategory, CFT | None]:
    d: dict[EdgeCategory, CFT | None] = defaultdict(NoneType)
    for _, dst, prop in cfg.out_edges(node, data=True):
        d[EdgeCategory.from_kind(prop["kind"])] = dst
    return d


class Template:
    def __init__(self, root: str, nodes: dict[str, NodeMatcher]):
        self.root = root
        self.nodes = nodes

    def try_match(self, cfg: CFG, node: CFT) -> dict[str, CFT | None] | None:
        """
        Checks if a subgraph rooted at `node` is valid for this matcher.
        If successful, returns a mapping from node names to nodes, otherwise `None`.
        """
        mapping: dict[str, CFT | None] = {}
        stack: list[tuple[str, CFT | None]] = [(self.root, node)]
        while stack:
            template_node, cfg_node = stack.pop()
            if template_node in mapping:
                if mapping[template_node] != cfg_node:
                    return None
                else:
                    continue
            cfg_node, x = self.nodes[template_node].try_match(cfg, cfg_node)
            if x is None:
                return None
            mapping[template_node] = cfg_node
            stack.extend(x)
        return mapping


class ConditionalNodeMatcher(NodeMatcher):
    """
    Matches the inner `NodeMatcher` only if the condition is true
    """

    def __init__(self, inner: NodeMatcher, cond: Callable[[CFG, CFT | None], bool]):
        self.inner = inner
        self.cond = cond

    @override
    def try_match(self, cfg: CFG, node: CFT | None) -> tuple[CFT | None, list[tuple[str, CFT | None]] | None]:
        if not self.cond(cfg, node):
            return node, None
        return self.inner.try_match(cfg, node)


class OptionalNodeMatcher(NodeMatcher):
    """
    Matches None or the inner `NodeMatcher`
    """

    def __init__(self, inner: NodeMatcher):
        self.inner = inner

    @override
    def try_match(self, cfg: CFG, node: CFT | None) -> tuple[CFT | None, list[tuple[str, CFT | None]] | None]:
        if node is None:
            return node, []
        return self.inner.try_match(cfg, node)


class AnyNodeMatcher(NodeMatcher):
    """
    Matches the first applicable NodeMatcher, if any
    """

    def __init__(self, *inner: NodeMatcher):
        self.inner = inner

    @override
    def try_match(self, cfg: CFG, node: CFT | None) -> tuple[CFT | None, list[tuple[str, CFT | None]] | None]:
        for inner in self.inner:
            new_node, x = inner.try_match(cfg, node)
            if x is not None:
                return new_node, x
        return node, None


class SubtemplateNodeMatcher(NodeMatcher):
    """
    Only tries to match the inner `NodeMatcher` if the template successfully matches.
    `revert_on_fail` should be used for the corresponding CFTs try_match
    """

    def __init__(self, inner: NodeMatcher, template: type[CFT]):
        self.inner = inner
        self.template = template

    @override
    def try_match(self, cfg: CFG, node: CFT | None) -> tuple[CFT | None, list[tuple[str, CFT | None]] | None]:
        if node is None:
            return node, None
        # copy = cfg.copy()
        copy = cfg
        cfg.speculate()
        if (new_node := self.template.try_match(copy, node)) is not None:
            new_node, x = self.inner.try_match(copy, new_node)
            if x is not None:
                cfg.apply_graphs()
                return new_node, x
        cfg.drop_graphs()
        return node, None


class NodeTemplate(NodeMatcher):
    """
    Matches a node if all of its edges match the matcher's corresponding `EdgeMatcher`
    """

    def __init__(self, edges: dict[EdgeCategory, EdgeMatcher]):
        self.edges = edges

    @override
    def try_match(self, cfg: CFG, node: CFT | None) -> tuple[CFT | None, list[tuple[str, CFT | None]] | None]:
        if node is None or node not in cfg.nodes:
            return node, None
        out_edges = out_edge_dict(cfg, node)
        next_nodes: list[tuple[str, CFT | None]] = []
        for edge_type, edge_matcher in self.edges.items():
            next_node = out_edges[edge_type]
            next = edge_matcher.try_match(cfg, node, next_node)
            if next is None:
                return node, None
            if next[1]:
                next_nodes.append((next[1], next[0]))
        return node, next_nodes


class EdgeTemplate(EdgeMatcher):
    """
    Matches an edge `(a, b)` if `b` is not None
    Assigns `b` to the node with name `name`
    """

    def __init__(self, name: str):
        self.name = name

    @override
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        if node_b is not None:
            return (node_b, self.name)


class OptionalEdge(EdgeMatcher):
    """
    Matches any edge `(a, b)`, even if `b` is None
    Assigns `b` to the node with name `name` if `b` is not None
    """

    def __init__(self, name: str):
        self.name = name

    @override
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        if node_b is not None:
            return (node_b, self.name)
        return (node_b, "")


class OptExcEdge(EdgeMatcher):
    def __init__(self, name: str):
        self.name = name

    @override
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        if node_b is None and all(x.opname == "JUMP_BACKWARD" for x in node_a.get_instructions()):
            return (node_b, "")
        if node_b is not None and cfg.get_edge_data(node_a, node_b, {}).get("kind") is EdgeKind.Meta:
            return (node_b, "")
        return (node_b, self.name)


class NoEdge(EdgeMatcher):
    """
    Matches an edge `(a, b)` if `b` is None (i.e. there is no edge)
    """

    edge = ""

    @override
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        if node_b is None:
            return (node_b, "")


class ExitableEdge(EdgeMatcher):
    def __init__(self, name: str):
        self.name = name

    @override
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        if node_b is None:
            d = out_edge_dict(cfg, node_a)
            if d[EdgeCategory.Meta] is not None:
                return (d[EdgeCategory.Meta], "")
            if d[EdgeCategory.Natural] is None and d[EdgeCategory.Conditional] is None:
                return (cfg.end, "")
        return (node_b, self.name)


class RaiseOutEdge(EdgeMatcher):
    def __init__(self, name: str):
        self.name = name

    @override
    def try_match(self, cfg: CFG, node_a: CFT, node_b: CFT | None) -> tuple[CFT | None, str] | None:
        if node_a.get_instructions()[-1].opname not in ["RERAISE", "RAISE_VARARGS"]:
            return None
        if node_b is None:
            d = out_edge_dict(cfg, node_a)
            if d[EdgeCategory.Meta] is not None:
                return (d[EdgeCategory.Meta], "")
        return (node_b, self.name)


class ControlFlowTemplate(ABC):
    members: dict[str, CFT | None]
    template: Template
    offset: int
    header_lines: list[SourceLine]
    blame: Code3
    _pos: list[tuple[float, float]]

    def __init__(self, members: dict[str, CFT | None]):
        self.members = members
        first = next(x for x in members.values() if x is not None)
        self.offset = first.offset
        self.header_lines = []
        self.blame = first.blame
        self._pos = sum((x._pos for x in members.values() if x is not None), start=[])

    def pos(self):
        if not self._pos:
            return "0.0,0.0!"
        avg_x = sum(x for x, _ in self._pos) / len(self._pos)
        avg_y = sum(y for _, y in self._pos) / len(self._pos)
        return f"{avg_x},{avg_y}!"

    def __getattr__(self, name: str) -> CFT:
        x = self.members[name]
        if x is not None:
            return x
        return MetaTemplate(f"{name} (empty)", self.blame)

    @classmethod
    @abstractmethod
    def try_match(cls, cfg: CFG, node: CFT) -> CFT | None:
        """
        Trys to match this template starting at `node`. Returns the new node if the match was successful.
        Modifies `cfg` on success.
        """
        ...

    @abstractmethod
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        """
        Returns the source code for this template, recursively calling into its children to create the full source code.
        """
        ...

    @override
    def __repr__(self) -> str:
        name = type(self).__name__
        components = indent_str(",\n".join(f"{k}={repr(v)}" for k, v in self.members.items()))
        return f"{name}[\n{components}]"

    def get_instructions(self) -> list[Inst]:
        return [i for m in self.members.values() if m is not None for i in m.get_instructions()]

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
        self._pos = []

    @staticmethod
    def match_all(cfg):
        mapping = {node: InstTemplate(node) for node in cfg.nodes if isinstance(node, Inst)}
        nx.relabel_nodes(cfg, mapping, copy=False)

    @override
    @classmethod
    def try_match(cls, cfg, node):
        raise NotImplementedError

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
        self._pos = []
        self.blame = blame

    @override
    @classmethod
    def try_match(cls, cfg: CFG, node: ControlFlowTemplate) -> ControlFlowTemplate | None:
        raise NotImplementedError

    @override
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        return self.line(f"# meta: {self.name}", meta=True)

    @override
    def get_instructions(self):
        return []

    @override
    def __repr__(self):
        return f"MetaTemplate[{self.name}]"


template_dict: dict[int, list[tuple[type[ControlFlowTemplate], int]]] = defaultdict(list)
version_specific_template_dict: dict[tuple[int, int], dict[int, list[tuple[type[ControlFlowTemplate], int]]]] = defaultdict(lambda: defaultdict(list))


def register_template(run: int, priority: int, *versions: tuple[int, int]):
    """
    Register a control flow template to be used in run `run` with priority `priority`.
    If no versions are given, the template is used for all versions.
    """

    def deco(template: type[C]) -> type[C]:
        if not versions:
            template_dict[run].append((template, priority))
        else:
            for version in versions:
                version_specific_template_dict[version][run].append((template, priority))
        return template

    return deco


def get_template_runs(version: tuple[int, int]) -> list[list[type[ControlFlowTemplate]]]:
    runs: dict[int, list[tuple[type[ControlFlowTemplate], int]]] = defaultdict(list)
    for run in (template_dict | version_specific_template_dict[version]).keys():
        runs[run].extend(template_dict[run])
        runs[run].extend(version_specific_template_dict[version][run])
    return [[x[0] for x in sorted(runs[run], key=lambda x: x[1])] for run in sorted(runs)]
