from __future__ import annotations
from itertools import chain
from typing import TYPE_CHECKING, override

from pylingual.control_flow_reconstruction.source import SourceContext, SourceLine

from .Block import BlockTemplate, LoopElse
from ..cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, register_template, out_edge_dict
from ..utils import (
    T,
    N,
    is_not_type,
    no_back_edges,
    versions_below,
    versions_until,
    versions_except,
    versions_from,
    ending_instructions,
    has_no_lines,
    condense_mapping,
    defer_source_to,
    starting_instructions,
    to_indented_source,
    make_try_match,
    with_top_level_instructions,
    without_top_level_instructions,
)

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG



@register_template(0, 1, *versions_below(3, 14))
class ForLoop(ControlFlowTemplate):
    template = T(
        for_iter=~N("for_body", "tail"),
        for_body=~N("for_iter").with_in_deg(1),
        tail=N.tail().with_cond(is_not_type(LoopElse)),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "for_iter", "for_body")

    @to_indented_source
    def to_indented_source():
        """
        {for_iter}
            {for_body}
        """

@register_template(0, 1, *versions_from(3, 14))
class ForLoop3_14(ControlFlowTemplate):
    template = T(
        for_iter=~N("for_body", "tail").with_cond(with_top_level_instructions("FOR_ITER")),
        for_body=~N("for_iter").with_in_deg(1),
        tail=N.tail().with_cond(is_not_type(LoopElse)),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "for_iter", "for_body")

    @to_indented_source
    def to_indented_source():
        """
        {for_iter}
            {for_body}
        """


@register_template(0, 1)
class ForElseLoop(ControlFlowTemplate):
    template = T(
        for_iter=~N("for_body", "else_body").with_cond(with_top_level_instructions("FOR_ITER")),
        for_body=~N("for_iter").with_in_deg(1),
        else_body=~N("tail.").of_type(LoopElse),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "for_iter", "for_body", "else_body")

    @to_indented_source
    def to_indented_source():
        """
        {for_iter}
            {for_body}
        else:
            {else_body}
        """


