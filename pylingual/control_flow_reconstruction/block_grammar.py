"""
The block structure Python accepts, as a pushdown automaton over skeletons in source order (see skeleton.py).

Every skeleton the automaton accepts renders (skeleton_template.py) to source that compiles, as long as each statement
line is valid on its own and the statements fit together (`consistent`). It checks that:
    - header statements open a block and other statements do not; a while header comes after LOOP, so every
      structure has one spelling
    - clauses follow the block they continue: else, except / except*, finally, case
    - a try has an except or finally, a bare except and an irrefutable case come last, except and except* do not mix
    - break / continue are in a loop and not in an except* block, and continue is not in a finally block before 3.8
    - return is not in an except* block
    - decorators come right before a definition, docstrings and `from __future__` imports come first
    - nesting stays under CPython's limits
Empty blocks are fine: SourceContext writes `pass` in them. tests/test_block_grammar.py and tests/test_cflow_dataset.py
compile random accepted skeletons with every version.

From every state the automaton reaches the skeleton can still be finished (`complete`), so a decoder that only takes
allowed tokens never gets stuck.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from collections.abc import Iterable
from typing import NamedTuple

from pylingual.utils.version import PythonVersion

from .skeleton import CLOSE, LOOP, OPEN, parse_ref, ref

END = "</s>"  # end of the skeleton

MAX_BLOCKS = 18  # CPython's static block limit is 20, and a try adds one more in 3.9 - 3.11
MAX_FINALLY = 4  # nested finally blocks: CPython compiles a finally body twice, so each one doubles the code
MAX_DEPTH = 64  # nested blocks of any kind (CPython allows 100 levels of indentation)

# compiler blocks each kind of block takes at most (a try with a finally takes one more around its try, handlers
# and else; an `except ... as` handler takes two from 3.9), measured with every version
BLOCK_WEIGHT = {"while": 1, "for": 1, "with": 1, "try": 2, "except": 3, "except_bare": 3, "except*": 3, "try_else": 2, "finally": 1}
# what may follow a closed block of each kind in the block around it
CHAIN_AFTER = {
    "if": "if",
    "while": "loop",
    "for": "loop",
    "try": "try",
    "except": "except",
    "except_bare": "except_bare",
    "except*": "except*",
    "try_else": "try_else",
    "case": "case",
    "case_bare": "case_bare",
}
# chains after which a clause may come
CLAUSE_AFTER = {
    "else": ("if", "loop", "except", "except_bare", "except*"),
    "except": ("try", "except"),
    "except*": ("try", "except*"),
    "finally": ("try", "except", "except_bare", "except*", "try_else"),
    "case": ("match_empty", "case"),
}
# chains that must be continued before anything else: a try needs a handler, decorators a definition, a match a case
OBLIGATIONS = {"try", "deco", "match_empty"}


@dataclass(frozen=True)
class Shape:
    """What a statement is to the block structure."""

    opener: str | None = None  # block it opens: cond (if or while, which the skeleton chooses), if, while, for, with, try, except, except*, else, finally, match, case
    inline: bool = False  # a header with its body on the same line (`if x: y`), which opens no block
    bare: bool = False  # `except:` or an irrefutable case, which must come last
    jumps: frozenset[str] = frozenset()  # break / continue / return that leave the statement
    decorator: bool = False
    definition: bool = False  # def or class
    prefix: bool = False  # a docstring or `from __future__` import, which must come first

    def __str__(self):
        base = self.opener or ("deco" if self.decorator else "def" if self.definition else "prefix" if self.prefix else "stmt")
        flags = (["bare"] if self.bare else []) + sorted(self.jumps)
        return ("inline:" if self.inline else "") + "+".join([base, *flags])

    @staticmethod
    def parse(text: str) -> Shape:
        """Inverse of `str`."""
        inline = text.startswith("inline:")
        base, *flags = text.removeprefix("inline:").split("+")
        fields = {"deco": {"decorator": True}, "def": {"definition": True}, "prefix": {"prefix": True}, "stmt": {}}.get(base, {"opener": base})
        return Shape(**fields, inline=inline, bare="bare" in flags, jumps=frozenset(f for f in flags if f != "bare"))


KEYWORD_SHAPES = {
    "else": Shape("else"),
    "try": Shape("try"),
    "finally": Shape("finally"),
    "except": Shape("except", bare=True),
    "while_true": Shape("while"),
    "break": Shape(jumps=frozenset({"break"})),
    "continue": Shape(jumps=frozenset({"continue"})),
    "case_": Shape("case", bare=True),
}

# kinds (model_view.line_kind) of block headers, and the block they open
KIND_OPENERS = {"K_cond": "cond", "K_while_true": "while", "K_for": "for", "K_with": "with", "K_try": "try", "K_except": "except", "K_finally": "finally", "K_else": "else", "K_match": "match", "K_case": "case"}
# a keyword line with none of the bytecode it compiles to (model_view.statement_kind) is still written as its header
KEYWORD_LINE_KINDS = {"while True:": "K_while_true", "while 1:": "K_while_true", "try:": "K_try", "else:": "K_else", "finally:": "K_finally", "except:": "K_except"}
KIND_JUMPS = {"K_break": "break", "K_continue": "continue", "K_return": "return"}
INLINE_OPENERS = {"if", "elif", "while", "for", "with", "try", "except", "except*", "else", "finally", "case"}
# what makes a lone clause parse
CLAUSE_CONTEXT = {"else": "if 0: pass\n", "except": "try: pass\n", "except*": "try: pass\n", "finally": "try: pass\n"}


def first_word(text: str) -> str:
    """The keyword a line starts with (`except*` for an except* clause), without `async`."""
    text = text.removeprefix("async ")
    if text.startswith("except") and text[6:].lstrip().startswith("*"):
        return "except*"
    words = text.replace(":", " :", 1).split()
    return words[0] if words else ""


def soft_keyword(text: str) -> str | None:
    """
    `match` or `case` when `text` is that soft keyword's header (with its body for an inline case: `case 1: x`), even with
    no space after it (`match(x):`). None otherwise, as when it is a name: `case = x`, `match.group(1)`.
    """
    for word in ("match", "case"):
        rest = text.removeprefix(word)
        if rest == text or ("_" + rest[:1]).isidentifier():  # another word, or the bare name
            continue
        src = text + "\n    case _: pass" if word == "match" else "match 0:\n    " + text + ("\n        pass" if text.endswith(":") else "")
        return word if parse(src) is not None else None
    return None


def jumps_of(tree: ast.AST) -> frozenset[str]:
    """break / continue outside the loops in `tree`, and return, not counting nested functions and classes."""
    found = set()

    def visit(node: ast.AST, in_loop: bool):
        for name, value in ast.iter_fields(node):
            loop_body = in_loop or (isinstance(node, (ast.For, ast.AsyncFor, ast.While)) and name == "body")
            for child in value if isinstance(value, list) else [value]:
                if not isinstance(child, ast.AST) or isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                    continue
                if isinstance(child, ast.Break | ast.Continue) and not loop_body:
                    found.add("break" if isinstance(child, ast.Break) else "continue")
                elif isinstance(child, ast.Return):
                    found.add("return")
                visit(child, loop_body)

    visit(tree, False)
    return frozenset(found)


def is_irrefutable(pattern: ast.pattern) -> bool:
    if isinstance(pattern, ast.MatchAs):
        return pattern.pattern is None or is_irrefutable(pattern.pattern)
    if isinstance(pattern, ast.MatchOr):
        return any(map(is_irrefutable, pattern.patterns))
    return False


def parse(text: str) -> ast.Module | None:
    try:
        return ast.parse(text)
    except (SyntaxError, ValueError):
        return None


def shape_of(kind: str, text: str) -> Shape:
    """Shape of a statement of `kind` (see model_view.line_kind) whose translated line is `text`."""
    text = text.strip()
    word = first_word(text)
    if kind == "K_none":
        kind = KEYWORD_LINE_KINDS.get(text, kind)
    if kind == "K_deco":
        return Shape(decorator=True)
    if kind == "K_def":
        return Shape(definition=True)
    if text.startswith(("from __future__ import", "__doc__ = ")):
        return Shape(prefix=True)
    if text.startswith(("match", "case")):
        word = soft_keyword(text)  # soft keywords: None when a name starts the statement (`case = x`)
    inline = not text.endswith(":")
    if kind in KIND_OPENERS or (kind == "K_stmt" and inline and word in INLINE_OPENERS):
        opener = KIND_OPENERS.get(kind, word)
        if kind in ("K_while_true", "K_match"):
            inline = False
        if opener == "except" and word == "except*":
            opener = "except*"
        if opener == "cond" and inline:
            opener = "while" if word == "while" else "if"  # an inline elif is written as if (sanitize_line)
        opener = "if" if opener == "elif" else opener
        bare = opener == "except" and text.replace(" ", "").startswith("except:")
        if opener == "case":
            tree = parse("match 0:\n    " + text + ("" if inline else "\n        pass"))
            bare = tree is not None and (case := tree.body[0].cases[0]).guard is None and is_irrefutable(case.pattern)
        jumps = frozenset()
        if inline:
            if opener == "case":
                tree = parse("match 0:\n    " + text)
            elif opener == "try":
                tree = parse(text + "\nfinally: pass")
            else:
                tree = parse(CLAUSE_CONTEXT.get(opener, "") + text)
            jumps = jumps_of(tree) if tree is not None else frozenset()
        return Shape(opener, inline=inline, bare=bare, jumps=jumps)
    tree = parse(text)
    jumps = jumps_of(tree) if tree is not None else frozenset()
    if kind in KIND_JUMPS:
        jumps |= {KIND_JUMPS[kind]}
    return Shape(jumps=jumps)


def consistent(shapes: list[Shape]) -> bool:
    """
    Whether some skeleton places every statement. Only a bad translation is inconsistent: a case without a match,
    more irrefutable cases than matches, or a decorator without a definition. Nothing compiles then.
    """
    matches = sum(s.opener == "match" for s in shapes)
    cases = sum(s.opener == "case" for s in shapes)
    bare_cases = sum(s.opener == "case" and s.bare for s in shapes)
    decorators = sum(s.decorator for s in shapes)
    definitions = sum(s.definition for s in shapes)
    return (not cases or matches > 0) and bare_cases <= matches and (not decorators or definitions > 0)


class Frame(NamedTuple):
    kind: str  # root, or the block: if, while, for, with, try, except, except_bare, except*, else, try_else, finally, match, case, case_bare
    chain: str | None  # what the frame's last item lets come next: a CHAIN_AFTER value, deco, match_empty, or None
    loop: bool  # break / continue allowed
    no_continue: bool  # in a finally block, before 3.8
    no_jump: bool  # in an except* block: no break / continue
    no_return: bool  # in an except* block: no return
    blocks: int  # BLOCK_WEIGHT of the blocks around the frame's contents
    finallies: int  # finally blocks around the frame's contents


class State(NamedTuple):
    placed: int  # bitmask of placed statements
    stack: tuple[Frame, ...]  # open blocks, the root first
    pending: Frame | None = None  # a header was written: OPEN comes next and opens this frame
    loop_next: bool = False  # LOOP was written: a while header comes next (a cond statement, or `while True:`)
    done: bool = False  # END was written


ROOT = Frame("root", None, False, False, False, False, 0, 0)


class BlockGrammar:
    """
    The automaton for one code object whose statements have `shapes`. `allowed` gives the statements and other tokens
    that may come next, `step` takes one, `check` and `accepts` take a whole skeleton, and `complete` finishes one.
    States are immutable and hashable. `loops`, when given, are the statements that may head a while loop (from the
    bytecode: a loop jumps back to its header or its first statement); otherwise any header that can be one.
    """

    def __init__(self, shapes: list[Shape], version: PythonVersion | tuple | str, loops: Iterable[int] | None = None):
        self.shapes = shapes
        self.n = len(shapes)
        self.version = PythonVersion(version)
        self.all = (1 << self.n) - 1
        self.groups: dict[Shape, int] = {}  # statements of each shape, as a bitmask
        for i, shape in enumerate(shapes):
            self.groups[shape] = self.groups.get(shape, 0) | (1 << i)
        mask = lambda f: sum(1 << i for i, s in enumerate(shapes) if f(s))  # noqa: E731
        self.cases = mask(lambda s: s.opener == "case")
        self.bare_cases = mask(lambda s: s.opener == "case" and s.bare)
        self.jump_cases = mask(lambda s: s.opener == "case" and bool(s.jumps & {"break", "continue"}))
        self.ret_cases = mask(lambda s: s.opener == "case" and "return" in s.jumps)
        self.both_cases = self.jump_cases & self.ret_cases
        self.bare_jump_cases = self.jump_cases & self.bare_cases
        self.bare_ret_cases = self.ret_cases & self.bare_cases
        self.bare_both_cases = self.both_cases & self.bare_cases
        self.bare_restricted_cases = (self.jump_cases | self.ret_cases) & self.bare_cases
        self.matches = mask(lambda s: s.opener == "match")
        self.decorators = mask(lambda s: s.decorator)
        self.definitions = mask(lambda s: s.definition)
        self.prefixes = mask(lambda s: s.prefix)
        self.loop_headers = mask(lambda s: s.opener in ("cond", "while") and not s.inline)
        if loops is not None:
            self.loop_headers &= sum(1 << i for i in set(loops) if 0 <= i < self.n)

    def start(self) -> State:
        return State(0, (ROOT,))

    @staticmethod
    def left(state: State, mask: int) -> int:
        """How many statements in `mask` are not placed yet."""
        return (mask & ~state.placed).bit_count()

    def cases_fit(self, state: State, placed_case: Shape | None = None, close_top: bool = False, new_match: Frame | None = None) -> bool:
        """
        Whether all remaining cases (including jump/return-bearing and irrefutable ones) still have compatible match
        blocks available: unplaced matches (which can be placed in any context) plus open matches whose current case is
        not irrefutable.
        """
        c_all = self.left(state, self.cases)
        c_jump = self.left(state, self.jump_cases)
        c_ret = self.left(state, self.ret_cases)
        c_both = self.left(state, self.both_cases)
        b_all = self.left(state, self.bare_cases)
        b_jump = self.left(state, self.bare_jump_cases)
        b_ret = self.left(state, self.bare_ret_cases)
        b_both = self.left(state, self.bare_both_cases)
        b_any_res = self.left(state, self.bare_restricted_cases)
        if placed_case is not None:
            has_j = bool(placed_case.jumps & {"break", "continue"})
            has_r = "return" in placed_case.jumps
            c_all -= 1
            c_jump -= has_j
            c_ret -= has_r
            c_both -= has_j and has_r
            if placed_case.bare:
                b_all -= 1
                b_jump -= has_j
                b_ret -= has_r
                b_both -= has_j and has_r
                b_any_res -= has_j or has_r
        if c_all <= 0:
            return True
        unplaced = self.left(state, self.matches) - (1 if new_match is not None else 0)
        open_matches = [f for f, inner in zip(state.stack[:-1], state.stack[1:]) if f.kind == "match" and inner.kind == "case"]
        if not close_top and state.stack[-1].kind == "match" and state.stack[-1].chain != "case_bare":
            open_matches.append(state.stack[-1])
        if new_match is not None:
            open_matches.append(new_match)
        m_both = unplaced + sum(f.loop and not f.no_jump and not f.no_return for f in open_matches)
        m_jump = unplaced + sum(f.loop and not f.no_jump for f in open_matches)
        m_ret = unplaced + sum(not f.no_return for f in open_matches)
        m_any = unplaced + len(open_matches)
        return (
            (not c_both or m_both > 0)
            and (not c_jump or m_jump > 0)
            and (not c_ret or m_ret > 0)
            and m_any > 0
            and b_both <= m_both
            and b_jump <= m_jump
            and b_ret <= m_ret
            and b_any_res <= m_jump + m_ret - m_both
            and b_all <= m_any
        )

    def block_kind(self, shape: Shape, top: Frame, loop: bool = False) -> str:
        """The kind of block a header of `shape` opens in `top`."""
        opener = "while" if loop else shape.opener
        if opener in ("cond", "if"):
            return "if"
        if opener == "else":
            return "try_else" if top.chain in ("except", "except_bare", "except*") else "else"
        if shape.bare:
            return {"except": "except_bare", "case": "case_bare"}.get(opener, opener)
        return opener

    def open_frame(self, kind: str, top: Frame) -> Frame:
        loop = kind in ("while", "for")
        return Frame(
            kind,
            "match_empty" if kind == "match" else None,
            loop or top.loop,
            not loop and (top.no_continue or (kind == "finally" and self.version < (3, 8))),
            not loop and (top.no_jump or kind == "except*"),
            top.no_return or kind == "except*",
            top.blocks + BLOCK_WEIGHT.get(kind, 0),
            top.finallies + (kind == "finally"),
        )

    def can_place(self, state: State, shape: Shape, keyword: bool = False) -> bool:
        """Whether an item of `shape` (a statement, or a keyword) can come next, apart from the checks on what is left."""
        top = state.stack[-1]
        if state.loop_next:
            return shape.opener in ("cond", "while") and not shape.inline
        if shape.opener == "while" and not shape.inline and not keyword:
            return False  # a while statement comes after LOOP
        if (top.kind == "match") != (shape.opener == "case"):
            return False  # a match holds cases only
        if top.chain == "deco" and not (shape.decorator or shape.definition):
            return False
        if shape.opener in CLAUSE_AFTER:
            after = ("try", "except") if shape.opener == "except" and shape.bare else CLAUSE_AFTER[shape.opener]
            if top.chain not in after:
                return False
        elif top.chain in OBLIGATIONS - {"deco"}:
            return False
        if shape.jumps & {"break", "continue"} and (not top.loop or top.no_jump):
            return False
        if "continue" in shape.jumps and top.no_continue:
            return False
        if "return" in shape.jumps and top.no_return:
            return False
        if shape.opener is not None:
            kind = self.block_kind(shape, top)
            if top.blocks + BLOCK_WEIGHT.get(kind, 0) > MAX_BLOCKS or len(state.stack) > MAX_DEPTH:
                return False
            if kind == "finally" and top.finallies >= MAX_FINALLY:
                return False
            # a try needs room for the handler or finally after it
            if kind == "try" and top.blocks + BLOCK_WEIGHT["except"] > MAX_BLOCKS and top.finallies >= MAX_FINALLY:
                return False
        return True

    def allowed(self, state: State) -> tuple[int, list[str]]:
        """Statements (a bitmask) and other tokens (keywords, OPEN, CLOSE, LOOP, END) that may come next."""
        if state.done:
            return 0, []
        if state.pending is not None:
            return 0, [OPEN]
        top = state.stack[-1]
        prefixes_left = self.left(state, self.prefixes)
        stmts = 0
        for shape, group in self.groups.items():
            group &= ~state.placed & (self.loop_headers if state.loop_next else self.all)
            if not group or not self.can_place(state, shape):
                continue
            if shape.prefix and (top.kind != "root" or state.placed & ~self.prefixes):
                continue
            if prefixes_left and not shape.prefix:
                continue
            if shape.decorator and not self.left(state, self.definitions):
                continue
            # a definition must leave one for the decorators not placed yet
            if shape.definition and self.left(state, self.decorators) and self.left(state, self.definitions) < 2:
                continue
            # placing a match in a restricted context (outside a loop or inside except*) must not strand jump/return cases
            if shape.opener == "match" and not self.cases_fit(state, new_match=self.open_frame("match", top)):
                continue
            # the cases after an irrefutable one need another compatible match
            if shape.opener == "case" and shape.bare and not self.cases_fit(state, placed_case=shape, close_top=True):
                continue
            stmts |= group
        if state.loop_next or prefixes_left:
            return stmts, []
        tokens = [k for k, shape in KEYWORD_SHAPES.items() if self.can_place(state, shape, keyword=True) and not (k == "case_" and not self.cases_fit(state, close_top=True))]
        if self.left(state, self.loop_headers) and top.kind != "match" and top.chain not in OBLIGATIONS and top.blocks + BLOCK_WEIGHT["while"] <= MAX_BLOCKS and len(state.stack) <= MAX_DEPTH:
            tokens.append(LOOP)
        if top.chain not in OBLIGATIONS:
            if top.kind != "root" and (top.kind != "match" or self.cases_fit(state, close_top=True)):
                tokens.append(CLOSE)
            if top.kind == "root" and state.placed == self.all:
                tokens.append(END)
        return stmts, tokens

    def place(self, state: State, shape: Shape, bit: int = 0) -> State:
        """State after an item of `shape`: statement `bit`, or a keyword when 0."""
        top = state.stack[-1]
        placed = state.placed | bit
        if shape.opener is not None and not shape.inline:
            frame = self.open_frame(self.block_kind(shape, top, state.loop_next), top)
            return State(placed, state.stack, frame)
        if shape.opener is not None:  # an inline header is a whole block of its kind
            chain = CHAIN_AFTER.get(self.block_kind(shape, top))
        else:
            chain = "deco" if shape.decorator else None
        return State(placed, state.stack[:-1] + (top._replace(chain=chain),))

    def step(self, state: State, token: str) -> State:
        """State after `token`. Raises ValueError if it is not allowed."""
        stmts, tokens = self.allowed(state)
        i = parse_ref(token)
        if i is not None:
            if i >= self.n or not stmts >> i & 1:
                raise ValueError(f"{token} not allowed")
            return self.place(state, self.shapes[i], 1 << i)
        if token not in tokens:
            raise ValueError(f"{token} not allowed")
        if token == OPEN:
            return State(state.placed, state.stack + (state.pending,))
        if token == CLOSE:
            closed, parent = state.stack[-1], state.stack[-2]
            return State(state.placed, state.stack[:-2] + (parent._replace(chain=CHAIN_AFTER.get(closed.kind)),))
        if token == LOOP:
            return State(state.placed, state.stack, loop_next=True)
        if token == END:
            return state._replace(done=True)
        return self.place(state, KEYWORD_SHAPES[token])

    def check(self, tokens: list[str]) -> str | None:
        """Why the skeleton `tokens` (without END) is not accepted, or None if it is."""
        state = self.start()
        for n, token in enumerate([*tokens, END]):
            try:
                state = self.step(state, token)
            except ValueError as e:
                return f"token {n}: {e}"
        return None

    def accepts(self, tokens: list[str]) -> bool:
        return self.check(tokens) is None

    def complete(self, state: State) -> list[str]:
        """
        Tokens (without END) that finish a skeleton from `state`: what is left goes in statement order, blocks close
        when nothing more can go in them, and a statement that needs a loop or try gets one.
        """
        out = []
        for _ in range(12 * self.n + 8 * MAX_DEPTH):
            stmts, tokens = self.allowed(state)
            if END in tokens:
                return out
            top = state.stack[-1]
            chain = top.chain
            if OPEN in tokens:
                token = OPEN
            elif stmts:
                token = ref((stmts & -stmts).bit_length() - 1)
            elif chain == "try" and (handler := next((k for k in ("except", "finally") if k in tokens), None)):
                token = handler
            elif chain == "match_empty" and "case_" in tokens:
                token = "case_"
            elif LOOP in tokens:  # a while header is left
                token = LOOP
            elif len(state.stack) == 2 and top.kind == "while" and top.loop and not top.no_jump and not top.no_continue and not top.no_return and (hosted := self.host_in_loop(state, tokens)) is not None:
                token = hosted
            elif CLOSE in tokens:
                token = CLOSE
            else:
                token = self.host(state, tokens)
            out.append(token)
            state = self.step(state, token)
        raise RuntimeError("no completion")

    def host_in_loop(self, state: State, tokens: list[str]) -> str | None:
        """A keyword opening a try or inner loop inside a top-level while for a jump-bearing clause (`except E: break`, `else: break`)."""
        for i in range(self.n):
            shape = self.shapes[i]
            if state.placed >> i & 1 or not (shape.jumps & {"break", "continue"}):
                continue
            if shape.opener in ("except", "except*", "finally"):
                need = "try"
            elif shape.opener == "else":
                need = "while_true"
            else:
                continue
            if need in tokens:
                return need
        return None

    def host(self, state: State, tokens: list[str]) -> str:
        """A keyword opening the block a statement left over needs: a loop for jumps and else, a try for handlers."""
        for i in range(self.n):
            shape = self.shapes[i]
            if state.placed >> i & 1:
                continue
            if shape.jumps & {"break", "continue"} or shape.opener == "else":
                need = "while_true"
            elif shape.opener in ("except", "except*", "finally"):
                need = "try"
            else:
                continue
            if need in tokens:
                return need
        raise RuntimeError(f"no completion from {state}")
