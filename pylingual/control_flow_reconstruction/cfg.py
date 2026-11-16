from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, override

import networkx as nx

from pylingual.editable_bytecode import EditableBytecode, Inst
from .cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, MetaTemplate, indent_str, out_edge_dict
from .source import SourceContext, SourceLine

if TYPE_CHECKING:
    DiGraph_CFT = nx.DiGraph[ControlFlowTemplate]
else:
    DiGraph_CFT = nx.DiGraph


class CFG(DiGraph_CFT):
    """Control flow graph of a code object's instructions, merged into basic blocks, which the equivalence check compares."""

    start: ControlFlowTemplate
    end: ControlFlowTemplate

    @staticmethod
    def from_graph(cfg: nx.DiGraph, bytecode: EditableBytecode) -> CFG:
        self = CFG(cfg)
        self.start = MetaTemplate("start", bytecode.codeobj)
        self.end = MetaTemplate("end", bytecode.codeobj)

        InstTemplate.match_all(self)
        for _a, _b, _p in self.edges(data=True):
            self[_a][_b]["kind"] = EdgeKind(_p["type"])

        root_node = min([x for x in self.nodes], key=lambda x: x.get_instructions()[0].offset)
        self.add_nodes_from([self.start, self.end])
        self.add_edge(self.start, root_node, kind=EdgeKind.Meta)
        self.add_edges_from((node, self.end, EdgeKind.Meta.prop()) for node in self.nodes if isinstance(node, InstTemplate) and self.out_degree(node) == 0)

        BlockTemplate.match_all(self)
        return self


# basic blocks: the equivalence check compares code objects block by block
class BlockTemplate(ControlFlowTemplate):
    members: list[ControlFlowTemplate]

    def __init__(self, members: list[ControlFlowTemplate]):
        self.members = members  # type: ignore
        self.offset = members[0].offset if members else -1
        self.header_lines = []
        self.blame = members[0].blame

    @staticmethod
    def match_all(cfg: CFG):
        for node in list(cfg.nodes):
            if isinstance(node, MetaTemplate) or node not in cfg.nodes:
                continue
            BlockTemplate.try_match(cfg, node)

    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        members: list[ControlFlowTemplate] = []
        out = out_edge_dict(cfg, node)
        exc = out[EdgeCategory.Exception]
        current = node
        while True:
            if out[EdgeCategory.Exception] != exc:
                break
            if current != node and cfg.in_degree(current) > 1:  # type: ignore
                break
            if current in members:
                break
            members.append(current)
            next = out[EdgeCategory.Natural]
            if next is None:
                break
            if cfg.get_edge_data(current, next).get("kind") != EdgeKind.Fall:
                break
            if out[EdgeCategory.Conditional] is not None:
                break
            out = out_edge_dict(cfg, next)
            current = next
        if len(members) < 2:
            return None
        template = BlockTemplate([x for m in members for x in (m.members if isinstance(m, BlockTemplate) else [m])])
        in_edges = [(src, template, prop) for src, _, prop in cfg.in_edges(node, data=True) if src not in members]
        out_edges = [(template, template, prop) if dst in members else (template, dst, prop) for _, dst, prop in cfg.out_edges(members[-1], data=True)]
        cfg.remove_nodes_from(members)
        cfg.add_node(template)
        cfg.add_edges_from(chain(in_edges, out_edges))
        return template

    @override
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        return list(chain.from_iterable(source[m] for m in self.members))

    @override
    def get_instructions(self) -> list[Inst]:
        insts: list[Inst] = []
        for member in self.members:
            insts.extend(member.get_instructions())
        return insts

    @override
    def __repr__(self) -> str:
        components = indent_str("\n".join(repr(member) for member in self.members))
        return f"BlockTemplate[\n{components}]"
