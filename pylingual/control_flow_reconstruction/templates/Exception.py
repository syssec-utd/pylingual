from itertools import chain
from typing import override

from .Block import BlockTemplate
from .Conditional import IfElse, IfThen
from ..cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, SourceLine, SourceContext, register_template
from ..utils import (
    E,
    N,
    T,
    condense_mapping,
    defer_source_to,
    with_instructions,
    ending_instructions,
    exact_instructions,
    no_back_edges,
    without_top_level_instructions,
    has_incoming_edge_of_categories,
    revert_on_fail,
    starting_instructions,
    to_indented_source,
    make_try_match,
    versions_from,
)

reraise = +N().with_cond(exact_instructions("COPY", "POP_EXCEPT", "RERAISE"))


class Except3_11(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if [x.opname for x in node.get_instructions()] == ["RERAISE"]:
            return node
        if x := ExceptExc3_11.try_match(cfg, node):
            return x
        if x := BareExcept3_11.try_match(cfg, node):
            return x


@register_template(0, 0, *versions_from(3, 11))
class Try3_11(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("tail.", None, "except_body"),
        except_body=N("tail.", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        reraise=reraise,
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "except_body",
            "reraise",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        """


@register_template(0, 0, *versions_from(3, 11))
class TryElse3_11(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("try_else.", None, "except_body"),
        except_body=N("tail.", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        try_else=~N("tail.").with_in_deg(1),
        reraise=reraise,
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "except_body",
            "try_else",
            "reraise",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        else:
            {try_else}
        """


class BareExcept3_11(Except3_11):
    template = T(
        except_body=N("except_footer.", None, "reraise").with_cond(without_top_level_instructions("RERAISE")),
        except_footer=~N("tail.").with_in_deg(1).with_cond(starting_instructions("POP_EXCEPT")),
        reraise=reraise,
        tail=N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "tail",
            EdgeKind.Exception: "reraise",
        },
        "except_body",
        "except_footer",
    )

    @to_indented_source
    def to_indented_source():
        """
        except:
            {except_body}
            {except_footer}
        """


class ExcBody3_11(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if x := NamedExc3_11.try_match(cfg, node):
            return x
        return node


class NamedExcTail3_11(ControlFlowTemplate):
    template = T(
        SWAP=N("tail", None, "reraise").with_cond(exact_instructions("SWAP")),
        reraise=reraise,
        tail=N.tail(),
    )

    @classmethod
    def _try_match(cls, cfg, node):
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            return None
        return condense_mapping(cls, cfg, mapping, "SWAP", "tail", out_filter=[EdgeCategory.Exception])

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if x := cls._try_match(cfg, node):
            return x
        return node

    to_indented_source = defer_source_to("tail")


class NamedExc3_11(ExcBody3_11):
    template = T(
        STORE=N("body", None, "reraise").with_cond(exact_instructions("STORE_FAST"), exact_instructions("STORE_NAME")),
        body=N("tail.", None, "cleanup"),
        cleanup=N(E.exc("reraise")).with_cond(exact_instructions("LOAD_CONST", "STORE_FAST", "DELETE_FAST", "RERAISE"), exact_instructions("LOAD_CONST", "STORE_NAME", "DELETE_NAME", "RERAISE")),
        reraise=reraise,
        tail=N.tail().of_subtemplate(NamedExcTail3_11),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail", EdgeKind.Exception: "reraise"}, "STORE", "body", "cleanup")

    to_indented_source = defer_source_to("body")


class ExceptExc3_11(Except3_11):
    template = T(
        except_header=N("except_body", "no_match", "reraise").with_cond(ending_instructions("CHECK_EXC_MATCH", "POP_JUMP_FORWARD_IF_FALSE"), ending_instructions("CHECK_EXC_MATCH", "POP_JUMP_IF_FALSE")),
        except_body=N("except_footer.", None, "reraise").of_subtemplate(ExcBody3_11).with_in_deg(1),
        no_match=N("tail?", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        except_footer=~N("tail.").with_in_deg(1).with_cond(starting_instructions("POP_EXCEPT")),
        reraise=reraise,
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
                EdgeKind.Exception: "reraise",
            },
            "except_header",
            "except_body",
            "except_footer",
            "no_match",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {except_header}
            {except_body}
            {except_footer}
        {no_match}
        """


@register_template(0, 50)
@register_template(2, 50)
class TryFinally3_11(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N(E.exc("reraise")).with_cond(ending_instructions("POP_TOP", "RERAISE")),
        reraise=reraise,
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_body", None, "fail_body").of_type(Try3_11, TryElse3_11),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N(E.exc("reraise")).with_cond(ending_instructions("POP_TOP", "RERAISE")),
        reraise=reraise,
        tail=N.tail(),
    )

    @staticmethod
    def find_finally_cutoff(mapping):
        f = mapping["finally_body"]
        g = mapping["fail_body"]
        if any(x.starts_line is not None for x in g.get_instructions()):
            return None
        if not isinstance(f, BlockTemplate):
            f = BlockTemplate([f])
        if not isinstance(g, BlockTemplate):
            g = BlockTemplate([g])
        if isinstance(g.members[0], InstTemplate) and g.members[0].inst.opname == "PUSH_EXC_INFO":
            g.members.pop(0)
        if isinstance(g.members[-1], InstTemplate) and g.members[-1].inst.opname == "RERAISE":
            g.members.pop()
        x = None
        for x, y in zip(f.members, g.members):
            if all(type(a) in [IfThen, IfElse] for a in (x, y)):
                continue
            if type(x) is not type(y):
                return None
        return x and f.members.index(x)

    cutoff: int

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            mapping = cls.template2.try_match(cfg, node)
            if mapping is None:
                return None
            mapping["try_header"] = mapping.pop("try_except")

        cutoff = cls.find_finally_cutoff(mapping)
        if cutoff is None:
            if cfg.run == 2:
                cutoff = 9999
            else:
                return None

        template = condense_mapping(cls, cfg, mapping, "try_header", "try_body", "finally_body", "fail_body", "reraise")
        template.cutoff = cutoff
        return template

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        header = source[self.try_header]
        body = source[self.try_body, 1]
        if isinstance(self.try_header, (Try3_11, TryElse3_11)) and self.members['try_body'] is None:
            s = header
        else:
            s = chain(header, self.line('try:'), body)

        if isinstance(self.finally_body, BlockTemplate):
            i = self.cutoff + 1
            in_finally = source[BlockTemplate(self.finally_body.members[:i]), 1] if i > 0 else []
            after = source[BlockTemplate(self.finally_body.members[i:])] if i < len(self.finally_body.members) else []
        else:
            in_finally = source[self.finally_body, 1]
            after = []

        return list(chain(s, self.line("finally:"), in_finally, after))


class Except3_9(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if [x.opname for x in node.get_instructions()] == ["RERAISE"]:
            return node
        if x := ExceptExc3_9.try_match(cfg, node):
            return x
        if x := BareExcept3_9.try_match(cfg, node):
            return x
        if isinstance(node, Except3_9):
            return node
        

@register_template(0, 1, (3, 9), (3, 10))
class Try3_9(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body"),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("tail."),
        except_body=~N("tail.").of_subtemplate(Except3_9),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "except_body",
            "try_footer",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        """


@register_template(0, 0, (3, 9), (3, 10))
class TryElse3_9(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body"),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("else_body").with_in_deg(1),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_9),
        else_body=~N("tail.").with_in_deg(1),
        tail=~N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "try_footer",
            "except_body",
            "else_body",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        else:
            {else_body}
        """


class ExcBody3_9(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if x := NamedExc3_9.try_match(cfg, node):
            return x
        return node


class NamedExc3_9(ExcBody3_9):
    template = T(
        header=~N("body", None).with_cond(with_instructions("POP_TOP", "STORE_FAST")),
        body=N("normal_cleanup.", None, "exception_cleanup"),
        normal_cleanup=~N("tail.").with_cond(with_instructions("STORE_FAST", "DELETE_FAST")),
        exception_cleanup=~N.tail().with_cond(with_instructions("STORE_FAST", "DELETE_FAST")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "exception_cleanup", "header", "body", "normal_cleanup")

    to_indented_source = defer_source_to("body")


class BareExcept3_9(Except3_9):
    template = T(
        except_body=~N("tail.", None).with_cond(starting_instructions("POP_TOP", "POP_TOP", "POP_TOP")).with_cond(has_incoming_edge_of_categories("exception", "false_jump")),
        tail=~N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "except_body",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        except:
            {except_body}
        """


class ExceptExc3_9(Except3_9):
    template = T(
        except_header=~N("body", "falsejump"),
        body=~N("tail.").of_subtemplate(ExcBody3_9),
        falsejump=~N("tail.").of_subtemplate(Except3_9),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "body",
            "except_header",
            "falsejump",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {except_header}
            {body}
        {falsejump}
        """


@register_template(2, 50, (3, 9), (3, 10))
class TryFinally3_9(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(ending_instructions("POP_TOP", "RERAISE")),
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_tail", None, "fail_body").of_type(TryElse3_9, Try3_9),
        finally_tail=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(ending_instructions("POP_TOP", "RERAISE")),
        tail=N.tail(),
    )

    @staticmethod
    def find_finally_cutoff(mapping):
        f = mapping["finally_body"]
        g = mapping["fail_body"]
        if any(x.starts_line is not None for x in g.get_instructions()):
            return None
        if not isinstance(f, BlockTemplate):
            f = BlockTemplate([f])
        if not isinstance(g, BlockTemplate):
            g = BlockTemplate([g])
        if isinstance(g.members[-1], InstTemplate) and g.members[-1].inst.opname == "RERAISE":
            g.members.pop()
        x = None
        for x, y in zip(f.members, g.members):
            if all(type(a) in [IfThen, IfElse] for a in (x, y)):
                continue
            if type(x) is not type(y):
                return None
        return x and f.members.index(x)

    cutoff: int

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            mapping = cls.template2.try_match(cfg, node)
            if mapping is None:
                return None
            mapping["try_header"] = mapping.pop("try_except")

        cutoff = cls.find_finally_cutoff(mapping)
        if cutoff is None:
            if cfg.run == 2:
                cutoff = 9999
            else:
                return None

        template = condense_mapping(cls, cfg, mapping, "try_header", "try_body", "finally_body", "fail_body")
        template.cutoff = cutoff
        return template

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        header = source[self.try_header]
        body = source[self.try_body, 1]

        if isinstance(self.finally_body, BlockTemplate):
            i = self.cutoff + 1
            in_finally = source[BlockTemplate(self.finally_body.members[:i]), 1] if i > 0 else []
            after = source[BlockTemplate(self.finally_body.members[i:])] if i < len(self.finally_body.members) else []
        else:
            in_finally = source[self.finally_body, 1]
            after = []

        return list(chain(header, self.line("try:"), body, self.line("finally:"), in_finally, after))


class Except3_6(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if [x.opname for x in node.get_instructions()] == ["END_FINALLY"]:
            return node
        if x := ExceptExc3_6.try_match(cfg, node):
            return x
        if x := BareExcept3_6.try_match(cfg, node):
            return x
        return None


@register_template(0, 0, (3, 6), (3, 7), (3, 8))
class Try3_6(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body").with_cond(without_top_level_instructions("SETUP_WITH")),
        try_body=N("try_footer", None, "except_body"),
        try_footer=~N("tail."),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_6),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "try_footer",
            "except_body",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        """


class ExcBody3_6(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if x := NamedExc3_6.try_match(cfg, node):
            return x
        return node


class NamedExc3_6(ExcBody3_6):
    template = T(
        header=~N("body", None).with_cond(starting_instructions("POP_TOP", "STORE_FAST")),
        body=N("normal_cleanup.", None, "exception_cleanup"),
        normal_cleanup=~N("exception_cleanup."),
        exception_cleanup=~N("tail.").with_cond(with_instructions("LOAD_CONST", "STORE_FAST")),
        tail=N.tail()
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "exception_cleanup", "header", "body", "normal_cleanup")

    to_indented_source = defer_source_to("body")


class ExceptExc3_6(Except3_6):
    template = T(
        except_header=~N("except_body", "no_match").with_cond(
            ending_instructions("COMPARE_OP", "POP_JUMP_IF_FALSE"),
            ending_instructions("COMPARE_OP", "POP_JUMP_FORWARD_IF_FALSE")
        ),
        except_body=~N("tail.", None).of_subtemplate(ExcBody3_6).with_in_deg(1),
        no_match=~N.tail().of_subtemplate(Except3_6),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "except_header",
            "except_body",
            "no_match",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {except_header}
            {except_body}
        {no_match}
        """


@register_template(0, 0, (3, 6), (3, 7), (3, 8))
class TryElse3_6(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body").with_cond(exact_instructions("SETUP_EXCEPT"), exact_instructions("SETUP_FINALLY")),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("else_body").with_in_deg(1),
        except_body=~N("tail").with_in_deg(1).of_subtemplate(Except3_6),
        else_body=~N("tail").with_in_deg(1),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "try_footer",
            "except_body",
            "else_body",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        else:
            {else_body}
        """


class BareExcept3_6(Except3_6):
    template = T(
        except_body=~N("tail."),
        tail=~N.tail(),
    )

    try_match = make_try_match(
        {
            EdgeKind.Fall: "tail",
        },
        "except_body",
    )

    @to_indented_source
    def to_indented_source():
        """
        except:
            {except_body}
        """

@register_template(2, 50, (3, 6), (3, 7), (3, 8))
class TryFinally3_6(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("finally_body", None, "fail_body"),
        finally_body=~N("fail_body").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(with_instructions("POP_TOP", "END_FINALLY")),
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_tail", None, "fail_body").of_type(TryElse3_6, Try3_6),
        finally_tail=N("finally_body", None, "fail_body"),
        finally_body=~N("fail_body").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(with_instructions("POP_TOP", "END_FINALLY")),
        tail=N.tail(),
    )

    cutoff: int

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            mapping = cls.template2.try_match(cfg, node)
            if mapping is None:
                return None
            mapping["try_header"] = mapping.pop("try_except")

        cutoff = next((i for i, x in enumerate(mapping["fail_body"].get_instructions())), None)
        if cutoff is None:
            return None

        template = condense_mapping(cls, cfg, mapping, "try_header", "try_body", "finally_body", "fail_body")
        template.cutoff = cutoff
        return template

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        header = source[self.try_header]
        body = source[self.try_body, 1]

        if isinstance(self.fail_body, BlockTemplate):
            i = self.cutoff + 1
            in_finally = source[BlockTemplate(self.fail_body.members[:i]), 1] if i > 0 else []
            after = source[BlockTemplate(self.fail_body.members[i:])] if i < len(self.fail_body.members) else []
        else:
            in_finally = source[self.fail_body, 1]
            after = []

        return list(chain(header, self.line("try:"), body, self.line("finally:"), in_finally, after))
