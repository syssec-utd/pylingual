from __future__ import annotations
from typing import TYPE_CHECKING
from ..cft import ControlFlowTemplate, EdgeKind, register_template
from ..utils import (
    T,
    N,
    with_instructions,
    exact_instructions,
    has_no_lines,
    condense_mapping,
    defer_source_to,
    starting_instructions,
    to_indented_source,
    make_try_match,
)

if TYPE_CHECKING:
    from pylingual.control_flow_reconstruction.cfg import CFG


@register_template(0, 1)
class ForLoop(ControlFlowTemplate):
    template = T(
        for_iter=~N("for_body", "tail"),
        for_body=~N("for_iter").with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "for_iter", "for_body")

    @to_indented_source
    def to_indented_source():
        """
        {for_iter}
            {for_body}
        """


@register_template(0, 2)
class SelfLoop(ControlFlowTemplate):
    template = T(loop_body=~N("loop_body", None))

    try_match = make_try_match({}, "loop_body")

    @to_indented_source
    def to_indented_source():
        """
        while True:
            {loop_body}
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
        if isinstance(node, BreakTemplate) or has_no_lines(cfg, node) or with_instructions("RAISE_VARARGS")(cfg, node):
            return None
        return condense_mapping(cls, cfg, {"child": node}, "child")

    def to_indented_source(self, source):
        return self.child.to_indented_source(source) + self.line("break")


class ContinueTemplate(ControlFlowTemplate):
    @classmethod
    def try_match(cls, cfg, node):
        if isinstance(node, ContinueTemplate) or has_no_lines(cfg, node):
            return None
        instruction = node.get_instructions()[-1].opname
        if instruction in {"JUMP_ABSOLUTE", "JUMP_BACKWARD", "CONTINUE_LOOP"} and (node.get_instructions()[-1].starts_line is not None or node.get_instructions()[-2].starts_line is not None):
            return condense_mapping(cls, cfg, {"child": node}, "child")
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

        if not back_edges:
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
        candidate_end = None
        for succ in cfg.successors(node):
            if cfg.get_edge_data(node, succ).get("kind") == EdgeKind.FalseJump and cfg.out_degree(succ) <= 1:
                candidate_end = succ

                # Candidate end is a buffer node
                if cfg.in_degree(candidate_end) == 1 and any(exact_instructions(*op)(cfg, candidate_end) for op in [("POP_BLOCK",), ("END_FOR",), ("END_FOR", "POP_TOP"), ("LOAD_CONST", "RETURN_VALUE")]):
                    for ss in cfg.successors(candidate_end):
                        if cfg.out_degree(ss) <= 1:
                            candidate_end = ss
                            break

        if encompassed_nodes is not None:
            for succ in encompassed_nodes:
                if cfg.get_edge_data(succ, candidate_end) != None:
                    edges_to_remove.append((succ, candidate_end))

        for pred, succ in edges_to_remove:
            break_node = BreakTemplate.try_match(cfg, pred)
            if break_node is not None:
                cfg.remove_edge(break_node, succ)

        for candidate in back_edges:
            cont_node = ContinueTemplate.try_match(cfg, candidate)
            if cont_node is not None and cfg.in_degree(node) > 2:
                cfg.remove_edge(cont_node, node)

        cfg.iterate()
        return
