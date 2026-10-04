from itertools import chain
from typing import override

from .Block import BlockTemplate
from .Conditional import IfElse, IfThen
from ..cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, SourceLine, SourceContext, register_template
from ..source import indent_lines
from ..utils import (
    E,
    N,
    T,
    condense_mapping,
    defer_source_to,
    with_instructions,
    without_instructions,
    ending_instructions,
    has_no_lines,
    has_some_lines,
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


def try_header_source(template, source):
    header = template.members["try_header"]
    if header is None:
        if isinstance(template, TryNested3_11):
            return try_header_source(template.try_body, source)
        return []
    lines = source[header]
    if all(inst.opname == "NOP" for inst in header.get_instructions()):
        # An exception-region header falls through to its protected body.
        # A predicted return here would make that body unreachable.
        lines = [line for line in lines if line.line.strip() not in ("return", "return None")]
    return lines


@register_template(0, -1, (3, 11))
class EmptyTry3_11(ControlFlowTemplate):
    """Retain an optimized empty try whose handler is skipped by its jump."""

    @classmethod
    def try_match(cls, cfg, node):
        if not isinstance(node, InstTemplate) or node.inst.opname != "JUMP_FORWARD":
            return None
        inst = node.inst
        skipped = [i for i in inst.bytecode if inst.offset < i.offset < inst.target.offset]
        if [i.opname for i in skipped] != [
            "PUSH_EXC_INFO", "LOAD_GLOBAL", "CHECK_EXC_MATCH", "POP_JUMP_FORWARD_IF_FALSE", "STORE_FAST", "POP_EXCEPT",
            "LOAD_CONST", "STORE_FAST", "DELETE_FAST", "JUMP_FORWARD", "LOAD_CONST", "STORE_FAST", "DELETE_FAST", "RERAISE",
            "RERAISE", "COPY", "POP_EXCEPT", "RERAISE",
        ]:
            return None
        reachable = {i for n in cfg for i in n.get_instructions()}
        if any(i in reachable for i in skipped):
            return None
        if not any(entry.start == skipped[0].offset and entry.target == skipped[-3].offset and entry.lasti for entry in inst.bytecode.named_exception_table):
            return None
        exception_name, binding = skipped[1].argval, skipped[4].argval
        if not isinstance(exception_name, str) or not exception_name.isidentifier() or not isinstance(binding, str) or not binding.isidentifier():
            return None
        if any(skipped[i].argval != binding for i in (7, 8, 11, 12)) or any(skipped[i].argval is not None for i in (6, 10)):
            return None
        if skipped[3].target is not skipped[14] or skipped[9].target.offset < inst.target.offset:
            return None
        template = condense_mapping(cls, cfg, {"body": node}, "body")
        template.exception_name, template.binding = exception_name, binding
        return template

    def to_indented_source(self, source):
        return self.line("try:") + self.line("pass", 1) + self.line(f"except {self.exception_name} as {self.binding}:") + self.line("pass", 1)


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


def implicit_exception_return(cfg, node):
    if node is None:
        return False
    insts = node.get_instructions()
    opnames = [inst.opname for inst in insts]
    if opnames == ["POP_EXCEPT", "LOAD_CONST", "RETURN_VALUE"]:
        return insts[1].argval is None
    if opnames not in (["POP_EXCEPT", "LOAD_CONST", "STORE_FAST", "DELETE_FAST", "LOAD_CONST", "RETURN_VALUE"], ["POP_EXCEPT", "LOAD_CONST", "STORE_NAME", "DELETE_NAME", "LOAD_CONST", "RETURN_VALUE"]):
        return False
    return insts[1].argval is None and insts[4].argval is None and insts[2].argval == insts[3].argval


class ExceptionReturnTail3_11(ControlFlowTemplate):
    template = T(
        jump=~N("body").with_in_deg(1).with_cond(exact_instructions("JUMP_FORWARD")).with_cond(has_no_lines),
        body=N(E.meta("end")).with_in_deg(1).with_cond(implicit_exception_return).with_cond(has_no_lines),
        end=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Meta: "end"}, "jump", "body")
    to_indented_source = defer_source_to("body")


@register_template(0, 0, (3, 11))
class Try3_11(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("try_else.", None, "except_body"),
        except_body=N("tail.", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        try_else=~N("tail.").with_in_deg(1).with_cond(has_no_lines).of_subtemplate(ExceptionReturnTail3_11)
        | N("tail.").with_in_deg(1).with_cond(has_no_lines)
        | ~N("tail.").with_in_deg(1).with_cond(has_no_lines),
        reraise=reraise,
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_else",
            "try_body",
            "except_body",
            "reraise",
        )
    )

    def to_indented_source(self, source):
        return list(chain(try_header_source(self, source), self.line("try:"), source[self.try_body, 1], source[self.except_body]))


