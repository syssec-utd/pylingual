from ..cft import ControlFlowTemplate, EdgeKind, MetaTemplate, register_template
from ..utils import E, T, N, defer_source_to, has_some_lines, run_is, has_no_lines, with_instructions, exact_instructions, has_instval, starting_instructions, to_indented_source, make_try_match, without_top_level_instructions, ending_instructions
from .Loop import BreakTemplate, ContinueTemplate

class EarlyRet(ControlFlowTemplate):
    template = T(
        pop_block=~N("early_ret", None).with_cond(ending_instructions("POP_BLOCK")).with_in_deg(1),
        early_ret=N(E.meta("end")).with_cond(ending_instructions("RETURN_VALUE")).with_cond(has_no_lines).with_in_deg(1),
        end=N(None).of_type(MetaTemplate),
    )
    
    try_match = make_try_match({EdgeKind.Meta: "end"}, "pop_block", "early_ret")

    to_indented_source = defer_source_to("pop_block")


@register_template(1, 40)
class IfElse(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=~N.tail().of_subtemplate(EarlyRet) | ~N(None).with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("tail.").with_in_deg(1),
        else_body=~N.tail().of_subtemplate(EarlyRet) | ~N("tail.").with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("tail.").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1) | ~N("tail").with_cond(has_some_lines).with_in_deg(1),
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


@register_template(1, 40)
class IfJumpElse(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=N(None).with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("JUMP").with_in_deg(1),
        JUMP=N("tail.").with_cond(has_no_lines).with_cond(exact_instructions("JUMP_FORWARD"), exact_instructions("JUMP_ABSOLUTE")),
        else_body=N("tail.").with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("tail").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1) | ~N("tail").with_cond(has_some_lines).with_in_deg(1),
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



@register_template(1, 40)
class IfElseJump(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=N(None).with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("tail").with_in_deg(1),
        else_body=N("tail.").with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("JUMP").with_in_deg(1),
        JUMP=N("tail.").with_cond(has_no_lines).with_cond(exact_instructions("JUMP_FORWARD"), exact_instructions("JUMP_ABSOLUTE")),
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


@register_template(1, 39, (3, 12), (3, 13))
class IfElseLoop(ControlFlowTemplate):
    template = T(
        if_header=~N("else_body", "if_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=~N("tail.").with_in_deg(1),
        else_body=~N("tail.").with_in_deg(1).with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_cond(has_no_lines),
        for_iter=N.tail().with_cond(with_instructions("FOR_ITER")),
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


@register_template(1, 41)
@register_template(2, 41)
class IfThen(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "tail").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER", "JUMP_IF_NOT_EXC_MATCH")),
        if_body=~N.tail().with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("tail").with_in_deg(1) | ~N("tail.").with_in_deg(1).with_cond(run_is(2)) | ~N.tail().with_in_deg(1).with_cond(exact_instructions("LOAD_CONST","RETURN_VALUE"), exact_instructions("POP_TOP", "LOAD_CONST","RETURN_VALUE")) | ~N.tail().with_in_deg(1).with_cond(ending_instructions("POP_TOP", "RERAISE")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "if_header", "if_body")

    @to_indented_source
    def to_indented_source():
        """
        {if_header}
            {if_body}
        """


@register_template(0, 39)
class Assertion(ControlFlowTemplate):
    template = T(
        assertion=~N("fail", "tail"),
        fail=+N().with_cond(starting_instructions("LOAD_ASSERTION_ERROR"), has_instval("LOAD_GLOBAL", argval="AssertionError")).with_cond(has_no_lines),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "assertion", "fail")

    to_indented_source = defer_source_to("assertion")


@register_template(1, 46)
class ShortCircuitAnd(ControlFlowTemplate):
    template = T(
        A=~N("B", "tail"),
        B=~N("body", "tail").with_in_deg(1).with_cond(has_no_lines),
        body=~N.tail(),
        tail=N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "body",
            EdgeKind.FalseJump: "tail",
        },
        "A",
        "B",
    )

    @to_indented_source
    def to_indented_source():
        """
        {A}
            {B}
        """


@register_template(1, 45)
class ShortCircuitOr(ControlFlowTemplate):
    template = T(
        A=~N("B", "body"),
        B=~N("body", "tail").with_in_deg(1),
        body=~N.tail(),
        tail=N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "body",
            EdgeKind.FalseJump: "tail",
        },
        "A",
        "B",
    )

    to_indented_source = defer_source_to("A")