@register_template(0, 2)
class LoopedReturn(ControlFlowTemplate):
    template = T(
        for_iter=~N("for_body", "tail").with_cond(ending_instructions("FOR_ITER")),
        for_body=~N.tail().with_in_deg(1).with_cond(ending_instructions("RETURN_CONST"),ending_instructions("RETURN_VALUE")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "for_iter", "for_body")

    @to_indented_source
    def to_indented_source():
        """
        {for_iter}
            {for_body}
        """

@register_template(0, 2, *versions_except((3, 10), (3, 11), (3, 12), (3, 13)))
class SelfLoop3_6(ControlFlowTemplate):
    template = T(
        loop_body=~N("loop_body", None)
    )

    try_match = make_try_match({}, "loop_body")

    @to_indented_source
    def to_indented_source():
        """
        while True:
            {loop_body}
        """


@register_template(0, 2, *versions_from(3, 10))
class SelfLoop3_10(ControlFlowTemplate):
    template = T(
        loop_header=~N("loop_body", "RET_CONST?").with_cond(no_back_edges),
        loop_body=~N("loop_body", None),
        RET_CONST=N.tail(),
    )

    try_match = make_try_match({}, "loop_header", "loop_body", "RET_CONST")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        header = source[self.loop_header]
        body = source[self.loop_body, 1]
        if not any(source.lines[i.starts_line - 1].strip().startswith("while ") for i in self.loop_header.get_instructions() if i.starts_line is not None):
            return list(chain(header, self.line("while True:"), body))
        else:
            return list(chain(header, body))


def _is_break_jump(cfg, node) -> bool:
    """lone jump carrying a (sanitized) break line."""
    if not isinstance(node, InstTemplate) or node.inst.opname not in ("JUMP_ABSOLUTE", "JUMP_FORWARD", "BREAK_LOOP") or node.inst.starts_line is None:
        return False
    return not node.inst.source_line


@register_template(0, 1, *versions_until(3, 9))
class WhileTrueBreak3_8(ControlFlowTemplate):
    """`while true: ...; if c: break` with no loop header."""

    template = T(
        loop_body=~N("brk", "loop_body"),
        brk=N("tail").with_in_deg(1).with_cond(_is_break_jump),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "loop_body", "brk")

    @to_indented_source
    def to_indented_source():
        """
        while True:
            {loop_body}
                break
        """


@register_template(0, -1, (3, 6), (3, 7))
class MarkLoopElse3_6(ControlFlowTemplate):
    """mark a loop's POP_BLOCK-led exhaustion target as its else body."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if isinstance(node, LoopElse) or cfg.in_degree(node) != 1 or not starting_instructions("POP_BLOCK")(cfg, node) or has_no_lines(cfg, node):
            return None
        (pred, _, prop), = cfg.in_edges(node, data=True)
        if prop["kind"] is not EdgeKind.FalseJump or not (with_top_level_instructions("FOR_ITER")(cfg, pred) or cfg.is_loop_header(pred)):
            return None
        # no else if SETUP_LOOP targets the code right after POP_BLOCK
        pop = node.get_instructions()[0]
        after = [i for i in pop.bytecode if i.offset > pop.offset][:1]
        if after and any(i.opname == "SETUP_LOOP" and i.target is after[0] for i in pop.bytecode):
            return None
        return LoopElse.try_match(cfg, node)

    def to_indented_source(self, source):
        raise NotImplementedError


@register_template(0, -2, (3, 6), (3, 7))
class HandlerBreak3_6(ControlFlowTemplate):
    """break/continue in an except body: cut its edge so the handler doesn't seem to flow there."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if isinstance(node, (BreakTemplate, ContinueTemplate)) or not node.get_instructions():
            return None
        last = node.get_instructions()[-1]
        if last.opname not in ("BREAK_LOOP", "CONTINUE_LOOP") or last.starts_line is None:
            return None
        # inside a handler, and not breaking a loop that starts within that handler
        handlers = [h for h in cfg.nodes if h is not node and any(p["kind"] is EdgeKind.Exception for _, _, p in cfg.in_edges(h, data=True)) and cfg.dominates(h, node)]
        if not handlers or any(cfg.dominates(h, n) and cfg.dominates(n, node) and cfg.is_loop_header(n) for h in handlers for n in cfg.nodes):
            return None
        exc = out_edge_dict(cfg, node)[EdgeCategory.Exception]
        # can't raise, but sits in its test's handler region
        if exc is None and len(preds := list(cfg.predecessors(node))) == 1:
            exc = out_edge_dict(cfg, preds[0])[EdgeCategory.Exception]
        template = BreakTemplate if last.opname == "BREAK_LOOP" else ContinueTemplate
        return condense_mapping(template, cfg, {"child": node}, "child", out_edges={exc: EdgeKind.Exception.prop()} if exc is not None else {})

    def to_indented_source(self, source):
        raise NotImplementedError


def _is_cond(node) -> bool:
    insts = node.get_instructions()
    return bool(insts) and insts[-1].opname in ("POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE", "JUMP_IF_FALSE_OR_POP", "JUMP_IF_TRUE_OR_POP")


def _unthread(cfg, node, cont=None):
    """point a threaded back edge at the next test's continue."""
    if not _is_cond(node) or cfg.is_loop_header(node):
        return None
    out = {p["kind"]: (dst, p) for _, dst, p in cfg.out_edges(node, data=True)}
    nxt = out.get(EdgeKind.Fall, (None,))[0]
    back = [(dst, p) for k, (dst, p) in out.items() if k in (EdgeKind.TrueJump, EdgeKind.FalseJump) and cfg.dominates(dst, node)]
    # same line, so both tests are one condition
    if nxt is None or len(back) != 1 or not _is_cond(nxt) or cfg.in_degree(nxt) != 1 or any(i.starts_line is not None for i in nxt.get_instructions()):
        return None
    header, prop = back[0]
    exc = out_edge_dict(cfg, node)[EdgeCategory.Exception]
    if out_edge_dict(cfg, nxt)[EdgeCategory.Exception] is not exc:
        return None
    for c in cfg.successors(nxt):
        insts = c.get_instructions()
        if c is header or (cont is not None and c is not cont) or len(insts) != 1 or insts[0].opname != "JUMP_ABSOLUTE" or insts[0].starts_line is None:
            continue
        if (cont is None and cfg.in_degree(c) != 1) or [d for d in cfg.successors(c) if d is not exc] != [header]:
            continue
        cfg.remove_edge(node, header)
        cfg.add_edge(node, c, **prop)
        return c
    return None


@register_template(0, -2, (3, 7), (3, 8), (3, 9))
class UnthreadContinue3_7(ControlFlowTemplate):
    """undo a short-circuit test's jump threaded past the continue to the loop header."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        cont = _unthread(cfg, node)
        if cont is None:
            return None
        # earlier tests of the same condition
        while len(preds := list(cfg.predecessors(node))) == 1 and _unthread(cfg, preds[0], cont):
            node = preds[0]
        cfg.iterate()
        return cont

    def to_indented_source(self, source):
        raise NotImplementedError


@register_template(0, 1, (3, 6), (3, 7))
class WhileTrueOnce3_6(ControlFlowTemplate):
    """`while true: ...; break` with no back edge."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        insts = node.get_instructions()
        if not insts or insts[-1].opname != "SETUP_LOOP" or insts[-1].source_line:
            return None
        edges = {prop["kind"]: dst for _, dst, prop in cfg.out_edges(node, data=True)}
        body, end = edges.get(EdgeKind.Fall), edges.get(EdgeKind.Jump)
        if body is None or end is None or cfg.out_degree(node) != 2 or cfg.in_degree(body) != 1:
            return None
        last = body.members[-1] if isinstance(body, BlockTemplate) else body
        if not _is_break_jump(cfg, last) or list(cfg.successors(body)) != [end]:
            return None
        return condense_mapping(cls, cfg, {"setup": node, "body": body}, "setup", "body", out_edges={end: EdgeKind.Fall.prop()})

    @to_indented_source
    def to_indented_source():
        """
        {setup}
        while True:
            {body}
            break
        """


@register_template(0, 2)
class TrueSelfLoop(ControlFlowTemplate):
    template = T(loop_body=~N("tail.", "loop_body"), tail=N.tail())

    try_match = make_try_match(
        {
            EdgeKind.Fall: "tail",
        },
        "loop_body",
    )

    @to_indented_source
    def to_indented_source():
        """
        {loop_body}
        """


@register_template(0, 1, *versions_below(3, 10))
class WhileElse3_6(ControlFlowTemplate):
    template = T(
        while_header=~N("while_body", "else_body").with_cond(without_top_level_instructions("FOR_ITER")),
        while_body=~N("while_header").with_in_deg(1),
        else_body=~N("tail.").of_type(LoopElse),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "while_header", "while_body", "else_body")

    @to_indented_source
    def to_indented_source():
        """
        {while_header}
            {while_body}
        else:
            {else_body}
        """


@register_template(0, 1, (3, 10), (3, 11))
class WhileElse3_10(ControlFlowTemplate):
    template = T(
        while_header=~N("while_body", "else_body"),
        while_body=~N("else_body").of_type(TrueSelfLoop),
        else_body=~N("tail.").of_type(LoopElse),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "while_header", "while_body", "else_body")

    @to_indented_source
    def to_indented_source():
        """
        {while_header}
            {while_body}
        else:
            {else_body}
        """


@register_template(0, 1, *versions_from(3, 12))
class WhileElse3_12(ControlFlowTemplate):
    template = T(
        while_header=~N("while_body", "else_body"),
        while_body=~N("JUMP", "else_body"),
        JUMP=~N("while_body"),
        else_body=~N("tail.").of_type(LoopElse),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "while_header", "while_body", "else_body")

    @to_indented_source
    def to_indented_source():
        """
        {while_header}
            {while_body}
        else:
            {else_body}
        """


@register_template(0, 1, *versions_from(3, 12))
class AsyncForLoop3_12(ControlFlowTemplate):
    template = T(
        for_iter=N("for_body", None, "tail"),
        for_body=~N("for_iter").with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({}, "tail", "for_iter", "for_body")

    @to_indented_source
    def to_indented_source():
        """
        {for_iter}
            {for_body}
        {tail}
        """
        

@register_template(1, 39)
class WhileIfElseLoop(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        else_body=~N("if_header").with_in_deg(1),
        if_body=~N("tail.").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "if_header", "if_body", "else_body")

    @to_indented_source
    def to_indented_source():
        """
        while True:
            {if_header}
                {if_body}
            {else_body?else:}
                {else_body}
        """


@register_template(1, 39, *versions_from(3, 14))
class WhileLoop3_14(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER", "NOP")),
        else_body=~N("tail.").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1),
        if_body=~N("if_header").with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "if_header", "if_body", "else_body")

    @to_indented_source
    def to_indented_source():
        """
        {if_header}
            {if_body}
        {else_body?else:}
            {else_body}
        """


@register_template(1, 39, *versions_from(3, 14))
class WhileTrueLoop3_14(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")).with_cond(starting_instructions("NOP")),
        else_body=~N("tail.").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1),
        if_body=~N("if_header").with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "if_header", "if_body", "else_body")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        # a blank-line nop here is the break; the rest is after the loop
        exit_body, after = self.else_body, []
        members = exit_body.members if isinstance(exit_body, BlockTemplate) else [exit_body]
        first = members[0]
        if isinstance(first, InstTemplate) and first.inst.opname == "NOP" and first.inst.starts_line is not None and not source.lines[first.inst.starts_line - 1]:
            exit_body = first
            after = source[BlockTemplate(members[1:])] if len(members) > 1 else []
            body = self.line("break", 2)
        else:
            body = source[exit_body, 2]
        lines = list(chain(self.line("while True:"), source[self.if_header, 1], body))
        if source[self.if_body]:
            lines += self.line("else:", 1) + source[self.if_body, 2]
        return lines + after


