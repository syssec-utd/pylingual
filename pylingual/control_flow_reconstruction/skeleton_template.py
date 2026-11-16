"""Render a skeleton predicted by the control flow model as source, as a ControlFlowTemplate for SourceContext."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from xdis import iscode

from pylingual.editable_bytecode.utils import comprehension_names
from .block_grammar import shape_of
from .cft import ControlFlowTemplate
from .model_view import KEYWORD_LINES
from .skeleton import CLOSE, KEYWORD_TEXT, LOOP, OPEN, parse_ref
from .source import SourceContext, SourceLine, sanitize_line

if TYPE_CHECKING:
    from pylingual.editable_bytecode import EditableBytecode
    from .model_view import CflowRequest, Statement

# clauses and the block headers they may follow; "try else" is the else of a try
CLAUSE_AFTER = {"except": ("try", "except"), "else": ("if", "elif", "for", "while", "except"), "finally": ("try", "except", "try else")}


@dataclass
class Node:
    sid: int | None = None  # statement, or None for a keyword
    keyword: str | None = None
    loop: bool = False  # a `while` header
    children: list[Node] | None = None  # body, None if the node has no block


def parse_skeleton(tokens: list[str], n_stmts: int) -> list[Node]:
    """Skeleton tokens as a tree. Bad or repeated references and unbalanced braces are skipped."""
    root: list[Node] = []
    stack = [root]
    used: set[int] = set()
    loop = False
    for token in tokens:
        if token == LOOP:
            loop = True
            continue
        if token == OPEN:
            siblings = stack[-1]
            if siblings and siblings[-1].children is None:
                siblings[-1].children = []
                stack.append(siblings[-1].children)
        elif token == CLOSE:
            if len(stack) > 1:
                stack.pop()
        elif token in KEYWORD_TEXT:
            stack[-1].append(Node(keyword=token))
        elif (sid := parse_ref(token)) is not None and sid < n_stmts and sid not in used:
            used.add(sid)
            stack[-1].append(Node(sid=sid, loop=loop))
        loop = False
    return root


def condition(text: str) -> str | None:
    for keyword in ("if ", "elif ", "while "):
        if text.startswith(keyword):
            return text[len(keyword) :]
    return None


class SkeletonTemplate(ControlFlowTemplate):
    """Control flow of a whole code object, from a skeleton (in source order) predicted by the control flow model."""

    def __init__(self, bc: EditableBytecode, stmts: list[Statement], tokens: list[str]):
        self.bc = bc
        self.stmts = stmts
        self.tokens = tokens
        self.tree = parse_skeleton(tokens, len(stmts))
        self.blame = bc.codeobj
        self.header_lines = []

    @override
    def get_instructions(self):
        return list(self.bc)

    @override
    def __repr__(self):
        return f"SkeletonTemplate[{' '.join(self.tokens)}]"

    @staticmethod
    def for_request(bc: EditableBytecode, request: CflowRequest | None, tokens: list[str] | None = None) -> SkeletonTemplate:
        """
        The control flow of `bc`: the skeleton `tokens` for its request, or its statements in order without them.
        A code object without a request has nothing to structure: comprehensions and lambdas are written inside their
        parent's line, and an empty body gets `pass`.
        """
        if request is None:
            return SkeletonTemplate(bc, [], [])
        return SkeletonTemplate(bc, request.stmts, request.in_order() if tokens is None else tokens)

    def stmt_lines(self, stmt: Statement, source: SourceContext, depth: int, header: str | None, in_loop: bool) -> list[SourceLine]:
        """Lines of a statement (`header` replaces its first line), and placeholders for code objects it defines."""
        lines = []
        for inst in stmt.insts:  # its line start (merged cleanup lines are silent), and any code objects it defines
            if inst not in stmt.silent and (text := source.line_of(inst, raw=True)) is not None:
                if header is not None:
                    text, header = header, None
                elif not (in_loop and text in ("break", "continue")):
                    text = "" if text in KEYWORD_LINES else sanitize_line(text)  # structure without a block is a mistranslation
                if text:
                    lines.append(SourceLine(text, depth, self.blame))
            if inst.opname == "LOAD_CONST" and iscode(inst.argval) and inst.argval in source.cfts and inst.argval.co_name not in comprehension_names:
                lines.append(SourceLine("", depth + 1, inst.argval, inst.argval))
        return lines

    def stmt_line(self, node: Node, source: SourceContext) -> str | None:
        """Translated line of a statement node."""
        head = next((i for i in self.stmts[node.sid].insts if i.starts_line is not None), None)
        return None if head is None else source.line_of(head, raw=True)

    def inline_header(self, node: Node, source: SourceContext) -> str | None:
        """Line of a statement written with its body on the same line (`except E: x`), None for any other node."""
        if node.sid is None or node.children is not None or (text := self.stmt_line(node, source)) is None:
            return None
        shape = shape_of(self.stmts[node.sid].kind, text)
        return text.strip() if shape.inline and shape.opener is not None else None

    def header_text(self, node: Node, source: SourceContext, elif_: bool = False) -> str | None:
        """Line of a block header, with if / elif / while chosen by the skeleton."""
        text = self.stmt_line(node, source)
        cond = None if text is None else condition(text)
        if cond is None or text in ("while True:", "while 1:"):
            return text
        if node.loop:
            return "while " + cond
        return ("elif " if elif_ else "if ") + cond

    def opener(self, node: Node | None, source: SourceContext) -> str | None:
        """First word of the block header `node` renders as (if, try, except, ...), None if it opens no block. An inline
        header (`except E: x`) counts, as a whole block of its kind."""
        if node is None:
            return None
        if node.children is None:
            text = self.inline_header(node, source)
        else:
            text = KEYWORD_TEXT[node.keyword] if node.sid is None else self.header_text(node, source)
        words = (text or "").removeprefix("async ").split()
        return words[0].rstrip(":*") if words else None

    def is_elif(self, node: Node, source: SourceContext) -> bool:
        """`else { if ... { } [else { }] }` right after an if, which is written as elif."""
        c = node.children
        return node.keyword == "else" and bool(c) and len(c) <= 2 and c[0].children is not None and self.opener(c[0], source) == "if" and not c[0].loop and all(x.keyword == "else" for x in c[1:])

    def is_orphan(self, opener: str | None, prev: str | None, following: Node | None, source: SourceContext) -> bool:
        """A try without an except or finally after it, or a clause that does not follow a block it can continue."""
        if opener == "try":
            return self.opener(following, source) not in ("except", "finally")
        return opener in CLAUSE_AFTER and prev not in CLAUSE_AFTER[opener]

    def is_loop(self, node: Node, header: str | None) -> bool:
        if node.loop or node.keyword == "while_true":
            return True
        return (header or "").strip().startswith(("for ", "async for ", "while "))

    def render(self, nodes: list[Node], source: SourceContext, depth: int, in_loop: bool = False, prev: str | None = None) -> list[SourceLine]:
        """Source lines of `nodes` at indentation `depth`. `prev`: the header opened by the node before them."""
        lines = []
        for k, node in enumerate(nodes):
            if prev in ("if", "elif") and self.is_elif(node, source):
                cond, *rest = node.children
                lines += self.stmt_lines(self.stmts[cond.sid], source, depth, self.header_text(cond, source, elif_=True), in_loop)
                lines += self.render(cond.children, source, depth + 1, in_loop)
                lines += self.render(rest, source, depth, in_loop, prev="elif")
                prev = None
                continue
            opener = self.opener(node, source)
            # a clause without the block it continues does not compile, so its body goes in without the header
            orphan = self.is_orphan(opener, prev, nodes[k + 1] if k + 1 < len(nodes) else None, source)
            header = None
            if node.sid is not None:
                if node.children is not None:
                    header = "" if orphan else self.header_text(node, source)
                elif opener == "elif" and prev in ("if", "elif"):
                    header = self.inline_header(node, source)  # otherwise written as if (sanitize_line)
                lines += self.stmt_lines(self.stmts[node.sid], source, depth, header, in_loop)
            elif not orphan and (in_loop or node.keyword not in ("break", "continue")):
                lines.append(SourceLine(KEYWORD_TEXT[node.keyword], depth, self.blame))
            if node.children is not None:
                # a one-line compound statement (`if False: yield`) has no block, so its body follows it
                inner = depth if orphan or (header is not None and not header.endswith(":")) else depth + 1
                lines += self.render(node.children, source, inner, in_loop or self.is_loop(node, header))
            prev = None if orphan else "try else" if opener == "else" and prev == "except" else opener
        return lines

    @override
    def to_indented_source(self, source: SourceContext) -> list[SourceLine]:
        return self.render(self.tree, source, 0)
