from __future__ import annotations
from typing import TYPE_CHECKING
from ..cft import ControlFlowTemplate, EdgeKind, register_template
from ..utils import (
    T,
    N,
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
        return condense_mapping(cls, cfg, {'child': node}, 'child')

    def to_indented_source(self, source):
        return self.child.to_indented_source(source) + self.line('break')

@register_template(0, 4)
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
            if cfg.has_edge(node, node):
                return None

        if not back_edges:
            return None
        
        nodes = []
        edges_to_remove = []

        for successor in list(cfg.successors(node)):
            if cfg.in_degree(successor) != 1:
                for predecessor in list(cfg.predecessors(successor)):
                    if predecessor != node:
                        nodes.append(predecessor)
                        edges_to_remove.append((predecessor, successor))

        valid = []
        for pred, succ in edges_to_remove:
            if cfg.get_edge_data(pred, succ).get("kind") != EdgeKind.Exception:
                cfg.remove_edge(pred, succ)
                valid.append((pred, succ))
                
        for pred in set(x for x, _ in valid):
            BreakTemplate.try_match(cfg, pred)
        cfg.iterate()
        return