@register_template(0, 3)
class InlinedComprehensionTemplate(ControlFlowTemplate):
    template = T(
        comp=N("tail", None, "cleanup"),
        cleanup=+N().with_in_deg(1).with_cond(starting_instructions("SWAP", "POP_TOP", "SWAP")),
        tail=~N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "tail",
        },
        "comp",
        "cleanup",
    )

    to_indented_source = defer_source_to("comp")


_HANDLER_EXIT_OPS = {"POP_TOP", "LOAD_CONST", "LOAD_SMALL_INT", "LOAD_COMMON_CONSTANT", "STORE_FAST", "STORE_NAME", "DELETE_FAST", "DELETE_NAME", "SWAP", "POP_ITER",
                     "RETURN_VALUE", "RETURN_CONST", "JUMP_ABSOLUTE", "JUMP_FORWARD", "JUMP_BACKWARD", "JUMP_BACKWARD_NO_INTERRUPT", "POP_BLOCK", "POP_EXCEPT"}


def _handler_exit(node) -> bool:
    """break/continue out of an except: a blank-lined POP_EXCEPT (POP_BLOCK; POP_EXCEPT before 3.11), then only cleanup and the jump/exit."""
    if not isinstance(node, (BlockTemplate, InstTemplate)):
        return False
    insts = node.get_instructions()
    for k, i in enumerate(insts):
        if i.opname in ("POP_EXCEPT", "POP_BLOCK") and i.starts_line is not None and not i.source_line:
            rest = insts[k + 1 :]
            if i.opname == "POP_BLOCK" and not any(j.opname == "POP_EXCEPT" for j in rest):
                return False
            return all(j.opname in _HANDLER_EXIT_OPS and j.starts_line is None for j in rest)
    return False


