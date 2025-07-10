from __future__ import annotations
from typing import TYPE_CHECKING
from ..cft import ControlFlowTemplate, EdgeKind, register_template
from ..utils import (
    T,
    N,
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
        