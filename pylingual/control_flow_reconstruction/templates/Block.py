from __future__ import annotations

from typing import TYPE_CHECKING, override
from itertools import chain
from pylingual.editable_bytecode import Inst

import networkx as nx

from ..cft import ControlFlowTemplate, EdgeKind, InstTemplate, SourceContext, SourceLine, register_template, EdgeCategory, out_edge_dict, MetaTemplate, indent_str
from ..utils import not_try_header, E, N, T, condense_mapping, defer_source_to, no_self_edges, remove_nodes, versions_from, versions_until, without_instructions, has_no_lines, exact_instructions, make_try_match

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG


class LoopElse(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg, node):
        if has_no_lines(cfg, node):
            return None
        else:
            return condense_mapping(cls, cfg, {"child": node}, "child")

    def to_indented_source(self, source):
        return self.child.to_indented_source(source)


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


@register_template(0, 0, *versions_from(3, 12))
class JumpTemplate(ControlFlowTemplate):
    template = T(
        body=~N("jump", None).with_cond(without_instructions("CLEANUP_THROW")),
        jump=N("tail", "block?")
        .with_cond(has_no_lines)
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
            EdgeKind.Jump: "tail",
            EdgeKind.TrueJump: "block",
        },
        "body",
        "jump",
        # 3.14+ try bodies in loops jump back on their own
        check=lambda cfg, m: without_instructions("NOP")(cfg, m["tail"]) or (cfg.bytecode.version[:2] >= (3, 14) and out_edge_dict(cfg, m["body"])[EdgeCategory.Exception] is not None),
    )

    to_indented_source = defer_source_to("body")


_BLOCK_STACK_OPS = {"POP_BLOCK", "POP_EXCEPT", "END_FINALLY", "RERAISE", "BEGIN_FINALLY", "CALL_FINALLY", "POP_FINALLY"}


def _inst_key(node: ControlFlowTemplate) -> list[tuple[str, object]]:
    return [(i.opname, i.argval) for i in node.get_instructions()]


def _exits(cfg: CFG, node: ControlFlowTemplate) -> bool:
    return all(EdgeCategory.from_kind(p["kind"]) is EdgeCategory.Meta for _, _, p in cfg.out_edges(node, data=True))


@register_template(0, -20, (3, 10))
class MergeDuplicatedExit(ControlFlowTemplate):
    """3.10 copies a ternary statement's join into each arm; point the line-less copies at the one with lines."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if not has_no_lines(cfg, node) or not _exits(cfg, node) or cfg.in_degree(node) == 0:
            return None
        key = _inst_key(node)
        if not key or key[-1][0] not in ("RETURN_VALUE", "RETURN_CONST") or out_edge_dict(cfg, node)[EdgeCategory.Exception] is not None:
            return None
        # exits that close a block are not interchangeable
        if any(op in _BLOCK_STACK_OPS or op.startswith(("SETUP_", "WITH_")) for op, _ in key):
            return None
        for other in list(cfg.nodes):
            if other is node or has_no_lines(cfg, other) or not _exits(cfg, other) or out_edge_dict(cfg, other)[EdgeCategory.Exception] is not None:
                continue
            members = other.members if isinstance(other, BlockTemplate) else [other]
            if not all(isinstance(m, InstTemplate) for m in members) or len(members) < len(key):
                continue
            k = len(members) - len(key)
            if [(m.inst.opname, m.inst.argval) for m in members[k:]] != key:
                continue
            # copy must start with the ternary's POP_TOP, then a lined statement
            if members[k].inst.opname != "POP_TOP" or members[k].inst.starts_line is not None or len(members) < k + 2 or members[k + 1].inst.starts_line is None:
                continue
            preds = list(cfg.in_edges(node, data=True))
            if k == 0 and any(cfg.has_edge(src, other) for src, _, _ in preds):
                continue
            if k == 0:
                target = other
            else:
                head = BlockTemplate(members[:k]) if k > 1 else members[0]
                target = BlockTemplate(members[k:]) if len(key) > 1 else members[k]
                in_edges = list(cfg.in_edges(other, data=True))
                out_edges = list(cfg.out_edges(other, data=True))
                cfg.remove_node(other)
                cfg.add_edges_from((src if src is not other else head, head, prop) for src, _, prop in in_edges)
                cfg.add_edge(head, target, kind=EdgeKind.Fall)
                cfg.add_edges_from((target, dst, prop) for _, dst, prop in out_edges)
            cfg.remove_node(node)
            cfg.add_edges_from((src, target, prop) for src, _, prop in preds)
            cfg.iterate()
            return target
        return None


def _bare_return(cfg, node) -> bool:
    key = _inst_key(node)
    return bool(key) and key[-1][0] in ("RETURN_VALUE", "RETURN_CONST") and has_no_lines(cfg, node) and _exits(cfg, node) and cfg.in_degree(node) == 1


@register_template(0, -20, *versions_from(3, 11))
class MergeTryIfReturn3_11(ControlFlowTemplate):
    """an if ending a try at function end gets a line-less return per arm; keep one."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        exc = out_edge_dict(cfg, node)[EdgeCategory.Exception]
        if exc is None:
            return None
        succs = [dst for _, dst, p in cfg.out_edges(node, data=True) if EdgeCategory.from_kind(p["kind"]) is not EdgeCategory.Exception]
        if len(succs) != 2:
            return None
        for ret, body in (succs, succs[::-1]):
            if not _bare_return(cfg, ret) or cfg.in_degree(body) != 1 or out_edge_dict(cfg, body)[EdgeCategory.Exception] is not exc:
                continue
            body_out = [(dst, p) for _, dst, p in cfg.out_edges(body, data=True) if EdgeCategory.from_kind(p["kind"]) is not EdgeCategory.Exception]
            if len(body_out) != 1 or body_out[0][0] is ret or not _bare_return(cfg, body_out[0][0]) or _inst_key(body_out[0][0]) != _inst_key(ret):
                continue
            cfg.remove_node(body_out[0][0])
            cfg.add_edge(body, ret, **body_out[0][1])
            cfg.iterate()
            return ret
        return None


