from itertools import chain
from typing import override

from .Block import BlockTemplate
from .Conditional import IfElse, IfThen
from ..cft import ControlFlowTemplate, EdgeCategory, EdgeKind, InstTemplate, SourceLine, SourceContext, register_template, out_edge_dict
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
    has_exception_edge,
    is_else_body,
    _is_line_nop,
    _opnames,
    _handler_exits_explicitly,
    same_code,
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


_FOOTER_JUMPS = ("JUMP_FORWARD", "JUMP_BACKWARD", "JUMP_BACKWARD_NO_INTERRUPT", "JUMP_ABSOLUTE")


def _footer_key(cfg, node):
    """key of a line-less `POP_EXCEPT; [cleanup;] JUMP` handler footer."""
    insts = node.get_instructions()
    ops = list(_opnames(insts))
    if ops[:1] != ["POP_EXCEPT"] or ops[-1:][0] not in _FOOTER_JUMPS or ops[1:-1] not in ([], ["LOAD_CONST", "STORE_FAST", "DELETE_FAST"], ["LOAD_CONST", "STORE_NAME", "DELETE_NAME"]):
        return None
    if not has_no_lines(cfg, node) or cfg.in_degree(node) != 1:
        return None
    out = out_edge_dict(cfg, node)
    return (tuple((i.opname, i.argval) for i in insts[:-1]), ops[-1], out[EdgeCategory.Natural], out[EdgeCategory.Exception])


@register_template(0, -10, *versions_from(3, 11))
class MergeExceptFooters3_11(ControlFlowTemplate):
    """merge the outer handler footer copied onto each exit of a nested try."""

    @classmethod
    @override
    def try_match(cls, cfg, node):
        key = _footer_key(cfg, node)
        if key is None or key[2] is None:
            return None
        # the copy comes from the cleanup of the try body's handler
        (body, _, _), = cfg.in_edges(node, data=True)
        handler = out_edge_dict(cfg, body)[EdgeCategory.Exception]
        if handler is None:
            return None
        for other in list(cfg.nodes):
            if other is node or _footer_key(cfg, other) != key:
                continue
            (pred, _, prop), = cfg.in_edges(other, data=True)
            if cfg.has_edge(pred, node):
                continue
            # skip sibling except clauses
            if not (has_no_lines(cfg, pred) and starting_instructions("POP_EXCEPT")(cfg, pred) and cfg.dominates(handler, pred)):
                continue
            cfg.remove_node(other)
            cfg.add_edge(pred, node, **prop)
            cfg.iterate()
            return node
        return None


def _arm_footer_key(cfg, node):
    """like _footer_key, but the trailing jump is optional."""
    insts = node.get_instructions()
    if insts and insts[-1].opname in _FOOTER_JUMPS:
        insts = insts[:-1]
    if list(_opnames(insts[:1])) != ["POP_EXCEPT"] or list(_opnames(insts[1:])) not in ([], ["LOAD_CONST", "STORE_FAST", "DELETE_FAST"], ["LOAD_CONST", "STORE_NAME", "DELETE_NAME"]):
        return None
    if not has_no_lines(cfg, node) or cfg.in_degree(node) != 1:
        return None
    out = out_edge_dict(cfg, node)
    return (tuple((i.opname, i.argval) for i in insts), out[EdgeCategory.Natural], out[EdgeCategory.Exception])


@register_template(0, -10, *versions_from(3, 11))
class MergeArmFooters3_11(ControlFlowTemplate):
    """merge the footer copied onto each arm of an if in one except clause."""

    @classmethod
    @override
    def try_match(cls, cfg, node):
        key = _arm_footer_key(cfg, node)
        if key is None or key[1] is None:
            return None
        (pred, _, _), = cfg.in_edges(node, data=True)
        for other in list(cfg.nodes):
            if other is node or _arm_footer_key(cfg, other) != key:
                continue
            (other_pred, _, prop), = cfg.in_edges(other, data=True)
            if other_pred is pred:
                continue
            # the arms must split at an if in the clause body, not at an except header
            doms = [d for d in cfg.nodes if cfg.dominates(d, pred) and cfg.dominates(d, other_pred)]
            split = next((d for d in doms if all(cfg.dominates(o, d) for o in doms)), None)
            if split is None or split in (pred, other_pred) or with_instructions("CHECK_EXC_MATCH")(cfg, split) or not has_some_lines(cfg, split):
                continue
            cfg.remove_node(other)
            cfg.add_edge(other_pred, node, **prop)
            cfg.iterate()
            return node
        return None


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
            {EdgeKind.Fall: "tail"},
            "try_header", "try_body", "except_body", "reraise",
            check=lambda cfg, m: not is_else_body(cfg, m),
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

