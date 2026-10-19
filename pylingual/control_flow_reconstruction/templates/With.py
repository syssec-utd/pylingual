from ..cft import ControlFlowTemplate, EdgeKind, register_template
from ..utils import E, T, N, ending_instructions, exact_instructions, has_no_lines, with_instructions, starting_instructions, without_top_level_instructions, to_indented_source, make_try_match, versions_from


class WithCleanup3_11(ControlFlowTemplate):
    template = T(
        start=N("reraise", "poptop", "exc").with_cond(starting_instructions("PUSH_EXC_INFO", "WITH_EXCEPT_START")),
        reraise=N(None, None, "exc").with_cond(exact_instructions("RERAISE")).with_in_deg(1),
        poptop=N("pop_exc", None, "exc").with_cond(exact_instructions("POP_TOP")).with_in_deg(1),
        exc=+N().with_cond(exact_instructions("COPY", "POP_EXCEPT", "RERAISE")).with_in_deg(3),
        pop_exc=~N("tail.", None).with_cond(starting_instructions("POP_EXCEPT", "POP_TOP")).with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "start", "reraise", "poptop", "exc", "pop_exc")

    @to_indented_source
    def to_indented_source():
        """
        {pop_exc}
        """


@register_template(0, 9, *versions_from(3, 11))
class WithReturnExit3_11(ControlFlowTemplate):
    """A return in a nested with leaves through the inner exit call into the outer exits and the return"""

    template = T(
        exit=~N("ret").with_cond(has_no_lines).with_cond(ending_instructions("CALL", "POP_TOP")),
        ret=N(E.meta("end"), E.exc("ret_exc?")).with_in_deg(1).with_cond(has_no_lines).with_cond(with_instructions("CALL", "POP_TOP")).with_cond(ending_instructions("RETURN_VALUE"), ending_instructions("RETURN_CONST")),
        ret_exc=N.tail(),
        end=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Meta: "end"}, "exit", "ret")

    @to_indented_source
    def to_indented_source():
        """
        {exit}
        {ret}
        """


@register_template(0, 10, *versions_from(3, 11))
class With3_11(ControlFlowTemplate):
    template = T(
        setup_with=~N("with_body", None),
        with_body=N("normal_cleanup.", None, "exc_cleanup").with_in_deg(1),
        exc_cleanup=~N("tail.", None).of_subtemplate(WithCleanup3_11).with_in_deg(1),
        normal_cleanup=~N("tail.", None).with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "setup_with", "with_body", "exc_cleanup", "normal_cleanup")

    @to_indented_source
    def to_indented_source():
        """
        {setup_with}
            {with_body}
        {normal_cleanup}
        {exc_cleanup}
        """


class WithCleanup3_9(ControlFlowTemplate):
    template = T(
        start=~N("reraise", "poptop").with_cond(starting_instructions("WITH_EXCEPT_START")),
        reraise=+N().with_cond(exact_instructions("RERAISE")).with_in_deg(1),
        poptop=~N("tail.", None).with_cond(starting_instructions("POP_TOP")).with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "start", "reraise", "poptop")

    @to_indented_source
    def to_indented_source():
        """
        {poptop}
        """


@register_template(0, 10, (3, 9), (3, 10))
class With3_9(ControlFlowTemplate):
    template = T(
        setup_with=~N("with_body", None),
        with_body=N("normal_cleanup.", None, "exc_cleanup").with_in_deg(1),
        exc_cleanup=N.tail().of_subtemplate(WithCleanup3_9).with_in_deg(1),
        normal_cleanup=~N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "normal_cleanup"}, "setup_with", "with_body", "exc_cleanup")

    @to_indented_source
    def to_indented_source():
        """
        {setup_with}
            {with_body}
        {exc_cleanup}
        """


@register_template(0, 10, (3, 6), (3, 7), (3, 8))
class With3_6(ControlFlowTemplate):
    template = T(
        setup_with=~N("with_body", None).with_cond(without_top_level_instructions("SETUP_FINALLY", "SETUP_EXCEPT")),
        with_body=N("buffer_block.", None, "normal_cleanup").with_in_deg(1),
        buffer_block=~N("normal_cleanup.", None).with_in_deg(1),
        normal_cleanup=~N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "normal_cleanup"}, "setup_with", "with_body", "buffer_block")

    @to_indented_source
    def to_indented_source():
        """
        {setup_with}
            {with_body}
        """
