from __future__ import annotations

from typing import TYPE_CHECKING, override
from itertools import chain
from pylingual.editable_bytecode import Inst

import networkx as nx

from ..cft import ControlFlowTemplate, EdgeKind, SourceContext, SourceLine, register_template, EdgeCategory, out_edge_dict, MetaTemplate, indent_str
from ..utils import E, N, T, defer_source_to, no_self_edges, remove_nodes, versions_from, without_instructions, has_no_lines, exact_instructions, make_try_match

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


@register_template(3, 0)
class RemoveUnreachable(ControlFlowTemplate):
    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if node is not cfg.start:
            return None

        valid = list(nx.dfs_preorder_nodes(cfg, source=cfg.start))
        invalid = [n for n in cfg.nodes if n not in valid and has_no_lines(cfg, n)]
        if invalid:
            cfg.remove_nodes_from(invalid)
            return node


@register_template(0, 0, (3, 13))
class JumpTemplate(ControlFlowTemplate):
    template = T(
        body=~N("jump", None).with_cond(without_instructions("CLEANUP_THROW")),
        jump=N("tail", "block?")
        .with_cond(no_self_edges)
        .with_in_deg(1)
        .with_cond(
            exact_instructions("JUMP_BACKWARD_NO_INTERRUPT"),
            exact_instructions("POP_JUMP_IF_TRUE"),
            exact_instructions("JUMP_FORWARD"),
            exact_instructions("JUMP_BACKWARD"),
            exact_instructions("POP_JUMP_IF_NOT_NONE"),
            exact_instructions("POP_JUMP_IF_NONE"),
            exact_instructions("POP_JUMP_IF_FALSE"),
        ),
        block=N.tail(),
        tail=N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "tail",
            EdgeKind.TrueJump: "block",
        },
        "body",
        "jump",
    )

    to_indented_source = defer_source_to("body")


@register_template(0, 0, *versions_from(3, 11))
class NopTemplate(ControlFlowTemplate):
    template = T(
        body=~N("nop", None).with_cond(without_instructions("CLEANUP_THROW")),
        nop=N("tail", None).with_in_deg(1).with_cond(exact_instructions("NOP")).with_cond(has_no_lines),
        tail=N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "tail",
        },
        "body",
        "nop",
    )

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
