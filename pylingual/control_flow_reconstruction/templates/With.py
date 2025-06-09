from typing import override
from ..cft import ControlFlowTemplate, EdgeKind, register_template
from ..utils import T, N, exact_instructions, starting_instructions, to_indented_source, make_try_match, versions_from


class WithCleanup3_12(ControlFlowTemplate):
    template = T(
        start=N("reraise", "poptop", "exc").with_cond(
            exact_instructions("PUSH_EXC_INFO", "WITH_EXCEPT_START", "POP_JUMP_IF_TRUE"),  # 3.12
            exact_instructions("PUSH_EXC_INFO", "WITH_EXCEPT_START", "TO_BOOL", "POP_JUMP_IF_TRUE"),  # 3.13
        ),
        reraise=N(None, None, "exc").with_cond(exact_instructions("RERAISE")).with_in_deg(1),
        poptop=N("tail", None, "exc").with_cond(exact_instructions("POP_TOP")).with_in_deg(1),
        exc=+N().with_cond(exact_instructions("COPY", "POP_EXCEPT", "RERAISE")).with_in_deg(3),
        tail=~N.tail().with_cond(starting_instructions("POP_EXCEPT", "POP_TOP", "POP_TOP")).with_in_deg(1),
    )

    try_match = make_try_match({}, "start", "reraise", "poptop", "exc", "tail")

    @override
    def to_indented_source(self, source):
        return []


@register_template(0, 10, *versions_from(3, 12))
class With3_12(ControlFlowTemplate):
    template = T(
        setup_with=~N("with_body", None),
        with_body=N("normal_cleanup", None, "exc_cleanup").with_in_deg(1),
        exc_cleanup=N.tail().of_subtemplate(WithCleanup3_12).with_in_deg(1),
        normal_cleanup=~N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "normal_cleanup"}, "setup_with", "with_body", "exc_cleanup")

    @to_indented_source
    def to_indented_source():
        """
        {setup_with}
            {with_body}
        """

class WithCleanup3_9(ControlFlowTemplate):
    template = T(
        start=~N("reraise", "poptop").with_cond(
            starting_instructions("WITH_EXCEPT_START"),  # 3.9 & 3.10
        ),
        reraise=+N().with_cond(exact_instructions("RERAISE")).with_in_deg(1),
        poptop=~N("tail.", None).with_cond(starting_instructions("POP_TOP")).with_in_deg(1),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "start", "reraise", "poptop")

    @override
    def to_indented_source(self, source):
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

@register_template(0, 10, (3, 8))
class With3_8(ControlFlowTemplate):
    template = T(
        setup_with=~N("with_body", None),
        with_body=N("begin_finally.", None, "normal_cleanup").with_in_deg(1),
        begin_finally=~N("normal_cleanup.", None).with_in_deg(1),
        normal_cleanup=~N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "normal_cleanup"}, "setup_with", "with_body", "begin_finally")

    @to_indented_source
    def to_indented_source():
        """
        {setup_with}
            {with_body}
        """