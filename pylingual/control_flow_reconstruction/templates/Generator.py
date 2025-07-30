from ..cft import ControlFlowTemplate, EdgeKind, MetaTemplate, register_template
from ..utils import E, T, N, defer_source_to, ending_instructions, exact_instructions, no_back_edges, to_indented_source, make_try_match


@register_template(0, 0)
class Await3_12(ControlFlowTemplate):
    template = T(
        awaited=N("SEND", None, "gen_cleanup").with_cond(no_back_edges),
        SEND=N("YIELD_VALUE", "JUMP_BACK_NO_INT", "gen_cleanup").with_in_deg(2).with_cond(exact_instructions("SEND")),
        YIELD_VALUE=N("JUMP_BACK_NO_INT", None, "CLEANUP_THROW").with_in_deg(1).with_cond(exact_instructions("YIELD_VALUE")),
        JUMP_BACK_NO_INT=N("SEND", None, "gen_cleanup").with_in_deg(2).with_cond(exact_instructions("JUMP_BACKWARD_NO_INTERRUPT")),
        CLEANUP_THROW=N("JUMP_BACK", None, "gen_cleanup").with_in_deg(1).with_cond(exact_instructions("CLEANUP_THROW")),
        JUMP_BACK=N("tail").with_in_deg(1).with_cond(exact_instructions("JUMP_BACKWARD"), exact_instructions("JUMP_BACKWARD_NO_INTERRUPT")),
        gen_cleanup=~N.tail(),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail", EdgeKind.Exception: "gen_cleanup"}, "awaited", "SEND", "YIELD_VALUE", "JUMP_BACK_NO_INT", "CLEANUP_THROW", "JUMP_BACK")

    to_indented_source = defer_source_to("awaited")


@register_template(0, 0)
class AwaitWith3_12(ControlFlowTemplate):
    template = T(
        awaited=~N("SEND", None).with_cond(no_back_edges),
        SEND=~N("YIELD_VALUE", "CLEANUP_THROW").with_in_deg(2).with_cond(exact_instructions("SEND")),
        YIELD_VALUE=N("JUMP_BACK_NO_INT", None, "CLEANUP_THROW").with_in_deg(1).with_cond(exact_instructions("YIELD_VALUE")),
        JUMP_BACK_NO_INT=~N("SEND", None).with_cond(exact_instructions("JUMP_BACKWARD_NO_INTERRUPT")),
        CLEANUP_THROW=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "CLEANUP_THROW"}, "awaited", "SEND", "YIELD_VALUE", "JUMP_BACK_NO_INT")

    to_indented_source = defer_source_to("awaited")


@register_template(0, 0)
class Generator3_12(ControlFlowTemplate):
    template = T(
        entry=N("body").with_cond(ending_instructions("RETURN_GENERATOR", "POP_TOP")),
        body=N(E.exc("gen_cleanup"), E.meta("end?")),
        gen_cleanup=N(E.meta("end")).with_cond(exact_instructions("CALL_INTRINSIC_1", "RERAISE")),
        end=N().of_type(MetaTemplate),
    )

    try_match = make_try_match({EdgeKind.Fall: "end"}, "entry", "body", "gen_cleanup")

    @to_indented_source
    def to_indented_source():
        """
        {entry}
        {body}
        """