_CONST_LOADS = ("LOAD_CONST", "LOAD_SMALL_INT", "LOAD_COMMON_CONSTANT")


def _const_return_len(members) -> int:
    """length of a trailing `return <const>`, else 0."""
    ops = [x.inst.opname if isinstance(x, InstTemplate) else None for x in members[-2:]]
    if ops[-1:] == ["RETURN_CONST"]:
        return 1
    if len(ops) == 2 and ops[0] in _CONST_LOADS and ops[1] == "RETURN_VALUE":
        return 2
    return 0


@register_template(0, 5, *versions_from(3, 11))
class TryFinallyDeadHandler3_12(ControlFlowTemplate):
    """`try: return <const> / finally: ...` with the dead exceptional finally copy dropped."""

    @classmethod
    @override
    def try_match(cls, cfg, node):
        if not isinstance(node, BlockTemplate) or out_edge_dict(cfg, node)[EdgeCategory.Exception] is not None:
            return None
        m = node.members
        n = _const_return_len(m)
        if not n:
            return None
        last = m[-n]
        for i in range(len(m) - 1 - n):
            a, b = m[i], m[i + 1]
            if not (_is_line_nop(a) and _is_line_nop(b)):
                continue
            if a.inst.source_line.strip() not in ("", "try:") or not b.inst.source_line.strip().startswith("return"):
                continue
            # a later-lined trailing return is the finally's, else the try's
            own = last.inst.starts_line is not None and last.inst.starts_line > b.inst.starts_line
            end = len(m) if own else len(m) - n
            if end - (i + 2) < 1:  # empty finally
                continue
            t = condense_mapping(cls, cfg, {"child": node}, "child")
            t.i, t.end = i, end
            return t
        return None

    def to_indented_source(self, source):
        m = self.child.members
        before = source[BlockTemplate(m[: self.i])] if self.i else []
        ret = source[m[self.i + 1], 1]
        fin = source[BlockTemplate(m[self.i + 2 : self.end]), 1]
        return list(chain(before, self.line("try:"), ret, self.line("finally:"), fin))

def _returned_value(node):
    """instruction that loads the returned value."""
    insts = node.get_instructions()
    return insts[-1] if insts[-1].opname == "RETURN_CONST" or len(insts) < 2 else insts[-2]


@register_template(0, -2, *versions_from(3, 11))
class TryFinallyReturn3_12(ControlFlowTemplate):
    """`try: a / finally: return x` with a line-less handler."""

    template = T(
        try_body=N("ret", None, "handler"),
        ret=N(E.meta("end"))
        .with_in_deg(1)
        .with_cond(exact_instructions("RETURN_CONST"), exact_instructions("RETURN_VALUE"), *(exact_instructions(load, "RETURN_VALUE") for load in _CONST_LOADS))
        .with_cond(has_some_lines),
        handler=N("footer", None, "reraise")
        .with_in_deg(1)
        .with_cond(exact_instructions("PUSH_EXC_INFO", "POP_TOP"))
        .with_cond(has_no_lines),
        footer=N(E.meta("end"))
        .with_in_deg(1)
        .with_cond(exact_instructions("POP_EXCEPT", "RETURN_CONST"), exact_instructions("POP_EXCEPT", "RETURN_VALUE"), *(exact_instructions("POP_EXCEPT", load, "RETURN_VALUE") for load in _CONST_LOADS))
        .with_cond(has_no_lines),
        reraise=reraise,
        end=N.tail(),
    )

    try_match = make_try_match(
        {EdgeKind.Meta: "end"},
        "try_body", "ret", "handler", "footer", "reraise",
        check=lambda cfg, m: (_returned_value(m["ret"]).opname, _returned_value(m["ret"]).argval) == (_returned_value(m["footer"]).opname, _returned_value(m["footer"]).argval),
    )

    @to_indented_source
    def to_indented_source():
        """
        try:
            {try_body}
        finally:
            {ret}
        """