class BreakTemplate(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg, node):
        if _handler_exit(node):
            return condense_mapping(cls, cfg, {"child": node}, "child")
        break_candidates = {"POP_TOP", "LOAD_FAST", "LOAD_CONST", "LOAD_SMALL_INT", "LOAD_COMMON_CONSTANT", "RETURN_VALUE", "RETURN_CONST", "JUMP_ABSOLUTE", "JUMP_FORWARD", "JUMP_BACKWARD", "BREAK_LOOP", "POP_BLOCK", "POP_EXCEPT"}

        if not with_top_level_instructions(*break_candidates)(cfg, node) or has_no_lines(cfg, node):
            return None

        if isinstance(node, BlockTemplate):
            opcodes = list(x.inst for x in node.members if isinstance(x, InstTemplate))
        if isinstance(node, InstTemplate):
            opcodes = [node.inst]

        i = len(opcodes) - 1
        while i >= 0:
            instruction = opcodes[i].opname
            if instruction in break_candidates:
                if opcodes[i].starts_line is not None and not any(opcodes[i].source_line.strip().startswith(word) for word in {"pass", "...", "return"}):
                    return condense_mapping(cls, cfg, {"child": node}, "child")
                else:
                    i -= 1
                    continue
            else:
                return None
        return None

    def to_indented_source(self, source):
        lines = self.child.to_indented_source(source)
        # a handler's POP_EXCEPT already emits a (guessed) keyword; this template knows better
        if lines and lines[-1].line in ("break", "continue"):
            lines = lines[:-1]
        return lines + self.line("break")


