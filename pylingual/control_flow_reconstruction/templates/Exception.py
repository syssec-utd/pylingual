from itertools import chain
from typing import override

from .Block import BlockTemplate
from .Conditional import IfElse, IfThen
from ..cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, SourceLine, SourceContext, register_template
from ..utils import E, N, T, condense_mapping, defer_source_to, with_instructions, ending_instructions, exact_instructions, no_back_edges, revert_on_fail, starting_instructions, to_indented_source, make_try_match, versions_from, hook_template

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

class Except3_10(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if [x.opname for x in node.get_instructions()] == ["RERAISE"]:
            return node
        if x := ExceptExc3_10.try_match(cfg, node):
            return x
        if x := BareExcept3_10.try_match(cfg, node):
            return x
        if isinstance(node, Except3_10):
            return node

@register_template(0, 0, *versions_from(3, 12))
class Try3_12(ControlFlowTemplate):
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


@register_template(0, 0, *versions_from(3, 12))
class TryElse3_12(ControlFlowTemplate):
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
@register_template(0, 1, *versions_from(3, 10))
class Try3_10(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body"),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("tail."),
        except_body=~N("tail.").of_subtemplate(Except3_10),
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
class TryHeaderless3_10(ControlFlowTemplate):
    template = T(
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("tail."),
        except_body=~N("tail.").of_subtemplate(Except3_10),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_body",
            "except_body",
            "try_footer",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        try:
            {try_body}
        {except_body}
        """

@register_template(0, 0, *versions_from(3, 10))
class TryElse3_10(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=N("else_body").with_in_deg(1),
        except_body=N("tail.").with_in_deg(1).of_subtemplate(Except3_10),
        else_body=~N("tail.").with_in_deg(1),
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

class TryElseHeaderless3_10(ControlFlowTemplate):
    template = T(
        try_body=N("else_body.", None, "except_body"),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_10),
        else_body=~N("tail.").with_in_deg(1),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_body",
            "try_footer",
            "except_body",
            "else_body",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        try:
            {try_body}
        {except_body}
        else:
            {else_body}
        """

class ExcBody3_10(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if x := NamedExc3_10.try_match(cfg, node):
            return x
        return node

class NamedExc3_10(ExcBody3_10):
    template = T(
        header=N("body", None).with_cond(with_instructions("POP_TOP", "STORE_FAST")),
        body=N("normal_cleanup", None, "exception_cleanup"),
        normal_cleanup=N("tail.").with_cond(with_instructions("STORE_FAST", "DELETE_FAST")),
        exception_cleanup=N.tail().with_cond(with_instructions("STORE_FAST", "DELETE_FAST")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "exception_cleanup", "header", "body", "normal_cleanup")

    to_indented_source = defer_source_to("body")


# @register_template(0, 0, *versions_from(3, 10))
class BareExcept3_10(Except3_10):
    template = T(
        except_body=~N("tail.", None).of_type(BlockTemplate).with_cond(with_instructions("POP_EXCEPT")),
        tail=N.tail(),
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

#@register_template(0, 0, *versions_from(3, 10))
class ExceptExc3_10(Except3_10):
    template = T(
            except_header = N("body", "falsejump"),
            body = N("tail.").of_subtemplate(ExcBody3_10),
            falsejump = N("tail.").of_subtemplate(Except3_10),
            tail = N.tail(),
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

@register_template(2, 50, *versions_from(3, 10))
class TryFinally3_10(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(with_instructions("RERAISE")),
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_tail", None, "fail_body").of_subtemplate(Try3_10),
        finally_tail=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(with_instructions("RERAISE")),
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
        #if isinstance(g.members[0], InstTemplate) and g.members[0].inst.opname == "PUSH_EXC_INFO":
        #    g.members.pop(0)
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

class BareExcept3_11(Except3_11):
    template = T(
        except_body=N("except_footer", None, "reraise"),
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
class TryFinally3_12(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N(E.exc("reraise")),
        reraise=reraise,
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_body", None, "fail_body").of_type(Try3_12, TryElse3_12),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N(E.exc("reraise")),
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

        if isinstance(self.finally_body, BlockTemplate):
            i = self.cutoff + 1
            in_finally = source[BlockTemplate(self.finally_body.members[:i]), 1] if i > 0 else []
            after = source[BlockTemplate(self.finally_body.members[i:])] if i < len(self.finally_body.members) else []
        else:
            in_finally = source[self.finally_body, 1]
            after = []

        return list(chain(header, self.line("try:"), body, self.line("finally:"), in_finally, after))
