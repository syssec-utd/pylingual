from __future__ import annotations
from itertools import chain
from typing import TYPE_CHECKING

from pylingual.control_flow_reconstruction.source import SourceContext, SourceLine

from .Block import BlockTemplate, LoopElse
from ..cft import ControlFlowTemplate, EdgeKind, InstTemplate, register_template
from ..utils import (
    T,
    N,
    is_not_type,
    no_back_edges,
    versions_below,
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



@register_template(0, 1)
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


@register_template(0, 1)
class ForElseLoop(ControlFlowTemplate):
    template = T(
        for_iter=~N("for_body", "else_body"),
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

@register_template(0, 2, *versions_below(3, 10))
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
        RET_CONST = source[self.RET_CONST]
        if not any(source.lines[i.starts_line - 1].strip().startswith("while ") for i in self.loop_header.get_instructions() if i.starts_line is not None):
            return list(chain(header, self.line("while True:"), body))
        else:
            return list(chain(header, body))


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


class BreakTemplate(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg, node):
        break_candidates = {"POP_TOP", "LOAD_FAST", "LOAD_CONST", "RETURN_VALUE", "RETURN_CONST", "JUMP_ABSOLUTE", "JUMP_FORWARD", "JUMP_BACKWARD", "BREAK_LOOP", "POP_BLOCK"}

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
        return self.child.to_indented_source(source) + self.line("break")


class ContinueTemplate(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg, node):
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
        return self.child.to_indented_source(source) + self.line("continue")


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

        # Get all nodes encompassed by the loop excluding source node and initial false jump
        loopnode = None
        for succ in cfg.successors(node):
            if cfg.get_edge_data(node, succ).get("kind") == EdgeKind.Fall:
                loopnode = succ
                break

        dfs_edges = cfg.dfs_labeled_edges_no_loop(source=loopnode)
        encompassed_nodes = [v for u, v, d in dfs_edges if d == "forward"]

        edges_to_remove = []

        # Find the candidate end that break connects to
        false_edge = None
        candidate_end = None
        for succ in cfg.successors(node):
            if cfg.get_edge_data(node, succ).get("kind") == EdgeKind.FalseJump and not any(n == node for n in cfg.successors(succ)):
                candidate_end = succ
                false_edge = succ

                # Candidate end is a buffer node
                if cfg.in_degree(candidate_end) == 1:
                    for ss in cfg.successors(candidate_end):
                        if cfg.get_edge_data(candidate_end, ss).get("kind") != EdgeKind.Exception:
                            candidate_end = ss
                            break

        if candidate_end == None:
            # While loops
            for candidate in back_edges:
                cont_node = ContinueTemplate.try_match(cfg, candidate)
                if cont_node is not None and not cfg.has_edge(node, cont_node):
                    cfg.remove_edge(cont_node, node)
            
            dfs_edges = cfg.dfs_labeled_edges_no_loop(source=node)
            candidates = [v for u, v, d in dfs_edges if d == "forward"][1:]

            for n in candidates:
                for s in cfg.successors(n):
                    if cfg.get_edge_data(n, s).get("kind") != EdgeKind.Exception and not all(cfg.get_edge_data(p, n).get("kind") == EdgeKind.Exception for p in cfg.predecessors(n)):
                        edges_to_remove.append((n, s))
            
            for pred, succ in edges_to_remove:
                break_node = BreakTemplate.try_match(cfg, pred)
                if break_node is not None and cfg.in_degree(succ) > 2:
                    cfg.remove_edge(break_node, succ)

        else:
            # For loops
            if encompassed_nodes is not None:
                for succ in encompassed_nodes:
                    if cfg.get_edge_data(succ, candidate_end) != None:
                        edges_to_remove.append((succ, candidate_end))

            for candidate in back_edges:
                cont_node = ContinueTemplate.try_match(cfg, candidate)
                if cont_node is not None and cfg.in_degree(node) > 2:
                    cfg.remove_edge(cont_node, node)

            for pred, succ in edges_to_remove:
                break_node = BreakTemplate.try_match(cfg, pred)
                if break_node is not None:
                    cfg.remove_edge(break_node, succ)
                    if succ != false_edge:
                        LoopElse.try_match(cfg, false_edge)

        cfg.iterate()
        return
