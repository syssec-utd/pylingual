from .Block import BlockTemplate
from ..cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, MetaTemplate, register_template, out_edge_dict
from ..utils import (
    E,
    T,
    N,
    defer_source_to,
    has_some_lines,
    run_is,
    has_no_lines,
    versions_from,
    with_instructions,
    exact_instructions,
    has_instval,
    starting_instructions,
    to_indented_source,
    make_try_match,
    without_instructions,
    without_top_level_instructions,
    ending_instructions,
    not_try_header,
)
from .Loop import BreakTemplate, ContinueTemplate


class EarlyRetDuplicateBlocks(ControlFlowTemplate):
    template = T(
        pop_block=~N("early_ret", None).with_in_deg(1),
        early_ret=N(E.meta("end")).with_cond(ending_instructions("RETURN_VALUE"), ending_instructions("RETURN_CONST")).with_cond(has_no_lines).with_in_deg(1),
        end=N(None).of_type(MetaTemplate),
    )

    try_match = make_try_match({EdgeKind.Meta: "end"}, "pop_block", "early_ret")

    to_indented_source = defer_source_to("pop_block")


class EarlyRet(ControlFlowTemplate):
    template = T(
        pop_block=~N("early_ret", None).with_cond(
            without_instructions("JUMP_BACKWARD_NO_INTERRUPT", "POP_JUMP_IF_TRUE", "JUMP_FORWARD", "JUMP_BACKWARD", "POP_JUMP_IF_NOT_NONE", "POP_JUMP_IF_NONE", "POP_JUMP_IF_FALSE", "YIELD_VALUE"),
        ).with_in_deg(1),
        early_ret=N(E.meta("end")).with_cond(ending_instructions("RETURN_VALUE"), ending_instructions("RETURN_CONST")).of_type(BlockTemplate, InstTemplate).with_cond(
            without_instructions("JUMP_BACKWARD_NO_INTERRUPT", "POP_JUMP_IF_TRUE", "JUMP_FORWARD", "JUMP_BACKWARD", "POP_JUMP_IF_NOT_NONE", "POP_JUMP_IF_NONE", "POP_JUMP_IF_FALSE", "LOAD_FAST"),
        ).with_in_deg(1),
        end=N(None).of_type(MetaTemplate),
    )

    try_match = make_try_match({EdgeKind.Meta: "end"}, "pop_block", "early_ret")

    @to_indented_source
    def to_indented_source():
        """
        {pop_block}
        {early_ret}
        """


def _handler_return(cfg, node) -> bool:
    """a return out of an except clause; it already left the handler's region."""
    return node is not None and cfg.out_degree(node) == 1 and starting_instructions("POP_EXCEPT")(cfg, node) and (ending_instructions("RETURN_VALUE")(cfg, node) or ending_instructions("RETURN_CONST")(cfg, node))


def _tail_in_if_body(cfg, m) -> bool:
    """the else exits and the tail is laid out before it or after the if body's cold code, so it continues the if body."""
    tail, body, other = m.get("tail"), m["if_body"], m["else_body"]
    if tail is None or other is None or cfg.in_degree(tail) != 1 or not has_some_lines(cfg, tail) or out_edge_dict(cfg, other)[EdgeCategory.Natural] is not None:
        return False
    # a real else branch, not a duplicated finally
    if body.offset > other.offset or not has_some_lines(cfg, other):
        return False
    if tail.offset < other.offset:
        return True
    after = max(i.offset for i in other.get_instructions())
    cold = [i.offset for i in body.get_instructions() if i.offset > after]
    return bool(cold) and min(cold) < tail.offset


@register_template(1, 40)
class IfElse(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=~N.tail().of_subtemplate(EarlyRet) | ~N.tail().of_subtemplate(EarlyRetDuplicateBlocks) | ~N(None).with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | N.tail().with_in_deg(1).with_cond(_handler_return).with_cond(has_some_lines) | ~N("tail.").with_in_deg(1).with_cond(not_try_header),
        else_body=~N.tail().of_subtemplate(EarlyRet)
        | ~N.tail().of_subtemplate(EarlyRetDuplicateBlocks) 
        | N.tail().with_in_deg(1).with_cond(_handler_return).with_cond(has_some_lines)
        | ~N("tail.").with_in_deg(1).of_type(BreakTemplate, ContinueTemplate)
        | ~N("tail.").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1)
        | ~N("tail").with_cond(has_some_lines).with_in_deg(1),
        tail=N.tail(),
    )

    # line-less arms that don't rejoin are a loop's bottom test
    try_match = make_try_match(
        {EdgeKind.Fall: "tail"},
        "if_header",
        "if_body",
        "else_body",
        check=lambda cfg, m: (has_some_lines(cfg, m["if_body"]) or has_some_lines(cfg, m["else_body"]) or (m.get("tail") is not None and not cfg.dominates(m["tail"], m["if_header"])))
        and not _tail_in_if_body(cfg, m),
    )

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


@register_template(1, 39, *versions_from(3, 12))
class IfElseLoop(ControlFlowTemplate):
    template = T(
        if_header=~N("else_body", "if_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        # a line-less return is the loop's bottom test
        if_body=~N("tail.").with_in_deg(1).with_cond(has_some_lines, lambda cfg, node: out_edge_dict(cfg, node)[EdgeCategory.Natural] is not None, ending_instructions("RAISE_VARARGS")),
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
        if_body=~N.tail().with_in_deg(1).of_type(BreakTemplate, ContinueTemplate)
        | ~N("tail").with_in_deg(1)
        | ~N("tail.").with_in_deg(1).with_cond(run_is(2))
        | ~N.tail().with_in_deg(1).with_cond(exact_instructions("LOAD_CONST", "RETURN_VALUE"), exact_instructions("POP_TOP", "LOAD_CONST", "RETURN_VALUE"))
        | ~N.tail().with_in_deg(1).with_cond(ending_instructions("POP_TOP", "RERAISE")),
        tail=N.tail(),
    )

    # a line-less return skipped by a back edge is the loop's exit test
    try_match = make_try_match(
        {EdgeKind.Fall: "tail"},
        "if_header",
        "if_body",
        check=lambda cfg, m: has_some_lines(cfg, m["if_body"]) or m.get("tail") is None or not cfg.dominates(m["tail"], m["if_header"]),
    )

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
        fail=+N().with_cond(starting_instructions("LOAD_ASSERTION_ERROR"),
                    has_instval("LOAD_GLOBAL", argval="AssertionError"),
                    has_instval("LOAD_COMMON_CONSTANT", argval=0),
                    has_instval("LOAD_COMMON_CONSTANT", argval=AssertionError)).with_cond(has_no_lines), # new argval added in 3.15
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