def _in_one_clause(cfg, nodes) -> bool:
    doms = [d for d in cfg.nodes if all(cfg.dominates(d, n) for n in nodes)]
    split = next((d for d in doms if all(cfg.dominates(o, d) for o in doms)), None)
    if split is None or any(i.opname in ("CHECK_EXC_MATCH", "JUMP_IF_NOT_EXC_MATCH") for i in split.get_instructions()):
        return False
    return any(EdgeCategory.from_kind(p["kind"]) is EdgeCategory.Exception for d in doms for _, _, p in cfg.in_edges(d, data=True))


@register_template(0, -20, *versions_from(3, 10))
class MergeHandlerReturn3_10(ControlFlowTemplate):
    """a try at function end returns after its body and again after its handler; keep one."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        key = _inst_key(node)
        # a constant return; a bare RETURN_VALUE returns whatever came before it
        if not key or not (key[-1][0] == "RETURN_CONST" or key[-1][0] == "RETURN_VALUE" and len(key) > 1 and key[-2][0] in ("LOAD_CONST", "LOAD_SMALL_INT", "LOAD_COMMON_CONSTANT")):
            return None
        if not has_no_lines(cfg, node) or not _exits(cfg, node):
            return None
        handlers = {h for t in cfg.nodes if (h := out_edge_dict(cfg, t)[EdgeCategory.Exception]) is not None}
        # handlers the body's copy is not in
        handlers = {h for h in handlers if not all(cfg.dominates(h, p) for p in cfg.predecessors(node))}
        for other in list(cfg.nodes):
            if other is node or _inst_key(other) != key or not has_no_lines(cfg, other) or not _exits(cfg, other):
                continue
            in_edges = list(cfg.in_edges(other, data=True))
            # every copy after a handler
            if not in_edges or not all(any(cfg.dominates(h, pred) for h in handlers) for pred, _, _ in in_edges):
                continue
            # handler footer copies must come from one except clause
            if ("POP_EXCEPT", None) in key and not _in_one_clause(cfg, [*cfg.predecessors(node), *(pred for pred, _, _ in in_edges)]):
                continue
            cfg.remove_node(other)
            cfg.add_edges_from((pred, node, prop) for pred, _, prop in in_edges)
            cfg.iterate()
            return node
        return None


_NON_RAISING_EXIT = {"POP_TOP", "LOAD_CONST", "RETURN_VALUE", "JUMP_ABSOLUTE", "JUMP_FORWARD"}
# a break/continue (blank line) out of a named handler also runs its cleanup
_HANDLER_CLEANUP = {"POP_EXCEPT", "STORE_FAST", "STORE_NAME", "DELETE_FAST", "DELETE_NAME"}


@register_template(0, -15, *versions_until(3, 10))
class MergePopBlock(ControlFlowTemplate):
    """join a break/continue/return's lined POP_BLOCK with the jump/exit after it."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        # a line-less POP_BLOCK is just the end of the try
        if not isinstance(node, InstTemplate) or node.inst.opname != "POP_BLOCK" or node.inst.starts_line is None:
            return None
        # blank is a break/continue
        line = node.inst.source_line.strip()
        if line and not line.startswith("return"):
            return None
        out = out_edge_dict(cfg, node)
        tail = out[EdgeCategory.Natural]
        if tail is None or out[EdgeCategory.Conditional] is not None or cfg.out_degree(node) != 1 + (out[EdgeCategory.Exception] is not None):
            return None
        if tail is node or cfg.in_degree(tail) != 1 or not has_no_lines(cfg, tail) or out_edge_dict(cfg, tail)[EdgeCategory.Exception] is not None:
            return None
        allowed = _NON_RAISING_EXIT | (_HANDLER_CLEANUP if not line else set())
        if not isinstance(tail, (InstTemplate, BlockTemplate)) or not all(i.opname in allowed for i in tail.get_instructions()):
            return None
        # must leave the try, not fall into the finally
        if tail.get_instructions()[-1].opname not in ("RETURN_VALUE", "JUMP_ABSOLUTE", "JUMP_FORWARD") or out[EdgeCategory.Exception] in cfg.successors(tail):
            return None
        members = [node, *(tail.members if isinstance(tail, BlockTemplate) else [tail])]
        template = BlockTemplate(members)
        in_edges = list(cfg.in_edges(node, data=True))
        out_edges = list(cfg.out_edges(tail, data=True))
        if out[EdgeCategory.Exception] is not None:
            out_edges.append((tail, out[EdgeCategory.Exception], EdgeKind.Exception.prop()))
        cfg.remove_nodes_from([node, tail])
        cfg.add_node(template)
        cfg.add_edges_from((src, template, prop) for src, _, prop in in_edges)
        cfg.add_edges_from((template, dst, prop) for _, dst, prop in out_edges)
        cfg.iterate()
        return template