class ContinueTemplate(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg, node):
        if _handler_exit(node):
            return condense_mapping(cls, cfg, {"child": node}, "child")
        continue_candidates = {"JUMP_ABSOLUTE", "JUMP_BACKWARD", "CONTINUE_LOOP", "POP_EXCEPT", "POP_BLOCK"}

        if not with_top_level_instructions(*continue_candidates)(cfg, node) or has_no_lines(cfg, node):
            return None
        
        if isinstance(node, BlockTemplate):
            opcodes = list(x.inst for x in node.members if isinstance(x, InstTemplate))
        if isinstance(node, InstTemplate):
            opcodes = [node.inst]
        
        i = len(opcodes) - 1
        while i >= 0:
            instruction = opcodes[i].opname
            if instruction in continue_candidates:
                if opcodes[i].starts_line is not None and not any(opcodes[i].source_line.strip().startswith(word) for word in {"pass", "...", "return"}):
                    return condense_mapping(cls, cfg, {"child": node}, "child")
                else:
                    i -= 1
                    continue
            else:
                return None
        return None

    def to_indented_source(self, source):
        lines = self.child.to_indented_source(source)
        # a handler's POP_EXCEPT already emits a (guessed) keyword; this template knows better
        if lines and lines[-1].line in ("break", "continue"):
            lines = lines[:-1]
        return lines + self.line("continue")


