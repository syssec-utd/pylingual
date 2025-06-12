from __future__ import annotations

from functools import partial
from itertools import chain
import textwrap
import pdb
import sys

from typing import TYPE_CHECKING, Callable, TypeVar, override

from pylingual.utils.version import supported_versions
from .cft import (
    AnyNodeMatcher,
    ConditionalNodeMatcher,
    ControlFlowTemplate,
    EdgeCategory,
    EdgeKind,
    EdgeMatcher,
    EdgeTemplate,
    ExitableEdge,
    InstTemplate,
    OptExcEdge,
    RaiseOutEdge,
    SourceContext,
    SourceLine,
    SubtemplateNodeMatcher,
    Template,
    NoEdge,
    NodeMatcher,
    NodeTemplate,
    OptionalEdge,
    OptionalNodeMatcher,
)

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG

    C = TypeVar("C", bound=ControlFlowTemplate)

no_edge = NoEdge()


def has_in_degree(n: int):
    def check_in_degree(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return node is not None and cfg.in_degree(node) == n

    return check_in_degree


def exact_instructions(*opnames: str):
    def check_instructions(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return node is not None and tuple(x.opname for x in node.get_instructions()) == opnames

    return check_instructions


def starting_instructions(*opnames: str):
    def check_instructions(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return node is not None and tuple(x.opname for x in node.get_instructions()[: len(opnames)]) == opnames

    return check_instructions


def ending_instructions(*opnames: str):
    def check_instructions(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return node is not None and tuple(x.opname for x in node.get_instructions()[-len(opnames) :]) == opnames

    return check_instructions


def without_instructions(*opnames: str):
    def check_instructions(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return node is not None and all(x.opname not in opnames for x in node.get_instructions())

    return check_instructions

def with_instructions(*opnames: str):
    def check_instructions(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        ops = {x.opname for x in node.get_instructions()}
        return node is not None and all(opname in ops for opname in opnames)

    return check_instructions

def without_top_level_instructions(*opnames: str):
    from .templates.Block import BlockTemplate

    def check_instructions(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        if isinstance(node, BlockTemplate):
            return all(x.inst.opname not in opnames for x in node.members if isinstance(x, InstTemplate))
        if isinstance(node, InstTemplate):
            return node.inst.opname not in opnames
        return True

    return check_instructions


def has_type(*template_type: type[ControlFlowTemplate]):
    def check_type(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return isinstance(node, template_type)

    return check_type


def no_back_edges(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
    return node is None or not any(cfg.dominates(succ, node) for succ in cfg.successors(node))


def run_is(n: int):
    def check_run(cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return cfg.run == n

    return check_run


_AUTO_EXC = "_EXC"


def T(root: str | None = None, **nodes: N | NodeTemplate) -> Template:
    """
    Convenience function for creating `Template`s
    If `root` is None, the first node in `nodes` is used
    """
    assert _AUTO_EXC not in nodes
    if any(x._auto_exc for x in nodes.values() if isinstance(x, N)):
        nodes[_AUTO_EXC] = N.tail().optional()
    if root is None:
        root = next(iter(nodes))
    return Template(root, {k: v._build(k) if isinstance(v, N) else v for k, v in nodes.items()})


if TYPE_CHECKING:
    NodeCondition = Callable[[CFG, ControlFlowTemplate | None], bool]

_ec = [EdgeCategory.Natural, EdgeCategory.Conditional, EdgeCategory.Exception, EdgeCategory.Meta]
_no_edges = {k: no_edge for k in _ec}


def _to_edge_dict(*edges: tuple[EdgeCategory, EdgeMatcher] | str | None) -> dict[EdgeCategory, EdgeMatcher]:
    return dict(x if isinstance(x, tuple) else (_ec[i], E._(x)) for i, x in enumerate(edges))


class N:
    """
    `NodeTemplate` builder class
    """

    _edges: dict[EdgeCategory, EdgeMatcher]
    _conds: list[NodeCondition]
    _is_optional: bool
    _auto_exc: bool

    def __init__(self, *edges: tuple[EdgeCategory, EdgeMatcher] | str | None):
        self._edges = _no_edges | _to_edge_dict(*edges)
        if any(x.endswith(".") for x in edges if isinstance(x, str)):
            del self._edges[EdgeCategory.Meta]
        self._conds = []
        self._is_optional = False
        self._auto_exc = False
        self._subtemplate = None

    def __invert__(self) -> N:
        """
        This node is connected to outer exception handler if one exists. An outer exception handler node will be automatically added to the template.
        """
        self._edges[EdgeCategory.Exception] = OptExcEdge(_AUTO_EXC)
        self._auto_exc = True
        return self

    def __pos__(self) -> N:
        """
        This node raises an exception to either an outer exception handler, or out of the codeobject. An outer exception handler node will be automatically added to the template.
        """
        self._edges[EdgeCategory.Exception] = RaiseOutEdge(_AUTO_EXC)
        if EdgeCategory.Meta in self._edges:
            del self._edges[EdgeCategory.Meta]
        self._auto_exc = True
        return self

    @staticmethod
    def tail() -> N:
        """
        Create a node and do not check any out edges from it.
        """
        x = N()
        x._edges = {}
        return x

    def optional(self) -> N:
        """
        The node is optional.
        """
        self._is_optional = True
        return self

    def with_in_deg(self, n: int, *n2: int) -> N:
        """
        The node must have in-degree `n` or any of the in-degrees in `n2`.
        """
        if not n2:
            self._conds.append(has_in_degree(n))
        else:
            self._conds.append(lambda cfg, node: node is not None and cfg.in_degree(node) in (n, *n2))
        return self

    def of_type(self, *template_type: type[ControlFlowTemplate]) -> N:
        """
        The node must be any template in `template_type`.
        """
        self._conds.append(has_type(*template_type))
        return self

    def of_subtemplate(self, template_type: type[ControlFlowTemplate]) -> N:
        """
        When matching a node, first try to match `template_type` rooted at the node, and only accept if the template successfully matched.
        """
        self._subtemplate = template_type
        return self

    def with_cond(self, cond: NodeCondition, *or_conds: NodeCondition) -> N:
        """
        The node must match `cond` or any of the conditions in `or_conds`.
        """
        if not or_conds:
            self._conds.append(cond)
        else:
            self._conds.append(lambda cfg, node: any(f(cfg, node) for f in (cond, *or_conds)))
        return self

    def __or__(self, o: N) -> N:
        """
        Match either this node or the other node.
        """
        return _Ns(self, o)

    def _all_conds(self, cfg: CFG, node: ControlFlowTemplate | None) -> bool:
        return all(c(cfg, node) for c in self._conds)

    def _build(self, name: str) -> NodeMatcher:
        x = NodeTemplate(self._edges)
        x.name = name
        if self._subtemplate:
            x = SubtemplateNodeMatcher(x, self._subtemplate)
            name += ".subtemplate"
            x.name = name
        if len(self._conds) == 1:
            x = ConditionalNodeMatcher(x, self._conds[0])
            name += ".condition"
            x.name = name
        elif self._conds:
            x = ConditionalNodeMatcher(x, self._all_conds)
            name += ".condition"
            x.name = name
        if self._is_optional:
            x = OptionalNodeMatcher(x)
            name += ".optional"
            x.name = name
        return x


class _Ns(N):
    def __init__(self, a: N, b: N):
        self.nodes = [a, b]

    @override
    def _build(self, name) -> NodeMatcher:
        return AnyNodeMatcher(*(x._build(name + ".any") for x in self.nodes))

    @override
    def optional(self) -> N:
        for node in self.nodes:
            node._is_optional = True
        return self

    @override
    def with_in_deg(self, n: int, *n2: int) -> N:
        self.nodes = [node.with_in_deg(n, *n2) for node in self.nodes]
        return self

    @override
    def of_type(self, *template_type: type[ControlFlowTemplate]) -> N:
        self.nodes = [n.of_type(*template_type) for n in self.nodes]
        return self

    @override
    def with_cond(self, cond: NodeCondition, *or_conds: NodeCondition) -> N:
        self.nodes = [n.with_cond(cond, *or_conds) for n in self.nodes]
        return self

    @override
    def __or__(self, o: N) -> N:
        if isinstance(o, _Ns):
            self.nodes.extend(o.nodes)
        else:
            self.nodes.append(o)
        return self


class E:
    """
    Namespace for edge convenience functions.
    """

    @staticmethod
    def _(x: str | None) -> EdgeMatcher:
        if x is None:
            return no_edge
        if x[-1] == "?":
            return OptionalEdge(x[:-1])
        if x[-1] == ".":
            return ExitableEdge(x[:-1])
        if x[-1] == "^":
            return RaiseOutEdge(x[:-1])
        return EdgeTemplate(x)

    @staticmethod
    def nat(n: str | None):
        return (EdgeCategory.Natural, E._(n))

    @staticmethod
    def cond(n: str | None):
        return (EdgeCategory.Conditional, E._(n))

    @staticmethod
    def exc(n: str | None):
        return (EdgeCategory.Exception, E._(n))

    @staticmethod
    def meta(n: str | None):
        return (EdgeCategory.Meta, E._(n))


def remove_nodes(cfg: CFG, mapping: dict[str, ControlFlowTemplate | None], *nodes: str):
    cfg.remove_nodes_from(filter(None, (mapping.get(n) for n in nodes if mapping.get(n))))


def _line(line: str) -> Callable[[ControlFlowTemplate, SourceContext], list[SourceLine]]:
    x = line.lstrip(" ")
    indent = (len(line) - len(x)) // 4
    if x[0] == "{":
        end = x.index("}")
        t = x[1:end]
        if "?" in t:
            s = t[t.index("?") + 1 :]
            t = t[: t.index("?")]
            return partial(lambda self, source, indent, t, s: self.line(s, indent) if self.members[t] is not None and source[self.members[t], indent] else [], indent=indent, t=t, s=s)
        return partial(lambda self, source, indent, t: source[self.members[t], indent] if self.members[t] is not None else [], indent=indent, t=t)
    return lambda self, source: self.line(x, indent)


def to_indented_source(f: Callable[[], None]):
    """
    "Compile" a function's docstring into an indented source function
    Indentation must be 4 spaces
    """
    assert f.__doc__ is not None and "\t" not in f.__doc__
    src = [_line(x) for x in textwrap.dedent(f.__doc__).strip().split("\n")]

    def to_indented_source(self: ControlFlowTemplate, source: SourceContext) -> list[SourceLine]:
        return list(chain.from_iterable(x(self, source) for x in src))

    return to_indented_source


def defer_source_to(n: str):
    def to_indented_source(self: ControlFlowTemplate, source: SourceContext) -> list[SourceLine]:
        node = self.members[n]
        if node is None:
            return []
        return source[node]

    return to_indented_source


def condense_mapping(
    cls: type[C], cfg: CFG, mapping: dict[str, ControlFlowTemplate | None], *nodes: str, in_edges: dict[ControlFlowTemplate, dict] | None = None, out_edges: dict[ControlFlowTemplate, dict] | None = None, out_filter: list[EdgeCategory] = []
) -> C:
    in_template = {x: mapping.get(x) for x in nodes}
    template = cls(in_template)

    if in_edges is None:
        in_edges = {src: prop for n in reversed(in_template.values()) for src, _, prop in cfg.in_edges(n, data=True) if src not in in_template.values() and n is not None}
    if out_edges is None:
        out_edges = {dst: prop for n in reversed(in_template.values()) for _, dst, prop in cfg.out_edges(n, data=True) if dst not in in_template.values() and n is not None}
    if cfg.end in out_edges:
        out_edges[cfg.end] = EdgeKind.Meta.prop()
    if not out_edges:
        out_edges[cfg.end] = EdgeKind.Meta.prop()
    if out_filter:
        out_edges = {k: v for k, v in out_edges.items() if EdgeCategory.from_kind(v["kind"]) not in out_filter}
    remove_nodes(cfg, mapping, *in_template)
    cfg.add_node(template)
    cfg.add_edges_from((src, template, prop) for src, prop in in_edges.items())
    cfg.add_edges_from((template, dst, prop) for dst, prop in out_edges.items())
    cfg.iterate()
    return template


def make_try_match(out_edges: dict[EdgeKind, str], *nodes: str):
    """
    Make a `try_match` method for a `ControlFlowTemplate`.
    Matches `cls.template`, condenses all nodes in `nodes`, and creates a new node.
    """

    @classmethod
    @override
    def try_match(cls: type[ControlFlowTemplate], cfg: CFG, node: ControlFlowTemplate) -> ControlFlowTemplate | None:
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            return None
        edges: dict[ControlFlowTemplate, dict] = {mapping[name]: kind.prop() for kind, name in out_edges.items() if mapping.get(name) is not None}  # type: ignore
        if mapping.get(_AUTO_EXC) is not None and all(e["kind"] != EdgeKind.Exception for e in edges.values()):
            edges[mapping[_AUTO_EXC]] = EdgeKind.Exception.prop()  # type: ignore
        return condense_mapping(cls, cfg, mapping, *nodes, out_edges=edges)

    return try_match


def revert_on_fail(f: Callable[[type[ControlFlowTemplate], CFG, ControlFlowTemplate], ControlFlowTemplate | None] | classmethod):
    """
    Make a `ControlFlowTemplate`'s `try_match` method restore the CFG to before the method call if the match fails.
    """
    if isinstance(f, classmethod):
        f = f.__func__

    @classmethod
    @override
    def try_match(cls: type[ControlFlowTemplate], cfg: CFG, node: ControlFlowTemplate) -> ControlFlowTemplate | None:
        copy = cfg.copy()
        if (ret := f(cls, cfg, node)) is not None:
            return ret
        cfg.clear()
        cfg.update(copy)

    return try_match


def _check_break_condition(cfg: CFG, node: ControlFlowTemplate | None, offset: int | None, i: int | None, name: str | None):
    if offset is not None and (not node or node.offset != offset):
        return False
    if i is not None and cfg.i != i:
        return False
    if name is not None and cfg.bytecode.name != name:
        return False
    return True


def _hook(f, offset, i, name):
    def hooked(cfg: CFG, node: ControlFlowTemplate | None):
        if _check_break_condition(cfg, node, offset, i, name):
            p = pdb.Pdb()
            p.quitting = False
            p.botframe = None
            p.stopframe = None
            print(f"{cfg.i = }\n{cfg.bytecode.name = }\nnode.offset = {node and node.offset}\n{node = }")
            sys.settrace(p.trace_dispatch)
        return f(cfg, node)

    return hooked


def hook_template(offset: int | None = None, i: int | None = None, name: str | None = None):
    """
    Hook a `ControlFlowTemplate`'s `try_match` method to set a breakpoint before running when certain conditions are met.
    """

    def deco(template: type[C]):
        template.try_match = _hook(template.try_match, offset, i, name)
        return template

    return deco


def hook_node(node: str, offset: int | None = None, i: int | None = None, name: str | None = None):
    """
    In this `ControlFlowTemplate`, hook the node named `node`'s `try_match` method to set a breakpoint before running when certain conditions are met.
    """

    def deco(template: type[C]):
        template.template.nodes[node].try_match = _hook(template.template.nodes[node].try_match, offset, i, name)
        return template

    return deco


def versions_above(major: int, minor: int):
    return (x.as_tuple() for x in supported_versions if x > (major, minor))


def versions_from(major: int, minor: int):
    return (x.as_tuple() for x in supported_versions if x >= (major, minor))


def versions_below(major: int, minor: int):
    return (x.as_tuple() for x in supported_versions if x < (major, minor))


def versions_until(major: int, minor: int):
    return (x.as_tuple() for x in supported_versions if x <= (major, minor))


def versions_except(*versions: tuple[int, int]):
    return (x.as_tuple() for x in supported_versions if x not in versions)