@register_template(0, 0, (3, 11))
class TryElse3_11(ControlFlowTemplate):
    template = T(
        try_header=N("try_body"),
        try_body=N("try_else.", None, "except_body"),
        except_body=N("tail.", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        try_else=N("tail.").with_in_deg(1).with_cond(has_some_lines) | ~N("tail.").with_in_deg(1).with_cond(has_some_lines) ,
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

    def to_indented_source(self, source):
        return list(chain(try_header_source(self, source), self.line("try:"), source[self.try_body, 1], source[self.except_body], self.line("else:"), source[self.try_else, 1]))


@register_template(0, 1, (3, 11))
class TryNested3_11(Try3_11):
    template = T(
        try_body=N("try_else.", None, "except_body").of_type(Try3_11, TryElse3_11),
        except_body=N("tail.", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        try_else=~N("tail.").with_in_deg(1).with_cond(has_no_lines),
        reraise=reraise,
        tail=N.tail(),
    )

    try_match = revert_on_fail(make_try_match({EdgeKind.Fall: "tail"}, "try_header", "try_else", "try_body", "except_body", "reraise"))

    def to_indented_source(self, source):
        # A child's unprotected prefix stays outside the enclosing region too.
        header = try_header_source(self.try_body, source)
        body = source[self.try_body]
        return list(chain(header, self.line("try:"), indent_lines(body[len(header):]), source[self.except_body]))


class BareExcept3_11(Except3_11):
    template = T(
        except_body=N("except_footer.", None, "reraise").with_cond(without_top_level_instructions("RERAISE")),
        except_footer=~N("tail.").with_in_deg(1).with_cond(starting_instructions("POP_EXCEPT")),
        reraise=reraise,
        tail=N.tail(),
    )
    template2 = T(
        except_body=N("except_footer.", None, "reraise").with_cond(without_top_level_instructions("RERAISE")),
        except_footer=~N("tail.").with_in_deg(1).with_cond(starting_instructions("POP_EXCEPT")),
        reraise=reraise,
        tail=N(E.meta("end")).with_in_deg(1).with_cond(has_no_lines),
        end=N.tail()
    )

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        members = ["except_body", "except_footer"]
        mapping = cls.template2.try_match(cfg, node)
        if mapping is None:
            mapping = cls.template.try_match(cfg, node)
            if mapping is None:
                return None
        else:
            members.append("tail")
        template = condense_mapping(cls, cfg, mapping, *members)
        return template

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

    template_with_nops = T(
        STORE=N("prefix", None, "reraise").with_cond(exact_instructions("STORE_FAST"), exact_instructions("STORE_NAME")),
        prefix=N("body").with_in_deg(1).with_cond(lambda cfg, node: node is not None and bool(node.get_instructions()) and all(i.opname == "NOP" for i in node.get_instructions())),
        body=N("tail.", None, "cleanup"),
        cleanup=N(E.exc("reraise")).with_cond(exact_instructions("LOAD_CONST", "STORE_FAST", "DELETE_FAST", "RERAISE"), exact_instructions("LOAD_CONST", "STORE_NAME", "DELETE_NAME", "RERAISE")),
        reraise=reraise,
        tail=N.tail().of_subtemplate(NamedExcTail3_11),
    )

    @classmethod
    def try_match(cls, cfg, node):
        mapping = cls.template.try_match(cfg, node)
        if mapping is None:
            mapping = cls.template_with_nops.try_match(cfg, node)
        if mapping is None:
            return None
        edges = {mapping[name]: kind.prop() for kind, name in ((EdgeKind.Fall, "tail"), (EdgeKind.Exception, "reraise")) if mapping.get(name) is not None}
        return condense_mapping(cls, cfg, mapping, "STORE", "prefix", "body", "cleanup", out_edges=edges)

    @to_indented_source
    def to_indented_source():
        """
        {prefix}
        {body}
        """


class ExceptExc3_11(Except3_11):
    template = T(
        except_header=N("except_body", "no_match", "reraise").with_cond(ending_instructions("CHECK_EXC_MATCH", "POP_JUMP_FORWARD_IF_FALSE"), ending_instructions("CHECK_EXC_MATCH", "POP_JUMP_IF_FALSE")),
        except_body=N("except_footer.", None, "reraise").of_subtemplate(ExcBody3_11).with_in_deg(1),
        no_match=N("tail.", None, "reraise").with_in_deg(1).of_subtemplate(Except3_11),
        except_footer=~N("tail.").with_in_deg(1).with_cond(starting_instructions("SWAP", "POP_EXCEPT"), starting_instructions("POP_EXCEPT")),
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
        fail_body=N(E.exc("reraise")).with_cond(without_top_level_instructions("DELETE_FAST")),
        reraise=reraise,
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_body", None, "fail_body").of_type(Try3_11, TryElse3_11, Try3_12, TryElse3_12),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N(E.exc("reraise")).with_cond(without_top_level_instructions("DELETE_FAST")),
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
        if g.members and isinstance(g.members[0], InstTemplate) and g.members[0].inst.opname == "PUSH_EXC_INFO":
            g.members.pop(0)
        if g.members and isinstance(g.members[-1], InstTemplate) and g.members[-1].inst.opname == "RERAISE":
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
        if isinstance(self.try_header, (Try3_11, TryElse3_11, Try3_12, TryElse3_12)) and self.members["try_body"] is None:
            s = header
        else:
            s = chain(header, self.line("try:"), body)

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


@register_template(0, 0, (3, 9), (3, 10))
class Try3_9(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body"),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("tail."),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_9),
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
        {try_footer}
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
        header=~N("body", None).with_cond(with_instructions("POP_TOP", "STORE_FAST"), with_instructions("POP_TOP", "STORE_NAME")),
        body=N("normal_cleanup.", None, "exception_cleanup"),
        normal_cleanup=~N("tail.").with_cond(with_instructions("STORE_FAST", "DELETE_FAST"), with_instructions("STORE_NAME", "DELETE_NAME")),
        exception_cleanup=~N.tail().with_cond(with_instructions("STORE_FAST", "DELETE_FAST"), with_instructions("STORE_NAME", "DELETE_NAME")),
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
        fail_body=N("tail.").with_cond(without_top_level_instructions("DELETE_FAST")),
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_tail", None, "fail_body").of_type(TryElse3_9, Try3_9),
        finally_tail=N("finally_body", None, "fail_body"),
        finally_body=~N("tail.").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(without_top_level_instructions("DELETE_FAST")),
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
        if g.members and isinstance(g.members[-1], InstTemplate) and g.members[-1].inst.opname == "RERAISE":
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
        if [x.opname for x in node.get_instructions()[:1]] == ["END_FINALLY"]:
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
        try_body=N("try_footer.", None, "except_body"),
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
        header=~N("body", None).with_cond(with_instructions("POP_TOP", "STORE_FAST"), with_instructions("POP_TOP", "STORE_NAME")),
        body=N("normal_cleanup.", None, "exception_cleanup"),
        normal_cleanup=~N("exception_cleanup."),
        exception_cleanup=~N("tail.").with_cond(with_instructions("STORE_FAST", "DELETE_FAST"), with_instructions("STORE_NAME", "DELETE_NAME")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "exception_cleanup", "header", "body", "normal_cleanup")

    to_indented_source = defer_source_to("body")


class ExceptExc3_6(Except3_6):
    template = T(
        except_header=~N("except_body", "no_match").with_cond(ending_instructions("COMPARE_OP", "POP_JUMP_IF_FALSE"), ending_instructions("COMPARE_OP", "POP_JUMP_FORWARD_IF_FALSE")),
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
        try_header=~N("try_body").with_cond(ending_instructions("SETUP_EXCEPT"), ending_instructions("SETUP_FINALLY")),
        try_body=N("try_footer.", None, "except_body"),
        try_footer=~N("else_body").with_in_deg(1),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_6).with_cond(without_instructions("RETURN_VALUE")),
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


@register_template(0, 0, (3, 6), (3, 7), (3, 8))
class ReturnFinally3_6(ControlFlowTemplate):
    template = T(
        try_header=~N("try_body").with_cond(exact_instructions("SETUP_FINALLY")),
        try_body=N(None, None, "fail_body").with_cond(with_instructions("LOAD_CONST", "RETURN_VALUE")),
        fail_body=~N("tail."),
        tail=N.tail(),
    )

    try_match = revert_on_fail(
        make_try_match(
            {
                EdgeKind.Fall: "tail",
            },
            "try_header",
            "try_body",
            "fail_body",
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        finally:
            {fail_body}
        """


class BareExcept3_6(Except3_6):
    template = T(
        except_body=~N("tail.").with_cond(starting_instructions("POP_TOP", "POP_TOP", "POP_TOP")),
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
        fail_body=N("tail.").with_cond(without_top_level_instructions("DELETE_FAST")),
        tail=N.tail(),
    )
    template2 = T(
        try_except=N("finally_tail", None, "fail_body").of_type(TryElse3_6, Try3_6, ReturnFinally3_6),
        finally_tail=N("finally_body", None, "fail_body"),
        finally_body=~N("fail_body").with_in_deg(1).with_cond(no_back_edges),
        fail_body=N("tail.").with_cond(without_top_level_instructions("DELETE_FAST")),
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

        cutoff = next((i for i, x in enumerate(mapping["fail_body"].get_instructions()) if x.opname == "END_FINALLY"), 0)

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
