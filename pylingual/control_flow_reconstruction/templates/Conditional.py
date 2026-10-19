from .Block import BlockTemplate
from ..cft import ControlFlowTemplate, EdgeKind, InstTemplate, MetaTemplate, register_template
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
    condense_mapping,
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


def chained_compare_start(cfg, node):
    insts = node.get_instructions()[-4:] if node is not None else []
    return len(insts) == 4 and [x.opname for x in insts[:2]] == ["SWAP", "COPY"] and insts[2].opname in ("COMPARE_OP", "IS_OP", "CONTAINS_OP") and insts[3].opname == "POP_JUMP_IF_FALSE"


@register_template(0, 5, *versions_from(3, 12))
class ChainedCompare(ControlFlowTemplate):
    """A chained compare whose first compare's cleanup and second compare both lead to the same branch"""

    template = T(
        first=~N("second", "cleanup").with_cond(chained_compare_start),
        second=~N("second_nat", "second_cond").with_in_deg(1).with_cond(has_no_lines),
        cleanup=~N("target").with_in_deg(1).with_cond(exact_instructions("POP_TOP"), exact_instructions("POP_TOP", "JUMP_FORWARD")).with_cond(has_no_lines),
        second_nat=N.tail(),
        second_cond=N.tail(),
        target=N.tail(),
    )

    @classmethod
    def try_match(cls, cfg, node):
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            return None
        body, other, target = mapping["second_nat"], mapping["second_cond"], mapping["target"]
        # the second compare jumps over the cleanup into the body
        if body is not target and cfg.in_degree(body) == 1 and cfg.out_degree(body) == 1 and has_no_lines(cfg, body) and exact_instructions("JUMP_FORWARD")(cfg, body):
            mapping["jump"] = body
            body = next(cfg.successors(body))
        if target not in (body, other) or body is other:
            return None
        out_edges = {body: EdgeKind.Fall.prop(), other: cfg.get_edge_data(mapping["second"], other)}
        if mapping.get("_EXC") is not None:
            out_edges[mapping["_EXC"]] = EdgeKind.Exception.prop()
        return condense_mapping(cls, cfg, mapping, "first", "second", "cleanup", "jump", out_edges=out_edges)

    to_indented_source = defer_source_to("first")


@register_template(1, 40)
class IfElse(ControlFlowTemplate):
    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=~N.tail().of_subtemplate(EarlyRet) | ~N.tail().of_subtemplate(EarlyRetDuplicateBlocks) | ~N(None).with_in_deg(1).of_type(BreakTemplate, ContinueTemplate) | ~N("tail.").with_in_deg(1),
        else_body=~N.tail().of_subtemplate(EarlyRet)
        | ~N.tail().of_subtemplate(EarlyRetDuplicateBlocks) 
        | ~N("tail.").with_in_deg(1).of_type(BreakTemplate, ContinueTemplate)
        | ~N("tail.").with_cond(without_top_level_instructions("RERAISE", "END_FINALLY")).with_in_deg(1)
        | ~N("tail").with_cond(has_some_lines).with_in_deg(1),
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


def exits(cfg, node):
    return all(kind in (EdgeKind.Meta, EdgeKind.Exception) for _, _, kind in cfg.out_edges(node, data="kind"))


@register_template(1, 39, *versions_from(3, 11))
class IfElseSplitTail(ControlFlowTemplate):
    """An if body that jumps over an exiting else was merged with the code after the if; split it off again."""

    template = T(
        if_header=~N("if_body", "else_body").with_cond(without_top_level_instructions("WITH_EXCEPT_START", "CHECK_EXC_MATCH", "FOR_ITER")),
        if_body=N.tail().with_in_deg(1).of_type(BlockTemplate).with_cond(exits),
        else_body=N.tail().with_in_deg(1).with_cond(has_some_lines).with_cond(exits),
    )

    @classmethod
    def try_match(cls, cfg, node):
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            return None
        body, other = mapping["if_body"], mapping["else_body"]
        members = body.members
        for i, member in enumerate(members[:-1]):
            jumps = [x for x in member.get_instructions() if x.opname == "JUMP_FORWARD" and x.starts_line is None]
            first = members[i + 1].get_instructions()
            if first and any(x.target is first[0] and first[0].offset > other.offset for x in jumps):
                break
        else:
            return None
        head = members[: i + 1]
        rest = members[i + 1 :]
        head = head[0] if len(head) == 1 else BlockTemplate(head)
        rest = rest[0] if len(rest) == 1 else BlockTemplate(rest)
        in_edges = list(cfg.in_edges(body, data=True))
        out_edges = list(cfg.out_edges(body, data=True))
        cfg.remove_node(body)
        cfg.add_edges_from((src, head, prop) for src, _, prop in in_edges)
        cfg.add_edge(head, rest, kind=EdgeKind.Fall)
        cfg.add_edges_from((rest, dst, prop) for _, dst, prop in out_edges)
        cfg.add_edges_from((head, dst, prop) for _, dst, prop in out_edges if prop["kind"] is EdgeKind.Exception)
        return IfElse.try_match(cfg, node)


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
        if_body=~N.tail().of_subtemplate(EarlyRet) | ~N("tail.").with_in_deg(1),
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
        | ~N.tail().with_in_deg(1).with_cond(exact_instructions("LOAD_CONST", "RETURN_VALUE"), exact_instructions("POP_TOP", "LOAD_CONST", "RETURN_VALUE"), exact_instructions("LOAD_COMMON_CONSTANT", "RETURN_VALUE"), exact_instructions("POP_TOP", "LOAD_COMMON_CONSTANT", "RETURN_VALUE"))
        | ~N.tail().with_in_deg(1).with_cond(ending_instructions("POP_TOP", "RERAISE")),
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
