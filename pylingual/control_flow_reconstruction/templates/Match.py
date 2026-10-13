import re
from itertools import chain
from typing import override
from ..source import indent_lines
from ..cft import SourceContext, SourceLine, ControlFlowTemplate, EdgeCategory, EdgeKind, register_template, out_edge_dict
from ..utils import E, T, N, ending_instructions, has_no_lines, has_start_end_source, versions_from, make_try_match, condense_mapping


def split_header(source: SourceContext, header: ControlFlowTemplate, keyword: str, indent: int) -> tuple[list[SourceLine], list[SourceLine]]:
    """split header lines after the `keyword` line; the rest go one level deeper."""
    lines = source[header]
    cut = next((i for i, x in enumerate(lines) if x.line.strip().startswith(keyword)), 0) + 1
    return indent_lines(lines[:cut], indent), indent_lines(lines[cut:], indent + 1)


_CASE_LINE = re.compile(r"case\b.*:$")
_PATTERN_STEP_OPS = {"JUMP_FORWARD", "JUMP_ABSOLUTE", "NOT_TAKEN", "POP_TOP", "NOP"}


def _is_pattern_step(cfg, node) -> bool:
    """line-less piece of a case pattern: a test, or a jump/pop between tests."""
    if node is None or not has_no_lines(cfg, node) or not node.get_instructions():
        return False
    out = out_edge_dict(cfg, node)
    if out[EdgeCategory.Meta] is not None:
        return False
    return out[EdgeCategory.Conditional] is not None or all(i.opname in _PATTERN_STEP_OPS for i in node.get_instructions())


@register_template(0, -5, *versions_from(3, 10))
class CasePattern(ControlFlowTemplate):
    """fold a case pattern's tests into one branch: natural to the body, false to the fail path."""

    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        lines = [i for i in node.get_instructions() if i.starts_line is not None]
        if not lines or not _CASE_LINE.match(lines[-1].source_line.strip()):
            return None
        exc = out_edge_dict(cfg, node)[EdgeCategory.Exception]
        if out_edge_dict(cfg, node)[EdgeCategory.Conditional] is None:
            return None
        region = [node]
        grew = True
        while grew:
            grew = False
            for succ in {s for n in region for s in cfg.successors(n)}:
                if succ in region or succ is exc or not _is_pattern_step(cfg, succ) or out_edge_dict(cfg, succ)[EdgeCategory.Exception] is not exc:
                    continue
                if not all(p in region for p in cfg.predecessors(succ)):
                    continue
                region.append(succ)
                grew = True
        if len(region) < 2:
            return None
        # failed tests and subject-popping cleanups lead to the fail path
        exits: dict[ControlFlowTemplate, set[bool]] = {}
        for n in region:
            pops = n is not node and out_edge_dict(cfg, n)[EdgeCategory.Conditional] is None and any(i.opname == "POP_TOP" for i in n.get_instructions())
            for _, dst, prop in cfg.out_edges(n, data=True):
                cat = EdgeCategory.from_kind(prop["kind"])
                if dst not in region and cat is not EdgeCategory.Exception:
                    exits.setdefault(dst, set()).add(cat is EdgeCategory.Conditional or pops)
        if len(exits) != 2:
            return None
        body = [n for n, fails in exits.items() if fails == {False}]
        fail = [n for n, fails in exits.items() if fails == {True}]
        if len(body) != 1 or len(fail) != 1:
            return None
        edges = {body[0]: EdgeKind.Fall.prop(), fail[0]: EdgeKind.FalseJump.prop()}
        if exc is not None:
            edges[exc] = EdgeKind.Exception.prop()
        mapping = {f"n{i}": n for i, n in enumerate(region)}
        return condense_mapping(cls, cfg, mapping, *mapping, out_edges=edges)

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        return source[self.n0]


class CaseOne(ControlFlowTemplate):
    template = T(
        case_header=~N("case_body", None).with_cond(has_start_end_source("case", ":")),
        case_body=~N("tail."),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "case_header", "case_body")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        case_body = source[self.case_body]

        case_header, case_lines = split_header(source, self.case_header, "case", 1)

        return list(chain(case_header, case_lines, case_body))


class WildCase(ControlFlowTemplate):
    template = T(
        case_header=~N(E.meta("tail")).with_cond(has_start_end_source("case", ":")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Meta: "tail"}, "case_header")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:

        case_header, case_lines = split_header(source, self.case_header, "case", 1)

        return list(chain(case_header, case_lines))


class CaseWrapper(ControlFlowTemplate):
    @classmethod
    @override
    def try_match(cls, cfg, node) -> ControlFlowTemplate | None:
        if x := CaseTwo.try_match(cfg, node):
            return x
        if x := CaseOne.try_match(cfg, node):
            return x
        if x := WildCase.try_match(cfg, node):
            return x


@register_template(1, 0, *versions_from(3, 10))
class CaseTwo(ControlFlowTemplate):
    template = T(
        case_header=~N("case_body", "other.").with_cond(has_start_end_source("case", ":")),
        case_body=~N("other."),
        other=~N("tail.").of_subtemplate(CaseWrapper) | N.tail(),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "case_header", "case_body", "other")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        case_header = source[self.case_header, 1]
        case_body = source[self.case_body, 2]
        other = source[self.other]

        return list(chain(case_header, case_body, other))


@register_template(0, 0, *versions_from(3, 10))
class Match(ControlFlowTemplate):
    template = T(
        match_header=~N("case_body", "tail").with_cond(has_start_end_source("match", ":")), 
        case_body=~N("tail.").with_in_deg(1) | ~N("tail").with_in_deg(1).with_cond(ending_instructions("POP_TOP")),
        tail=~N.tail().of_subtemplate(CaseWrapper) | N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "match_header", "case_body", "POP_TOP")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        case_body = source[self.case_body, 2]

        match_line, case_line = split_header(source, self.match_header, "match", 0)

        return list(chain(match_line, case_line, case_body))
    

@register_template(0, 0, *versions_from(3, 10))
class MultiMatch(ControlFlowTemplate):
    template = T(
        match_header=~N("multi_header", "POP_TOP").with_cond(has_start_end_source("match", ":")),
        multi_header=~N("case_body", "POP_TOP"), 
        case_body=~N("tail.").with_in_deg(1) | ~N("tail").with_in_deg(1).with_cond(ending_instructions("POP_TOP")),
        POP_TOP=~N("tail."),
        tail=~N.tail().of_subtemplate(CaseWrapper) | ~N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "multi_header", "match_header", "case_body", "POP_TOP")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        case_body = source[self.case_body, 2]

        match_line, case_line = split_header(source, self.match_header, "match", 0)

        return list(chain(match_line, case_line, case_body))