@register_template(0, 0)
class FixLoop(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg: CFG, node: ControlFlowTemplate) -> ControlFlowTemplate | None:
        # check that its a loop that we need to fix
        # find the end of the loop
        # find all nodes that belong to the loop
        # find nodes in loop that go to end
        # replace those edges with meta edges to the end
        # find nodes in loop that go to header
        # replace all but last of those edges with meta edge to end

        # a node is a loop header if there are back-edges to it
        # a latching node is a node with a back-edge to the loop header
        # a back-edge is an edge from any node that is dominated by this node
        back_edges = []
        for predecessor in cfg.predecessors(node):
            # A back edge exists if the predecessor is reachable from the node (node dominates predecessor)
            if cfg.dominates(node, predecessor):
                back_edges.append(predecessor)
                
        if not back_edges or all(n == node for n in back_edges) or with_top_level_instructions("SEND")(cfg, node):
            return None

        # Check if for loop
        for_loop = True
        if without_top_level_instructions("FOR_ITER")(cfg, node):
            for_loop = False

        edges_to_remove = []
        else_candidates = []
        else_node = None

        if for_loop:
            # For loops
            # Much simpler and loop header indicated by "FOR_ITER" in all versions

            # Candidate ends are the nodes that all break statements point to 
            # and where the loop would naturally end
            candidate_end = None

            # Get all nodes encompassed by the loop excluding source node and initial false jump
            loopnode = None
            for succ in cfg.successors(node):
                if cfg.get_edge_data(node, succ).get("kind") == EdgeKind.Fall:
                    loopnode = succ
                    break

            dfs_edges = cfg.dfs_labeled_edges_no_loop(source=loopnode)
            encompassed_nodes = [v for u, v, d in dfs_edges if d == "forward"]
            
            # Find the candidate end that break connects to
            for succ in cfg.successors(node):
                if cfg.get_edge_data(node, succ).get("kind") == EdgeKind.FalseJump and not any(n == node for n in cfg.successors(succ)):
                    candidate_end = succ
                    else_node = succ

                    # Candidate end is a buffer node, look further for another candidate end
                    if cfg.in_degree(candidate_end) == 1:
                        for ss in cfg.successors(candidate_end):
                            if cfg.get_edge_data(candidate_end, ss).get("kind") != EdgeKind.Exception:
                                candidate_end = ss
                                break

            # Add all edges that is connected to candidate end
            for succ in encompassed_nodes:
                if cfg.get_edge_data(succ, candidate_end) != None:
                    edges_to_remove.append((succ, candidate_end))

            # Matching Continue statements and removing edges to loop header
            for candidate in back_edges:
                cont_node = ContinueTemplate.try_match(cfg, candidate)
                if cont_node is not None and cfg.in_degree(node) > 2:
                    cfg.remove_edge(cont_node, node)

            # Matching Break statements and removing edges to loop header
            # Checking Else node candidates
            for pred, succ in edges_to_remove:
                break_node = BreakTemplate.try_match(cfg, pred)
                if break_node is not None:
                    cfg.remove_edge(break_node, succ)
                    if succ != else_node and else_node not in else_candidates:
                        else_candidates.append(else_node)
        else:
            # While loops
            # Contains an extraneous header block (sometimes) which contains the while <condition>: line
            # Harder to apply candidate end strategy due to inconsistent header blocks and false_jumps
            loop_header = cfg.start

            for candidate in cfg.predecessors(node):
                # Finding loop header as help to find Else node
                if candidate.offset < node.offset:
                    loop_header = candidate
                
                # Finding Continue statement candidates 
                for predecessor in cfg.predecessors(candidate):
                    if cfg.dominates(node, predecessor):
                        back_edges.append(predecessor)
            
            # Finding Else node candidate
            if loop_header is not cfg.start and without_top_level_instructions("SETUP_LOOP")(cfg, loop_header):
                # Version difference contains SETUP_LOOP
                for succ in cfg.successors(loop_header):
                    if succ != node and cfg.get_edge_data(loop_header, succ).get("kind") == EdgeKind.FalseJump:
                        else_node = succ
            else:
                for succ in cfg.successors(node):
                    if succ != node and cfg.get_edge_data(node, succ).get("kind") == EdgeKind.FalseJump:
                        else_node = succ
            
            # Matching Continue statements and removing edges to loop header
            for candidate in back_edges:
                cont_node = ContinueTemplate.try_match(cfg, candidate)
                if cont_node is not None:
                    if cfg.has_edge(cont_node, node):
                        cfg.remove_edge(cont_node, node)
                    if cfg.has_edge(cont_node, loop_header):
                        cfg.remove_edge(cont_node, loop_header)
                        
            # Finding all nodes encompassed by the loop excluding source node
            dfs_edges = cfg.dfs_labeled_edges_no_loop(source=node)
            candidates = [v for u, v, d in dfs_edges if d == "forward"][1:]

            # Edge case check: Check through all candidates ensure they are not nodes that have 
            # predecessors with only Exception edge types
            # successors with only Exception edge types
            for n in candidates:
                for s in cfg.successors(n):
                    if cfg.get_edge_data(n, s).get("kind") != EdgeKind.Exception and not all(cfg.get_edge_data(p, n).get("kind") == EdgeKind.Exception for p in cfg.predecessors(n)):
                        edges_to_remove.append((n, s))
            
            # Matching Break statements and removing edges to the candidate end if applicable
            for pred, succ in edges_to_remove:
                break_node = BreakTemplate.try_match(cfg, pred)
                if break_node is not None:
                    # Only remove edge if there are more than 2 incoming edges to avoid breaking other control flow structures
                    # (a break out of an except body is unambiguous: drop it unless that strands the target)
                    if cfg.in_degree(succ) > 2 or (_handler_exit(break_node.child) and cfg.in_degree(succ) > 1 and succ != cfg.end):
                        cfg.remove_edge(break_node, succ)
                    elif cfg.in_degree(succ) <= 2 and succ != cfg.end:
                        # Broken: conflicting cases where removing the edge would strand blocks
                        # but also match correctly to valid Break statement nodes
                        continue

                    # Finding Else node candidate
                    if succ != else_node and else_node not in else_candidates:
                        else_candidates.append(else_node)
                    if pred in else_candidates:
                        else_candidates.remove(pred)
                        else_node = None

        # Match Else node if applicable
        if else_node in else_candidates:
            LoopElse.try_match(cfg, else_node)

        cfg.iterate()
        return
