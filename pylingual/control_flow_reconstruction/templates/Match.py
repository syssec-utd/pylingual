from itertools import chain
from typing import override
from .Block import BlockTemplate
from ..cft import SourceContext, SourceLine, ControlFlowTemplate, EdgeKind, register_template
from ..utils import E, T, N, ending_instructions, has_start_end_source, versions_from, make_try_match


class CaseOne(ControlFlowTemplate):
    template = T(
        case_header=~N("case_body", None).with_cond(has_start_end_source("case", ":")),
        case_body=~N("tail."),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Fall: "tail"}, "case_header", "case_body")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        case_body = source[self.case_body]

        cutoff = next((i for i, x in enumerate(self.case_header.get_instructions()) if x.source_line.strip().startswith("case")), 0)
        
        if isinstance(self.case_header, BlockTemplate):
            i = cutoff + 1
            case_header = source[BlockTemplate(self.case_header.members[:i]), 1] if i > 0 else []
            case_lines = source[BlockTemplate(self.case_header.members[i:]), 2] if i < len(self.case_header.members) else []
        else:
            case_header = source[self.case_header, 1]
            case_lines = []

        return list(chain(case_header, case_lines, case_body))


class WildCase(ControlFlowTemplate):
    template = T(
        case_header=~N(E.meta("tail")).with_cond(has_start_end_source("case", ":")),
        tail=N.tail(),
    )

    try_match = make_try_match({EdgeKind.Meta: "tail"}, "case_header")

    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:

        cutoff = next((i for i, x in enumerate(self.case_header.get_instructions()) if x.source_line.strip().startswith("case")), 0)
        
        if isinstance(self.case_header, BlockTemplate):
            i = cutoff + 1
            case_header = source[BlockTemplate(self.case_header.members[:i]), 1] if i > 0 else []
            case_lines = source[BlockTemplate(self.case_header.members[i:]), 2] if i < len(self.case_header.members) else []
        else:
            case_header = source[self.case_header, 1]
            case_lines = []

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
        match_line = None
        case_line = None
        case_body = source[self.case_body, 2]

        cutoff = next((i for i, x in enumerate(self.match_header.get_instructions()) if x.source_line.strip().startswith("match")), 0)

        if isinstance(self.match_header, BlockTemplate):
            i = cutoff + 1
            match_line = source[BlockTemplate(self.match_header.members[:i])] if i > 0 else []
            case_line = source[BlockTemplate(self.match_header.members[i:]), 1] if i < len(self.match_header.members) else []
        else:
            match_line = source[self.match_header, 1]
            case_line = []

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
        match_line = None
        case_line = None
        case_body = source[self.case_body, 2]

        cutoff = next((i for i, x in enumerate(self.match_header.get_instructions()) if x.source_line.strip().startswith("match")), 0)

        if isinstance(self.match_header, BlockTemplate):
            i = cutoff + 1
            match_line = source[BlockTemplate(self.match_header.members[:i])] if i > 0 else []
            case_line = source[BlockTemplate(self.match_header.members[i:]), 1] if i < len(self.match_header.members) else []
        else:
            match_line = source[self.match_header, 1]
            case_line = []

        return list(chain(match_line, case_line, case_body))