@register_template(0, -1, *versions_from(3, 12))
class ReturnInTry3_12(ControlFlowTemplate):
    """pull a return emitted after POP_BLOCK back into the try body."""

    template = T(
        try_body=~N("ret", None).with_cond(has_exception_edge),
        ret=N(E.meta("end"))
        .with_in_deg(1)
        .with_cond(exact_instructions("RETURN_CONST"), exact_instructions("RETURN_VALUE"), *(exact_instructions(load, "RETURN_VALUE") for load in _CONST_LOADS))
        .with_cond(has_some_lines),  # needs its own line
        end=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Meta: "end"}, "try_body", "ret")

    @to_indented_source
    def to_indented_source():
        """
        {try_body}
        {ret}
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


@register_template(0, -1, *versions_from(3, 12))
class TryDupReturn3_12(TryElse3_12):
    """the try body's copy of the return the handlers jump to; not an else."""

    try_match = revert_on_fail(
        make_try_match(
            {EdgeKind.Fall: "tail"},
            "try_header", "try_body", "except_body", "try_else", "reraise",
            check=lambda cfg, m: m.get("try_else") is not None
            and m["try_else"].get_instructions()[-1].opname in ("RETURN_VALUE", "RETURN_CONST")
            and same_code(m["try_else"], m.get("tail")),
        )
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
        {try_else}
        """

def implicit_exception_return(cfg, node):
    if node is None:
        return False
    insts = node.get_instructions()
    opnames = list(_opnames(insts))
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


def _first_line_offset(node) -> int:
    return next((i.offset for i in node.get_instructions() if i.starts_line is not None), node.offset)


@register_template(0, 2, (3, 11))
class TryFallthrough3_11(Try3_12):
    """try body running straight into what follows; 3.11 lays handlers out inline, so that code comes after the handler."""

    try_match = revert_on_fail(
        make_try_match(
            {EdgeKind.Fall: "tail"},
            "try_header", "try_body", "except_body", "reraise",
            check=lambda cfg, m: m.get("tail") is not None and _first_line_offset(m["tail"]) > m["except_body"].offset,
        )
    )


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
            # an else body is laid out before the handler; code after the try comes after it
            check=lambda cfg, m: _first_line_offset(m["try_else"]) < m["except_body"].offset,
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
        except_body=N("except_footer.", None, "reraise").with_cond(without_top_level_instructions("RERAISE")).with_cond(starting_instructions("PUSH_EXC_INFO", "POP_TOP"), starting_instructions("POP_TOP")), 
        except_footer=~N("tail.").with_in_deg(1).with_cond(starting_instructions("POP_EXCEPT")),
        reraise=reraise,
        tail=N.tail(),
    )
    template2 = T(
        
        except_body=N("except_footer.", None, "reraise").with_cond(without_top_level_instructions("RERAISE")).with_cond(starting_instructions("PUSH_EXC_INFO", "POP_TOP"), starting_instructions("POP_TOP")), 
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
        
        start = 0
        m0 = f.members[0] if f.members else None
        if (
            isinstance(m0, InstTemplate) and m0.inst.opname == "NOP"
            and m0.inst.starts_line is not None
            and m0.inst.source_line.strip().startswith("return")
            and not (g.members and isinstance(g.members[0], InstTemplate) and g.members[0].inst.opname == "NOP")
        ):
            start = 1
        x = None
        for x, y in zip(f.members[start:], g.members):
            if all(type(a) in [IfThen, IfElse] for a in (x, y)):
                continue
            if type(x) is not type(y):
                return None
        return x and (start, f.members.index(x))

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
                cutoff = (0, 9999)
            else:
                return None
        template = condense_mapping(cls, cfg, mapping, "try_header", "try_body", "finally_body", "fail_body", "reraise")
        template.start, template.cutoff = cutoff
        return template

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        header = source[self.try_header]
        body = source[self.try_body, 1]
        if isinstance(self.try_header, (Try3_11, TryElse3_11, Try3_12, TryElse3_12)) and self.members["try_body"] is None:
            s = header
        else:
            s = chain(header, self.line("try:"), body)

        if isinstance(self.finally_body, BlockTemplate):
            ms, j, i = self.finally_body.members, self.start, self.cutoff + 1
            in_try = source[BlockTemplate(ms[:j]), 1] if j > 0 else []
            in_finally = source[BlockTemplate(ms[j:i]), 1] if i > j else []
            after = source[BlockTemplate(ms[i:])] if i < len(ms) else []
        else:
            in_try, in_finally, after = [], source[self.finally_body, 1], []
        return list(chain(s, in_try, self.line("finally:"), in_finally, after))

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


@register_template(0, -10, (3, 9), (3, 10))
class TryFooterPopBlock3_9(ControlFlowTemplate):
    """join a nested try's `JUMP_FORWARD -> POP_BLOCK` footer inside a named handler."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if not isinstance(node, InstTemplate) or node.inst.opname != "JUMP_FORWARD" or not has_no_lines(cfg, node):
            return None
        out = out_edge_dict(cfg, node)
        pop = out[EdgeCategory.Natural]
        if pop is None or not isinstance(pop, InstTemplate) or pop.inst.opname != "POP_BLOCK" or not has_no_lines(cfg, pop) or cfg.in_degree(pop) != 1:
            return None
        if out_edge_dict(cfg, pop)[EdgeCategory.Exception] is not out[EdgeCategory.Exception] or cfg.out_degree(node) != cfg.out_degree(pop):
            return None
        # must be followed by the handler exit, not e.g. a with block
        after = out_edge_dict(cfg, pop)[EdgeCategory.Natural]
        if after is None or not starting_instructions("POP_EXCEPT")(cfg, after):
            return None
        template = BlockTemplate([node, pop])
        in_edges = list(cfg.in_edges(node, data=True))
        out_edges = list(cfg.out_edges(pop, data=True))
        cfg.remove_nodes_from([node, pop])
        cfg.add_node(template)
        cfg.add_edges_from((src, template, prop) for src, _, prop in in_edges)
        cfg.add_edges_from((template, dst, prop) for _, dst, prop in out_edges)
        cfg.iterate()
        return template


def _named_cleanup_key(cfg, node):
    """key of a line-less `POP_EXCEPT; name = None; del name; return|jump` exit."""
    insts = node.get_instructions()
    if insts and insts[-1].opname in _FOOTER_JUMPS:
        insts = insts[:-1]
    ops = [i.opname for i in insts]
    if ops[:1] != ["POP_EXCEPT"] or not has_no_lines(cfg, node) or cfg.in_degree(node) != 1 or cfg.out_degree(node) != 1:
        return None
    if not any(op in ("DELETE_FAST", "DELETE_NAME") for op in ops):
        return None
    # a deduplicated return leaves a jump or fallthrough to the shared one
    target = None if ops[-1] == "RETURN_VALUE" else out_edge_dict(cfg, node)[EdgeCategory.Natural]
    if ops[-1] != "RETURN_VALUE" and (ops[-1] not in ("DELETE_FAST", "DELETE_NAME") or target is None):
        return None
    (pred,) = cfg.predecessors(node)
    return tuple((i.opname, i.argval) for i in insts), target, out_edge_dict(cfg, pred)[EdgeCategory.Exception]


@register_template(0, -10, (3, 9), (3, 10))
class MergeNamedCleanup3_9(ControlFlowTemplate):
    """merge a named handler's cleanup copied onto each exit of a nested try."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        key = _named_cleanup_key(cfg, node)
        if key is None or key[2] is None:
            return None
        for other in list(cfg.nodes):
            if other is node or _named_cleanup_key(cfg, other) != key:
                continue
            (pred, _, prop), = cfg.in_edges(other, data=True)
            if cfg.has_edge(pred, node):
                continue
            cfg.remove_node(other)
            cfg.add_edge(pred, node, **prop)
            cfg.iterate()
            return node
        return None


def _else_after_exiting_except(cfg, m) -> bool:
    """except body falls off the function, so the try's jump target is its else body."""
    tail, handler = m.get("tail"), m["except_body"]
    if tail is None or cfg.in_degree(tail) != 1 or out_edge_dict(cfg, handler)[EdgeCategory.Natural] is not None or _handler_exits_explicitly(handler):
        return False
    return any(i.opname == "RETURN_VALUE" for i in handler.get_instructions())


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
            check=lambda cfg, m: not _else_after_exiting_except(cfg, m),
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


@register_template(0, -2, (3, 9), (3, 10))
class TryFinallyReturn3_9(ControlFlowTemplate):
    """`try: a / finally: return x` in 3.9/3.10."""

    template = T(
        try_header=~N("try_body").with_cond(ending_instructions("SETUP_FINALLY")),
        try_body=N("ret", None, "handler").with_in_deg(1).with_cond(ending_instructions("POP_BLOCK")),
        ret=N(E.meta("end")).with_in_deg(1).with_cond(exact_instructions("LOAD_CONST", "RETURN_VALUE")).with_cond(has_some_lines),
        handler=N(E.meta("end")).with_in_deg(1).with_cond(exact_instructions("POP_TOP", "POP_TOP", "POP_TOP", "POP_EXCEPT", "LOAD_CONST", "RETURN_VALUE")).with_cond(has_no_lines),
        end=N.tail(),
    )

    try_match = make_try_match(
        {EdgeKind.Meta: "end"},
        "try_header", "try_body", "ret", "handler",
        check=lambda cfg, m: m["ret"].get_instructions()[0].argval == m["handler"].get_instructions()[-2].argval,
    )

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        finally:
            {ret}
        """


def _same_finally(cfg, m) -> bool:
    """inlined finally copy matches the exceptional finally body."""
    ret = [(i.opname, i.argval) for i in m["ret_finally"].get_instructions()][:-2]
    fail = [(i.opname, i.argval) for i in m["fail_body"].get_instructions()][:-1]
    return bool(ret) and ret == fail


@register_template(0, -2, (3, 9), (3, 10))
class TryExceptReturnFinally3_9(ControlFlowTemplate):
    """`try / except: return / finally` where the return runs through an inlined finally copy."""

    template = T(
        finally_header=~N("except_header").with_cond(ending_instructions("SETUP_FINALLY")),
        except_header=N("try_body", None, "fail_body").with_in_deg(1).with_cond(exact_instructions("SETUP_FINALLY")),
        try_body=N(None, None, "handler").with_in_deg(1),
        handler=N("ret_finally", None, "fail_body").with_in_deg(1).with_cond(starting_instructions("POP_TOP", "POP_TOP", "POP_TOP"), ending_instructions("POP_BLOCK")),
        ret_finally=N(E.meta("end")).with_in_deg(1).with_cond(ending_instructions("LOAD_CONST", "RETURN_VALUE"), ending_instructions("LOAD_FAST", "RETURN_VALUE")),
        fail_body=N(E.meta("end")).with_in_deg(2).with_cond(ending_instructions("RERAISE")).with_cond(has_no_lines),
        end=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Meta: "end"}, "finally_header", "except_header", "try_body", "handler", "ret_finally", "fail_body", check=_same_finally)

    @to_indented_source
    def to_indented_source():
        """
        {finally_header}
        try:
            {try_body}
        except:
            {handler}
        finally:
            {ret_finally}
        """


@register_template(0, -2, (3, 8))
class TryExceptReturnFinally3_8(ControlFlowTemplate):
    """`try / except: return / finally` in 3.8, via CALL_FINALLY."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if not ending_instructions("SETUP_FINALLY")(cfg, node):
            return None
        out = out_edge_dict(cfg, node)
        except_header = out[EdgeCategory.Natural]
        if except_header is None or cfg.in_degree(except_header) != 1 or not exact_instructions("SETUP_FINALLY")(cfg, except_header):
            return None
        eh = out_edge_dict(cfg, except_header)
        try_body, finally_body = eh[EdgeCategory.Natural], eh[EdgeCategory.Exception]
        if try_body is None or finally_body is None or cfg.in_degree(try_body) != 1 or cfg.out_degree(try_body) != 1:
            return None
        handler = out_edge_dict(cfg, try_body)[EdgeCategory.Exception]
        if handler is None or cfg.in_degree(handler) != 1 or not starting_instructions("POP_TOP", "POP_TOP", "POP_TOP")(cfg, handler):
            return None
        h = out_edge_dict(cfg, handler)
        call = h[EdgeCategory.Natural]
        if h[EdgeCategory.Exception] is not finally_body or call is None or cfg.in_degree(call) != 1 or not exact_instructions("CALL_FINALLY")(cfg, call):
            return None
        edges = {prop["kind"]: dst for _, dst, prop in cfg.out_edges(call, data=True)}
        ret = edges.get(EdgeKind.Fall)
        if edges.get(EdgeKind.Jump) is not finally_body or ret is None or cfg.in_degree(ret) != 1 or not ending_instructions("RETURN_VALUE")(cfg, ret):
            return None
        if not ending_instructions("END_FINALLY", "LOAD_CONST", "RETURN_VALUE")(cfg, finally_body) or cfg.in_degree(finally_body) != 3:
            return None
        if out_edge_dict(cfg, node)[EdgeCategory.Exception] is not None or cfg.out_degree(finally_body) != 1 or cfg.out_degree(ret) != 1:
            return None
        mapping = {"finally_header": node, "except_header": except_header, "try_body": try_body, "handler": handler, "call": call, "ret": ret, "finally_body": finally_body}
        return condense_mapping(cls, cfg, mapping, *mapping, out_edges={cfg.end: EdgeKind.Meta.prop()})

    @to_indented_source
    def to_indented_source():
        """
        {finally_header}
        try:
            {try_body}
        except:
            {handler}
        finally:
            {finally_body}
        """


@register_template(0, 1, (3, 9), (3, 10))
class TryNoFooter3_9(ControlFlowTemplate):
    """try in a loop whose footer merged into the body."""

    template = T(
        try_header=~N("try_body"),
        try_body=N("tail.", None, "except_body").with_in_deg(1),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_9),
        tail=N.tail(),
    )

    try_match = revert_on_fail(make_try_match({EdgeKind.Fall: "tail"}, "try_header", "try_body", "except_body", check=lambda cfg, m: m.get("tail") is not None and cfg.dominates(m["tail"], m["try_header"])))

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
        # a named handler's prologue is not a full except body
        if ending_instructions("SETUP_FINALLY")(cfg, node):
            return None
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
        # the tail may be outside the enclosing region
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

    def to_indented_source(self, source):
        # a break/continue leaving the handler takes the place of the normal cleanup
        from .Loop import BreakTemplate, ContinueTemplate

        jump = source[self.normal_cleanup] if isinstance(self.members["normal_cleanup"], (BreakTemplate, ContinueTemplate)) else []
        return source[self.body] + jump


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


@register_template(0, 1, (3, 6), (3, 7), (3, 8))
class TryNoFooter3_6(ControlFlowTemplate):
    """try in a loop whose footer merged into the body."""

    template = T(
        try_header=~N("try_body").with_cond(without_top_level_instructions("SETUP_WITH")),
        try_body=N("tail.", None, "except_body").with_in_deg(1),
        except_body=~N("tail.").with_in_deg(1).of_subtemplate(Except3_6),
        tail=N.tail(),
    )

    try_match = revert_on_fail(make_try_match({EdgeKind.Fall: "tail"}, "try_header", "try_body", "except_body", check=lambda cfg, m: m.get("tail") is not None and cfg.dominates(m["tail"], m["try_header"])))

    @to_indented_source
    def to_indented_source():
        """
        {try_header}
        try:
            {try_body}
        {except_body}
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
