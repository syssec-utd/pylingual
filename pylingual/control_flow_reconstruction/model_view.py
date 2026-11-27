"""
Bytecode -> control flow model input.

A code object is split into statements, one per line start. Each statement is written as its kind (from the translated
line), its control flow opcodes and the edges that leave it, with targets as statement references:

    | <s1> K_for GET_ITER FOR_ITER f+ <s3> ~

Tokens:
    |           starts a statement, followed by its reference <sN> and its kind
    K_...       kind of the translated line (see `line_kind`); K_none for a keyword line its bytecode cannot be
    OPNAME      an opcode in CONTROL_OPS or a jump; a repeat in a row is written once. COMPARE_OP_EXC is an
                exception match (<= 3.8)
    n j t f     natural, jump, true and false edge to another statement, followed by its reference
    x           the exception handler changes to the statement that follows; x0: exceptions are no longer caught
    + - =       edge direction, appended to the edge letter: to a later, earlier or the same statement
    ~           after a reference: the edge lands inside that statement, not at its start
    @           code inside the statement that is not reached by falling through (merged handler code)
    nf          the statement never falls through to the next one
Edges to the next instruction and within a statement are implied, so are not written.

Trained models expect exactly this encoding: any change to the output here needs new models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pylingual.editable_bytecode.control_flow_graph import bytecode_to_control_flow_graph
from pylingual.utils.version import PythonVersion

from .block_grammar import BlockGrammar, Shape, consistent, shape_of, soft_keyword
from .skeleton import ref

if TYPE_CHECKING:
    from pylingual.editable_bytecode import EditableBytecode, Inst

STMT_SEP, MID, DETACHED, NO_FALL, NO_HANDLER = "|", "~", "@", "nf", "x0"
EDGE_TOKENS = {"natural": "n", "jump": "j", "true_jump": "t", "false_jump": "f", "exception": "x"}
EDGES = [e + d for e in EDGE_TOKENS.values() for d in "+-="]
# input tokens other than kinds and opcodes, in training vocabulary order
INPUT_TOKENS = [STMT_SEP, MID, DETACHED, NO_FALL, NO_HANDLER, *EDGES]

# opcodes kept in the input; all others are dropped
CONTROL_OPS = {
    "RETURN_VALUE", "RETURN_CONST", "RAISE_VARARGS", "RERAISE", "YIELD_VALUE", "YIELD_FROM", "SEND", "GET_AWAITABLE",
    "POP_BLOCK", "POP_EXCEPT", "PUSH_EXC_INFO", "CHECK_EXC_MATCH", "CHECK_EG_MATCH", "JUMP_IF_NOT_EXC_MATCH",
    "SETUP_LOOP", "SETUP_EXCEPT", "SETUP_FINALLY", "SETUP_WITH", "SETUP_ASYNC_WITH", "SETUP_CLEANUP", "SETUP_ANNOTATIONS",
    "BEGIN_FINALLY", "END_FINALLY", "CALL_FINALLY", "POP_FINALLY", "WITH_CLEANUP_START", "WITH_CLEANUP_FINISH",
    "BEFORE_WITH", "BEFORE_ASYNC_WITH", "WITH_EXCEPT_START", "LOAD_SPECIAL", "GET_ITER", "GET_AITER", "GET_ANEXT",
    "END_FOR", "END_ASYNC_FOR", "POP_ITER", "BREAK_LOOP", "CONTINUE_LOOP", "NOP", "LOAD_ASSERTION_ERROR", "CLEANUP_THROW",
    "MATCH_CLASS", "MATCH_MAPPING", "MATCH_SEQUENCE", "MATCH_KEYS", "GEN_START", "RETURN_GENERATOR", "ASYNC_GEN_WRAP",
}  # fmt: skip

# kinds of statements that open a block
HEADER_KINDS = {"K_cond", "K_while_true", "K_for", "K_with", "K_try", "K_except", "K_finally", "K_else", "K_match", "K_case"}

# lines that are only structure; the translator sometimes writes them for other code
KEYWORD_LINES = {"while True:", "while 1:", "try:", "else:", "finally:", "except:"}

# handler cleanup (re-raise after an except or finally body), which no source statement compiles to on its own.
# A lone POP_EXCEPT can be a `return` inside an except with a finally, so a cleanup must also re-raise or copy.
CLEANUP_OPS = {"COPY", "POP_EXCEPT", "RERAISE", "END_FINALLY"}

# keywords with a kind of their own; other simple statements are K_stmt
KEYWORD_KINDS = ("for", "with", "try", "except", "finally", "else", "return", "raise", "break", "continue")


@dataclass
class Statement:
    index: int
    insts: list[Inst]
    silent: set = field(default_factory=set)  # merged cleanup instructions, whose line is not rendered
    kind: str = "K_none"  # see statement_kind
    text: str = ""  # translated line
    loop_ok: bool = True  # a loop jumps back to it or the next statement, so it can head a while loop


@dataclass
class CflowRequest:
    """A code object for the control flow model: the model input, and the statement shapes and version its skeleton must fit (block_grammar.py)."""

    tokens: list[str]
    shapes: list[Shape]
    version: PythonVersion
    stmts: list[Statement] = field(default_factory=list)  # for rendering; empty when read from a dataset row
    loops: frozenset[int] | None = None  # statements that may head a while loop; None (a dataset row): any

    @property
    def n(self) -> int:
        return len(self.shapes)

    def grammar(self) -> BlockGrammar:
        return BlockGrammar(self.shapes, self.version, self.loops)

    def in_order(self) -> list[str]:
        """
        The statements in order, with the blocks BlockGrammar.complete gives them. When no skeleton fits the shapes (only
        a mistranslation does that), the statements in order without blocks: the renderer drops the headers then.
        """
        if not consistent(self.shapes):
            return [ref(k) for k in range(self.n)]
        grammar = self.grammar()
        return grammar.complete(grammar.start())

    def row(self) -> dict:
        """The request as dataset row fields."""
        out = {"input": " ".join(self.tokens), "n_stmts": self.n, "shapes": " ".join(map(str, self.shapes)), "version": str(self.version)}
        if self.loops is not None:
            out["loops"] = sorted(self.loops)
        return out

    @staticmethod
    def from_row(row: dict) -> CflowRequest:
        loops = frozenset(row["loops"]) if row.get("loops") is not None else None
        return CflowRequest(row["input"].split(), [Shape.parse(s) for s in row["shapes"].split()], PythonVersion(row["version"]), loops=loops)


def line_kind(text: str) -> str:
    """Kind of a translated line. if/elif/while share K_cond, since the translator often confuses them."""
    text = text.strip()
    if not text:
        return "K_none"
    words = text.split()
    head = words[0].rstrip(":")
    if text.startswith("async ") and len(words) > 1:
        head = words[1].rstrip(":")
    if text.startswith("@"):
        return "K_deco"
    if text in ("while True:", "while 1:"):
        return "K_while_true"
    if text.startswith("except") and text[6:].lstrip().startswith("*"):
        return "K_except"
    if head in ("if", "elif", "while"):
        return "K_cond"
    if head in KEYWORD_KINDS:
        return f"K_{head}"
    if head in ("def", "class"):
        return "K_def"
    if head in ("match", "case") and text.endswith(":"):
        return f"K_{head}"
    if text.endswith(":") and (keyword := soft_keyword(text)):  # no space after the keyword: `match(x):`, `case[a, b]:`
        return f"K_{keyword}"
    return "K_stmt"


def is_cleanup(insts: list[Inst]) -> bool:
    return all(i.opname in CLEANUP_OPS for i in insts) and any(i.opname != "POP_EXCEPT" for i in insts)


def split_statements(bc: EditableBytecode) -> list[Statement]:
    """Split `bc` into statements, one at each instruction with a starts_line (set from the segmentation)."""
    stmts: list[Statement] = []
    prologue: list[Inst] = []  # instructions before the first line start
    for inst in bc:
        if inst.starts_line is not None:
            stmts.append(Statement(len(stmts), [inst]))
        elif stmts:
            stmts[-1].insts.append(inst)
        else:
            prologue.append(inst)
    if stmts:
        stmts[0].insts[:0] = prologue
    # segmentation sometimes gives handler cleanup a line of its own; merge it into the statement before
    merged: list[Statement] = []
    for s in stmts:
        if merged and is_cleanup(s.insts):
            merged[-1].insts += s.insts
            merged[-1].silent.update(s.insts)
        else:
            merged.append(Statement(len(merged), s.insts))
    return merged


def statement_text(stmt: Statement, lines: list[str]) -> str:
    head = next((i for i in stmt.insts if i.starts_line is not None), None)
    if head is None or not 0 < head.starts_line <= len(lines):
        return ""
    return lines[head.starts_line - 1].strip()


def detached_instructions(stmts: list[Statement], graph) -> set:
    """First instructions of blocks inside a statement that are not reached by falling through (merged handler code)."""
    detached = set()
    for s in stmts:
        for prev, inst in zip(s.insts, s.insts[1:]):
            falls_in = prev in graph and graph.has_edge(prev, inst) and graph[prev][inst]["type"] != "exception"
            if inst in graph and not falls_in:
                detached.add(inst)
    return detached


def statement_kind(stmt: Statement, text: str, loop_headers: set[int]) -> str:
    """Kind of a statement whose translated line is `text`."""
    kind = line_kind(text)
    if text in KEYWORD_LINES and not any(i.opname in CONTROL_OPS or i.is_jump for i in stmt.insts):
        return "K_none"  # mistranslated: none of the code such a line compiles to
    if kind == "K_while_true" and stmt.index not in loop_headers:
        return "K_none"  # `while True:` must be jumped back to
    return kind


def encode_code_object(bc: EditableBytecode, lines: list[str]) -> tuple[list[Statement], list[str]]:
    """Statements of `bc` and the model input tokens. `lines` are the translated source lines."""
    stmts = split_statements(bc)
    if not stmts:
        return stmts, []
    graph = bytecode_to_control_flow_graph(bc)
    stmt_of = {inst: s.index for s in stmts for inst in s.insts}  # statement containing each instruction
    stmt_starting_at = {s.insts[0]: s.index for s in stmts}
    position = {inst: n for n, inst in enumerate(bc)}
    detached = detached_instructions(stmts, graph)

    def edges(inst):
        return graph.out_edges(inst, data=True) if inst in graph else []

    def reference(prefix: str, target_inst, target: int, source: int) -> list[str]:
        """`<prefix><direction> <s{target}>`, plus MID if the edge lands inside the target statement."""
        direction = "+" if target > source else "-" if target < source else "="
        return [prefix + direction, ref(target)] + ([MID] if stmt_starting_at.get(target_inst) != target else [])

    # statements a later statement jumps back to (loop headers), for spotting fake `while True:` lines
    loop_headers = {stmt_of[dst] for s in stmts for inst in s.insts for _, dst, data in edges(inst) if data["type"] != "exception" and stmt_of.get(dst, s.index) < s.index}
    # also counting a statement that jumps to itself (`while True: pass`), the statements a loop starts at
    loop_starts = loop_headers | {s.index for s in stmts for inst in s.insts for _, dst, data in edges(inst) if data["type"] != "exception" and stmt_of.get(dst) == s.index and position[dst] <= position[inst]}
    tokens: list[str] = []
    handler = None  # exception handler in effect; a token is written only when it changes
    for s in stmts:
        s.text = statement_text(s, lines)
        s.kind = statement_kind(s, s.text, loop_headers)
    last_break = max((s.index for s in stmts if s.kind == "K_break" or ("break" in s.text and "break" in shape_of(s.kind, s.text).jumps)), default=-1)
    for s in stmts:
        # a while loop jumps back to its header or first statement, emits SETUP_LOOP (<=3.7), or precedes a break;
        # on 3.8+, a while whose body always returns or raises compiles identically to an if
        s.loop_ok = bool({s.index, s.index + 1} & loop_starts) or any(i.opname == "SETUP_LOOP" for i in s.insts) or s.index < last_break
        if s.kind == "K_none" and s.text in ("while True:", "while 1:") and not s.loop_ok:
            # a mistranslation (a docstring's NOP is often translated so), written as nothing rather than a loop
            s.text = ""
        tokens += [STMT_SEP, ref(s.index), s.kind]
        falls_through = False
        last_op = None  # an opcode repeated in a row is written once
        for inst in s.insts:
            if inst not in graph:
                continue
            if inst in detached:
                tokens.append(DETACHED)
                last_op = None

            new_handler = next((dst for _, dst, data in edges(inst) if data["type"] == "exception"), None)
            if new_handler is not handler:
                handler = new_handler
                tokens += [NO_HANDLER] if handler not in stmt_of else reference("x", handler, stmt_of[handler], s.index)

            op = "COMPARE_OP_EXC" if inst.opname == "COMPARE_OP" and "exception" in str(inst.argrepr) else inst.opname
            if op in CONTROL_OPS or inst.is_jump or op == "COMPARE_OP_EXC":
                if op != last_op:
                    tokens.append(op)
                last_op = op

            for _, dst, data in edges(inst):
                kind, target = data["type"], stmt_of.get(dst)
                if target is None or kind == "exception":  # handlers are written above
                    continue
                if target == s.index + 1 and stmt_starting_at.get(dst) == target:
                    falls_through = True
                if kind == "natural" and position.get(dst) == position[inst] + 1:
                    continue  # to the next instruction: implied
                if target == s.index and dst not in detached:
                    continue  # within the statement
                tokens += reference(EDGE_TOKENS[kind], dst, target, s.index)
                last_op = None
        if not falls_through:
            tokens.append(NO_FALL)
    return stmts, tokens


def is_straight_line(tokens: list[str]) -> bool:
    """No jumps, exception edges, detached blocks or block headers: every statement in order is the skeleton."""
    return not any(t in EDGES or t == DETACHED or t in HEADER_KINDS for t in tokens)


def cflow_request(bc: EditableBytecode, lines: list[str]) -> CflowRequest | None:
    """Control flow model request for `bc`; None for comprehensions and code objects without statements."""
    if bc.is_comprehension:
        return None
    stmts, tokens = encode_code_object(bc, lines)
    if not stmts:
        return None
    return CflowRequest(tokens, [shape_of(s.kind, s.text) for s in stmts], PythonVersion(bc.version), stmts, frozenset(s.index for s in stmts if s.loop_ok))