def _bare_pop_block(cfg, node) -> bool:
    return isinstance(node, InstTemplate) and node.inst.opname == "POP_BLOCK" and node.inst.starts_line is None


@register_template(0, -15, (3, 10))
class MergePopBlockCopies3_10(ControlFlowTemplate):
    """each exit of a nested try pops the enclosing block; keep one copy."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if not _bare_pop_block(cfg, node):
            return None
        out = out_edge_dict(cfg, node)
        for other in list(cfg.nodes):
            if other is node or not _bare_pop_block(cfg, other) or cfg.in_degree(other) != 1 or out_edge_dict(cfg, other) != out or cfg.out_degree(other) != cfg.out_degree(node):
                continue
            (pred, _, prop), = cfg.in_edges(other, data=True)
            cfg.remove_node(other)
            cfg.add_edge(pred, node, **prop)
            cfg.iterate()
            return node
        return None


def _bare_jump(cfg, node) -> bool:
    return isinstance(node, InstTemplate) and node.inst.opname in ("JUMP_ABSOLUTE", "JUMP_FORWARD") and node.inst.starts_line is None and cfg.in_degree(node) == 1 and cfg.out_degree(node) == 1


@register_template(0, -15, (3, 10))
class MergeTryIfExit3_10(ControlFlowTemplate):
    """an if ending a try pops the block on each arm; share the body's exit jump."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if not isinstance(node, InstTemplate) or node.inst.opname != "POP_BLOCK" or node.inst.starts_line is not None or cfg.in_degree(node) != 1:
            return None
        out = out_edge_dict(cfg, node)
        jump = out[EdgeCategory.Natural]
        if jump is None or cfg.out_degree(node) != 1 + (out[EdgeCategory.Exception] is not None) or not _bare_jump(cfg, jump):
            return None
        (target,) = cfg.successors(jump)
        (src, _, prop), = cfg.in_edges(node, data=True)
        for other in list(cfg.predecessors(target)):
            if other is jump or not _bare_jump(cfg, other):
                continue
            (body,) = cfg.predecessors(other)
            # the other arm: popped the same block and branched from the same test
            if body.get_instructions()[-1].opname != "POP_BLOCK" or out_edge_dict(cfg, body)[EdgeCategory.Exception] is not out[EdgeCategory.Exception] or src not in cfg.predecessors(body):
                continue
            cfg.remove_nodes_from([node, jump])
            cfg.add_edge(src, other, **prop)
            cfg.iterate()
            return other
        return None


@register_template(0, -10, *versions_from(3, 11))
class ElideBranchNop(ControlFlowTemplate):
    """skip a line-less nop on a conditional branch."""

    @override
    @classmethod
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if not has_no_lines(cfg, node) or not all(i.opname in ("NOP", "NOT_TAKEN") for i in node.get_instructions()):
            return None
        if cfg.in_degree(node) != 1 or cfg.out_degree(node) != 1:
            return None
        (pred, _, in_prop), = cfg.in_edges(node, data=True)
        (_, succ, out_prop), = cfg.out_edges(node, data=True)
        if EdgeCategory.from_kind(in_prop["kind"]) is not EdgeCategory.Conditional or EdgeCategory.from_kind(out_prop["kind"]) is not EdgeCategory.Natural:
            return None
        if cfg.has_edge(pred, succ) or succ is node:
            return None
        # loop templates need the loop exit nop
        if cfg.is_loop_header(pred):
            return None
        cfg.remove_node(node)
        cfg.add_edge(pred, succ, **in_prop)
        cfg.iterate()
        return pred


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
        from .Loop import LoopElse
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
            if isinstance(current, LoopElse):
                break
            members.append(current)
            next = out[EdgeCategory.Natural]
            if next is None:
                break
            if cfg.get_edge_data(current, next).get("kind") != EdgeKind.Fall and cfg.run != 2:
                break
            if out[EdgeCategory.Conditional] is not None:
                break
            # a handler footer or finished statement ends before the next try's header
            if not not_try_header(cfg, next) and (not isinstance(current, (InstTemplate, BlockTemplate)) or members[0].get_instructions()[:1] and members[0].get_instructions()[0].opname == "POP_EXCEPT"):
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
