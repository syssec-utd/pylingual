from __future__ import annotations

from typing import TYPE_CHECKING, override
from itertools import chain
from pylingual.editable_bytecode import Inst

from ..cft import ControlFlowTemplate, EdgeKind, SourceContext, SourceLine, register_template, EdgeCategory, out_edge_dict, MetaTemplate, indent_str
from ..utils import E, N, T, defer_source_to, remove_nodes

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG


@register_template(100, 0)
class EndTemplate(ControlFlowTemplate):
    template = T(
        start=N(E.meta("body")).of_type(MetaTemplate),
        body=N(E.meta("end")),
        end=N.tail().of_type(MetaTemplate).with_in_deg(1),
    )

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if node is not cfg.start:
            return None
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            return None
        template = cls(mapping)
        remove_nodes(cfg, mapping, "start", "body", "end")
        cfg.add_node(template)
        cfg.start = template
        cfg.end = template
        return template

    to_indented_source = defer_source_to("body")


@register_template(0, 20)
@register_template(2, 20)
class BlockTemplate(ControlFlowTemplate):
    members: list[ControlFlowTemplate]

    def __init__(self, members: list[ControlFlowTemplate]):
        self.members = members  # type: ignore
        self.offset = members[0].offset if members else -1
        self._pos = sum((x._pos for x in members), start=[])
        self.header_lines = []
        self.blame = members[0].blame

    @staticmethod
    def match_all(cfg: CFG):
        it, cfg.iterate = cfg.iterate, lambda: None
        for node in list(cfg.nodes):
            if isinstance(node, MetaTemplate) or node not in cfg.nodes:
                continue
            BlockTemplate.try_match(cfg, node)
        cfg.iterate = it

    @override
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
            if cfg.get_edge_data(current, next).get("kind") != EdgeKind.Fall and cfg.run != 2:
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
        cfg.iterate()
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
