"""Inference-time lexical and mask-reference constraints for statement translation.

Provides a lightweight, tokenizer-indexed HuggingFace ``LogitsProcessor`` enforcing
model-agnostic invariants on generated masked Python statements:
- Static output bans (ASCII control bytes, raw newlines, ``<extra_id_*>``, bad words).
- Exact per-request input-mask whitelist for both atomic ``<mask_N>`` tokens and
  multi-piece BPE spellings of ``<mask_N>`` (enforced when ``>`` closes a complete mask).
- Character-level delimiter, quote, and f-string stack PDA rejecting provably
  unmatched closers, forbidding EOS on empty output or while delimiters/strings/escapes
  are open, and enforcing Python < 3.12 PEP 701 f-string quote/backslash rules inside
  replacement expressions.
"""

from __future__ import annotations

import codecs
import re
from collections import OrderedDict
from typing import TYPE_CHECKING, NamedTuple

import torch

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase


def _build_bytelevel_unicode_to_byte() -> dict[str, int]:
    """Inverse of GPT-2 / RoBERTa ByteLevel BPE bytes_to_unicode bijection."""
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    extra = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + extra)
            extra += 1
    return {chr(c): b for b, c in zip(bs, cs)}


_BYTELEVEL_U2B = _build_bytelevel_unicode_to_byte()

_ATOMIC_MASK_RE = re.compile(r"^<mask_(0|[1-9][0-9]*)>$", re.ASCII)
_CANONICAL_MASK_RE = re.compile(r"<mask_(0|[1-9][0-9]*)>", re.ASCII)
_INLINE_MASK_RE = re.compile(r"<mask_[0-9]+>", re.ASCII)
_EXTRA_ID_FULL_RE = re.compile(r"^<extra_id_\d+>$")
_EXTRA_ID_SUBSTR_RE = re.compile(r"<extra_id_\d+>")
_MASK_PREFIX = "<mask_"
_OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}
_CLOSE_TO_OPEN = {")": "(", "]": "[", "}": "{"}
_STRING_PREFIX_CHARS = frozenset("rRbBuUfFtT")
_VALID_PREFIX_PAIRS = frozenset(("fr", "rf", "br", "rb", "tr", "rt"))
_SYNTAX_CHARS = frozenset("()[]{}'\"\\#:<>")
_MIN_STACK_CACHE_WINDOW = 6
_MAX_MASK_CACHE = 4096


class LexState(NamedTuple):
    """Immutable lexical PDA state for a generated statement prefix."""

    # Frames are:
    #   "(" | "[" | "{"                        bracket/brace in code or f-string expr
    #   ("STR", quote)                         regular/raw/bytes string; quote in ("'", '"', "'''", '"""')
    #   ("FSTR_LIT", quote)                    f-string literal text
    #   ("FSTR_EXPR", just_opened)             f-string replacement expression
    #   "FSTR_SPEC"                            f-string format specifier
    stack: tuple = ()
    in_escape: bool = False
    triple_close: int = 0
    prefix_buf: str = ""
    prev_is_ident: bool = False
    just_closed_kind: str = ""  # "STR" or "FSTR_LIT" right after empty '' or ""
    just_closed_quote: str = ""  # "'" or '"'
    pending_fbrace_close: bool = False  # saw single '}' inside FSTR_LIT; next char must be '}'
    mask_partial: str = ""  # prefix of "<mask_<digits>" currently being spelled across tokens
    utf8_pending: bytes = b""  # incomplete valid UTF-8 prefix bytes across ByteLevel BPE tokens
    abstained: bool = False  # defensive fallback state if an invalid prefix ever entered replay
    has_content: bool = False  # at least one non-special content char or mask token has been emitted


INITIAL_STATE = LexState()


def _any_fstr_expr(stack: tuple) -> bool:
    """True if any enclosing frame is an f-string replacement expression."""
    return any(isinstance(frame, tuple) and frame[0] == "FSTR_EXPR" for frame in stack)


def _nearest_fstr_lit_quote(stack: tuple) -> str | None:
    """Return the quote delimiter of the nearest enclosing FSTR_LIT frame, if any."""
    for frame in reversed(stack):
        if isinstance(frame, tuple) and frame[0] == "FSTR_LIT":
            return frame[1]
    return None


def _forbidden_pre312_quotes(stack: tuple) -> frozenset[str]:
    """Quote styles forbidden for a new string opened inside an f-string expression on Python < 3.12."""
    forbidden: set[str] = set()
    for frame in stack:
        if isinstance(frame, tuple) and frame[0] == "FSTR_LIT":
            q = frame[1]
            if q == "'":
                forbidden.add("'")
                forbidden.add("'''")
            elif q == '"':
                forbidden.add('"')
                forbidden.add('"""')
            else:
                forbidden.add(q)
    return frozenset(forbidden)


def _advance_mask_partial(partial: str, ch: str, mask_count: int | None) -> tuple[str, bool]:
    """Update partial '<mask_<digits>' state. Enforces membership only when '>' closes a full mask."""
    if not partial:
        return ("<", True) if ch == "<" else ("", True)

    # Matching "<mask_" character by character (never reject before '>' closes a complete mask)
    if len(partial) < len(_MASK_PREFIX):
        if ch == _MASK_PREFIX[len(partial)]:
            return (partial + ch, True)
        return ("<", True) if ch == "<" else ("", True)

    digits = partial[len(_MASK_PREFIX) :]
    if "0" <= ch <= "9":
        if digits == "0" or digits == "!":
            # Leading zero (e.g. <mask_01>) or overflow: mark invalid if closed by '>'
            return ("<mask_!", True)
        new_digits = digits + ch
        if len(new_digits) > 9:
            return ("<mask_!", True)
        return (partial + ch, True)

    if ch == ">":
        if not digits:
            return ("", True)
        if digits == "!":
            return ("", False)
        if mask_count is not None and int(digits) >= mask_count:
            return ("", False)
        return ("", True)

    # Diverged from "<mask_<digits>>" (e.g. `a<mask_2` or `'<mask_9x'`)
    return ("<", True) if ch == "<" else ("", True)


def step_char(state: LexState, ch: str, *, py_lt_312: bool = False, mask_count: int | None = None) -> LexState | None:
    """Advance ``state`` by one character. Returns ``None`` if provably invalid."""
    mask_partial, mask_ok = _advance_mask_partial(state.mask_partial, ch, mask_count)
    if not mask_ok:
        return None

    if state.abstained:
        return state._replace(mask_partial=mask_partial, has_content=True)

    stack = state.stack
    top = stack[-1] if stack else None

    # 1. Inside a regular string literal
    if isinstance(top, tuple) and top[0] == "STR":
        quote = top[1]
        if state.in_escape:
            return state._replace(in_escape=False, triple_close=0, mask_partial=mask_partial, has_content=True)
        if ch == "\\":
            if py_lt_312 and _any_fstr_expr(stack):
                return None
            return state._replace(in_escape=True, triple_close=0, mask_partial=mask_partial, has_content=True)
        # On Python < 3.12, an outer 1-char f-string delimiter lexically terminates the f-string
        # even when it appears inside an opposite-quoted inner string (e.g. f'{"'"}').
        if py_lt_312 and _any_fstr_expr(stack) and ch in _forbidden_pre312_quotes(stack):
            return None
        if len(quote) == 1:
            if ch == quote:
                # Could be empty '' followed by a 3rd quote -> triple-quoted string
                just_kind = "STR" if state.triple_close == -1 else ""
                just_q = quote if state.triple_close == -1 else ""
                return LexState(
                    stack=stack[:-1],
                    just_closed_kind=just_kind,
                    just_closed_quote=just_q,
                    mask_partial=mask_partial,
                    has_content=True,
                )
            return state._replace(triple_close=0, mask_partial=mask_partial, has_content=True)
        # Triple-quoted string
        if ch == quote[0]:
            cnt = state.triple_close + 1
            if cnt == 3:
                return LexState(stack=stack[:-1], mask_partial=mask_partial, has_content=True)
            return state._replace(triple_close=cnt, mask_partial=mask_partial, has_content=True)
        return state._replace(triple_close=0, mask_partial=mask_partial, has_content=True)

    # 2. Inside an f-string literal text segment
    if isinstance(top, tuple) and top[0] == "FSTR_LIT":
        quote = top[1]
        if state.pending_fbrace_close:
            if ch == "}":
                return state._replace(pending_fbrace_close=False, triple_close=0, mask_partial=mask_partial, has_content=True)
            return None
        if state.in_escape:
            # In Python f-strings, '\' does NOT escape '{' or '}'; fall through to brace handling
            if ch in ("{", "}"):
                state = state._replace(in_escape=False)
            else:
                return state._replace(in_escape=False, triple_close=0, mask_partial=mask_partial, has_content=True)
        if ch == "\\":
            if py_lt_312 and _any_fstr_expr(stack):
                return None
            return state._replace(in_escape=True, triple_close=0, mask_partial=mask_partial, has_content=True)
        if py_lt_312 and _any_fstr_expr(stack) and ch in _forbidden_pre312_quotes(stack[:-1]):
            return None
        if ch == "{":
            return LexState(
                stack=stack + (("FSTR_EXPR", True),),
                mask_partial=mask_partial,
                has_content=True,
            )
        if ch == "}":
            return state._replace(pending_fbrace_close=True, triple_close=0, mask_partial=mask_partial, has_content=True)
        if len(quote) == 1:
            if ch == quote:
                just_kind = "FSTR_LIT" if state.triple_close == -1 else ""
                just_q = quote if state.triple_close == -1 else ""
                return LexState(
                    stack=stack[:-1],
                    just_closed_kind=just_kind,
                    just_closed_quote=just_q,
                    mask_partial=mask_partial,
                    has_content=True,
                )
            return state._replace(triple_close=0, mask_partial=mask_partial, has_content=True)
        # Triple-quoted f-string literal
        if ch == quote[0]:
            cnt = state.triple_close + 1
            if cnt == 3:
                return LexState(stack=stack[:-1], mask_partial=mask_partial, has_content=True)
            return state._replace(triple_close=cnt, mask_partial=mask_partial, has_content=True)
        return state._replace(triple_close=0, mask_partial=mask_partial, has_content=True)

    # 3. Inside an f-string format specifier
    if top == "FSTR_SPEC":
        if state.in_escape:
            # Backslash escapes quotes/backslashes in format specs, not '{' or '}'
            if ch in ("{", "}"):
                state = state._replace(in_escape=False)
            else:
                return state._replace(in_escape=False, triple_close=0, mask_partial=mask_partial, has_content=True)
        if ch == "\\":
            # Legal in top-level format specs even on < 3.12, forbidden inside an enclosing FSTR_EXPR on < 3.12
            if py_lt_312 and _any_fstr_expr(stack):
                return None
            return state._replace(in_escape=True, triple_close=0, mask_partial=mask_partial, has_content=True)
        if ch == "{":
            return LexState(stack=stack + (("FSTR_EXPR", False),), mask_partial=mask_partial, has_content=True)
        if ch == "}":
            return LexState(stack=stack[:-1], mask_partial=mask_partial, has_content=True)
        # Across all Python versions (including 3.12+), an unescaped enclosing delimiter terminates
        # the nearest enclosing f-string prematurely inside a format spec (raising SyntaxError).
        outer_q = _nearest_fstr_lit_quote(stack[:-1])
        if outer_q is not None:
            if len(outer_q) == 1:
                if ch == outer_q:
                    return None
                return state._replace(triple_close=0, mask_partial=mask_partial, has_content=True)
            if ch == outer_q[0]:
                cnt = state.triple_close + 1
                if cnt == 3:
                    return None
                return state._replace(triple_close=cnt, mask_partial=mask_partial, has_content=True)
        return state._replace(triple_close=0, mask_partial=mask_partial, has_content=True)

    # 4. Code context (top-level, inside (), [], {}, or inside FSTR_EXPR)
    in_fexpr_top = isinstance(top, tuple) and top[0] == "FSTR_EXPR"
    if in_fexpr_top and top[1]:
        # Immediately after '{' inside FSTR_LIT: a second '{' is an escaped literal '{{'
        if ch == "{":
            return LexState(stack=stack[:-1], mask_partial=mask_partial, has_content=True)
        # Otherwise lock this frame as a genuine replacement expression
        stack = stack[:-1] + (("FSTR_EXPR", False),)
        top = stack[-1]

    # Check if upgrading an immediately closed empty string '' or "" to triple-quoted ''' or """
    if state.just_closed_quote and ch == state.just_closed_quote:
        triple = ch * 3
        if py_lt_312 and _any_fstr_expr(stack) and triple in _forbidden_pre312_quotes(stack):
            return None
        return LexState(
            stack=stack + ((state.just_closed_kind, triple),),
            mask_partial=mask_partial,
            has_content=True,
        )

    # Opening a new string, f-string, or Python 3.14 PEP 750 t-string
    if ch in ("'", '"'):
        prefix_lower = state.prefix_buf.lower()
        kind = "FSTR_LIT" if ("f" in prefix_lower or "t" in prefix_lower) else "STR"
        if py_lt_312 and _any_fstr_expr(stack):
            if ch in _forbidden_pre312_quotes(stack):
                return None
        # Use triple_close=-1 as a sentinel meaning "0 chars seen inside this 1-char quote so far"
        return LexState(
            stack=stack + ((kind, ch),),
            triple_close=-1,
            mask_partial=mask_partial,
            has_content=True,
        )

    # Backslash in code (normalized single-line statements never use line continuations,
    # and Python < 3.12 forbids '\' anywhere inside f-string expressions)
    if ch == "\\":
        return None

    # Reject '#' comments in code (normalized single-line statements never contain comments
    # outside strings/format specs, and an accidental '#' can comment out closing delimiters)
    if ch == "#":
        return None

    # Colon directly inside FSTR_EXPR (bracket depth 0) transitions to FSTR_SPEC
    if ch == ":" and in_fexpr_top:
        return LexState(stack=stack[:-1] + ("FSTR_SPEC",), mask_partial=mask_partial, has_content=True)

    # Opening bracket / brace
    if ch in _OPEN_TO_CLOSE:
        return LexState(stack=stack + (ch,), mask_partial=mask_partial, has_content=True)

    # Closing bracket / brace
    if ch in _CLOSE_TO_OPEN:
        if ch == "}" and in_fexpr_top:
            return LexState(stack=stack[:-1], mask_partial=mask_partial, has_content=True)
        expected_open = _CLOSE_TO_OPEN[ch]
        if top != expected_open:
            return None
        return LexState(stack=stack[:-1], mask_partial=mask_partial, has_content=True)

    # Track potential string prefix letters (e.g. f, r, b, u, fr, rf, br, rb, t, tr, rt)
    is_ident_char = ch.isalnum() or ch == "_"
    new_prefix = ""
    if is_ident_char:
        if not state.prev_is_ident and ch in _STRING_PREFIX_CHARS:
            new_prefix = ch
        elif len(state.prefix_buf) == 1 and (state.prefix_buf + ch).lower() in _VALID_PREFIX_PAIRS:
            new_prefix = state.prefix_buf + ch

    return LexState(
        stack=stack,
        prefix_buf=new_prefix,
        prev_is_ident=is_ident_char,
        mask_partial=mask_partial,
        has_content=True,
    )


def _advance_utf8_bytes(pending: bytes, raw: bytes) -> tuple[str, bytes] | None:
    """Incrementally decode UTF-8 bytes, rejecting invalid sequences and dead-end prefixes."""
    buf = pending + raw
    try:
        decoded, consumed = codecs.utf_8_decode(buf, "strict", False)
    except UnicodeDecodeError:
        return None
    rem = buf[consumed:]
    if len(rem) >= 2:
        b0, b1 = rem[0], rem[1]
        # Reject 2-byte prefixes that have no valid UTF-8 completion (overlong, surrogate, >U+10FFFF)
        if (
            (b0 == 0xE0 and b1 < 0xA0)
            or (b0 == 0xED and b1 >= 0xA0)
            or (b0 == 0xF0 and b1 < 0x90)
            or (b0 == 0xF4 and b1 >= 0x90)
        ):
            return None
    return decoded, rem


def step_utf8_bytes(
    state: LexState, raw: bytes, *, py_lt_312: bool = False, mask_count: int | None = None
) -> LexState | None:
    """Advance ``state`` by raw UTF-8 bytes from a ByteLevel BPE token."""
    advanced = _advance_utf8_bytes(state.utf8_pending, raw)
    if advanced is None:
        return None
    decoded, rem = advanced
    cur: LexState | None = state._replace(utf8_pending=b"") if state.utf8_pending else state
    if decoded:
        cur = step_text(cur, decoded, py_lt_312=py_lt_312, mask_count=mask_count)
        if cur is None:
            return None
    if rem:
        if cur.pending_fbrace_close:
            return None
        return cur._replace(utf8_pending=rem, has_content=True)
    return cur


def step_atomic_mask(state: LexState, mask_idx: int, *, mask_count: int | None = None) -> LexState | None:
    """Advance ``state`` by an atomic ``<mask_N>`` token (treated as a placeholder, not '<'/'>')."""
    if state.utf8_pending:
        return None
    if mask_count is not None and mask_idx >= mask_count:
        return None
    if state.abstained:
        return state._replace(mask_partial="", has_content=True)
    stack = state.stack
    top = stack[-1] if stack else None
    if isinstance(top, tuple) and top[0] == "STR":
        return state._replace(in_escape=False, triple_close=0, mask_partial="", has_content=True)
    if isinstance(top, tuple) and top[0] == "FSTR_LIT":
        if state.pending_fbrace_close:
            return None
        return state._replace(in_escape=False, triple_close=0, mask_partial="", has_content=True)
    if top == "FSTR_SPEC":
        return state._replace(in_escape=False, triple_close=0, mask_partial="", has_content=True)
    if isinstance(top, tuple) and top[0] == "FSTR_EXPR" and top[1]:
        stack = stack[:-1] + (("FSTR_EXPR", False),)
    return LexState(
        stack=stack,
        prev_is_ident=True,
        mask_partial="",
        has_content=True,
    )


def step_text(state: LexState, text: str, *, py_lt_312: bool = False, mask_count: int | None = None) -> LexState | None:
    """Advance ``state`` through every character of ``text``."""
    if text and state.utf8_pending:
        return None
    cur: LexState | None = state
    for ch in text:
        cur = step_char(cur, ch, py_lt_312=py_lt_312, mask_count=mask_count)
        if cur is None:
            return None
    return cur


def is_eos_allowed(state: LexState) -> bool:
    """Whether EOS is allowed at ``state`` (non-empty, complete UTF-8, no open brackets/strings/escapes)."""
    if not state.has_content or state.utf8_pending:
        return False
    if state.abstained:
        return True
    return not state.stack and not state.in_escape and not state.pending_fbrace_close


def check_statement_constraints(text: str, *, py_lt_312: bool = False, mask_count: int | None = None) -> bool:
    """Check whether a complete masked statement satisfies all lexical and mask invariants."""
    if not text:
        return False
    if any(ord(c) < 32 or ord(c) == 127 for c in text):
        return False
    if _EXTRA_ID_SUBSTR_RE.search(text):
        return False
    state: LexState | None = INITIAL_STATE
    pos = 0
    for match in _CANONICAL_MASK_RE.finditer(text):
        if match.start() > pos:
            state = step_text(state, text[pos : match.start()], py_lt_312=py_lt_312, mask_count=mask_count)
            if state is None:
                return False
        state = step_atomic_mask(state, int(match.group(1)), mask_count=mask_count)
        if state is None:
            return False
        pos = match.end()
    if pos < len(text):
        state = step_text(state, text[pos:], py_lt_312=py_lt_312, mask_count=mask_count)
        if state is None:
            return False
    return is_eos_allowed(state)


class TokenizerConstraintIndex:
    """One-time vocabulary analysis for fast ``StatementLogitsProcessor`` masking."""

    def __init__(self, tokenizer: PreTrainedTokenizerBase, bad_words_ids: list[list[int]] | None = None):
        self.vocab_size = len(tokenizer)
        self.eos_token_id = tokenizer.eos_token_id
        self.pad_token_id = tokenizer.pad_token_id
        self.bos_token_id = tokenizer.bos_token_id

        excluded_roles = ("bos", "eos", "pad", "unk", "mask", "cls", "sep")
        self.special_non_output_ids = {
            tid
            for role in excluded_roles
            if (tid := getattr(tokenizer, f"{role}_token_id", None)) is not None and tid != self.eos_token_id
        }
        # T5 models trained with Roberta-style targets emit bos_token_id (<s>) as their first
        # generated token right after decoder_start_token_id (<pad>), then strip it on decode.
        self.allowed_initial_special_ids = {
            tid
            for role in ("bos", "cls")
            if (tid := getattr(tokenizer, f"{role}_token_id", None)) is not None and tid != self.eos_token_id
        }

        self.token_strings: list[str] = [
            tokenizer.decode([tid], skip_special_tokens=False, clean_up_tokenization_spaces=False)
            for tid in range(self.vocab_size)
        ]

        # Build static ban mask: existing bad_words_ids, non-EOS special role IDs,
        # <extra_id_*>, and ASCII control characters (never banning U+FFFD so multi-byte
        # UTF-8 byte-BPE pieces remain valid).
        static_ban = torch.zeros(self.vocab_size, dtype=torch.bool)
        for group in bad_words_ids or []:
            if len(group) == 1 and 0 <= group[0] < self.vocab_size:
                static_ban[group[0]] = True
        for tid in self.special_non_output_ids:
            if 0 <= tid < self.vocab_size:
                static_ban[tid] = True

        self.mask_id_to_num: dict[int, int] = {}
        self.atomic_mask_ids: list[int] = []
        self.atomic_mask_nums: list[int] = []
        self.partial_utf8_bytes: dict[int, bytes] = {}
        self.active_ids: list[int] = []
        self.inert_ids: list[int] = []

        max_closers_in_token = 0
        has_inline_mask_tokens = False

        for tid in range(self.vocab_size):
            if tid == self.eos_token_id:
                continue
            s = self.token_strings[tid]
            if _EXTRA_ID_FULL_RE.match(s) or _EXTRA_ID_SUBSTR_RE.search(s):
                static_ban[tid] = True
                continue
            if not static_ban[tid]:
                if not s or any(ord(c) < 32 or ord(c) == 127 for c in s):
                    static_ban[tid] = True
                    continue
            if static_ban[tid]:
                continue

            m = _ATOMIC_MASK_RE.match(s)
            if m is not None:
                num = int(m.group(1))
                self.mask_id_to_num[tid] = num
                self.atomic_mask_ids.append(tid)
                self.atomic_mask_nums.append(num)
                continue

            # Detect ByteLevel BPE partial UTF-8 byte tokens (e.g. split multi-byte UTF-8 pieces
            # that decode to U+FFFD in isolation) and recover their exact raw bytes so valid
            # continuation sequences pass while lone/dangling bytes are rejected.
            if "\ufffd" in s:
                raw_tok = tokenizer.convert_ids_to_tokens(tid)
                if isinstance(raw_tok, str) and raw_tok and all(ch in _BYTELEVEL_U2B for ch in raw_tok):
                    raw_bytes = bytes(_BYTELEVEL_U2B[ch] for ch in raw_tok)
                    if raw_bytes.decode("utf-8", errors="replace") == s:
                        self.partial_utf8_bytes[tid] = raw_bytes
                        self.active_ids.append(tid)
                        closers = sum(1 for c in s if c in ")]}'\"")
                        if closers > max_closers_in_token:
                            max_closers_in_token = closers
                        if _INLINE_MASK_RE.search(s):
                            has_inline_mask_tokens = True
                        continue

            # Because _advance_mask_partial only rejects when '>' closes a full mask, only
            # tokens containing characters in _SYNTAX_CHARS (which includes '>') can ever fail
            # a lexical or mask-spelling transition. Everything else behaves like an inert char.
            if any(c in _SYNTAX_CHARS for c in s):
                self.active_ids.append(tid)
                closers = sum(1 for c in s if c in ")]}'\"")
                if closers > max_closers_in_token:
                    max_closers_in_token = closers
                if _INLINE_MASK_RE.search(s):
                    has_inline_mask_tokens = True
            else:
                self.inert_ids.append(tid)

        self.stack_cache_window = max(_MIN_STACK_CACHE_WINDOW, max_closers_in_token + 1)
        self._has_inline_mask_tokens = has_inline_mask_tokens
        self.static_ban = static_ban
        self.atomic_mask_id_tensor = torch.tensor(self.atomic_mask_ids, dtype=torch.long)
        self.atomic_mask_num_tensor = torch.tensor(self.atomic_mask_nums, dtype=torch.long)
        self.inert_id_tensor = torch.tensor(self.inert_ids, dtype=torch.long)
        self._mask_cache: OrderedDict[tuple, torch.Tensor] = OrderedDict()

    def step_token(self, state: LexState, tid: int, *, py_lt_312: bool, mask_count: int | None) -> LexState | None:
        """Advance ``state`` by token ID ``tid``."""
        if tid == self.eos_token_id or tid in self.special_non_output_ids:
            return state
        num = self.mask_id_to_num.get(tid)
        if num is not None:
            return step_atomic_mask(state, num, mask_count=mask_count)
        raw_bytes = self.partial_utf8_bytes.get(tid)
        if raw_bytes is not None:
            return step_utf8_bytes(state, raw_bytes, py_lt_312=py_lt_312, mask_count=mask_count)
        return step_text(state, self.token_strings[tid], py_lt_312=py_lt_312, mask_count=mask_count)

    def check_token_sequence(self, token_ids: list[int], *, py_lt_312: bool = False, mask_count: int | None = None) -> bool:
        """Validate a tokenized target sequence against the exact inference constraint contract."""
        state: LexState | None = INITIAL_STATE
        for step_idx, tid in enumerate(token_ids):
            if tid < 0 or tid >= self.vocab_size:
                return False
            if tid == self.eos_token_id:
                return is_eos_allowed(state)
            if step_idx == 0 and tid in self.allowed_initial_special_ids:
                continue
            if self.static_ban[tid]:
                return False
            state = self.step_token(state, tid, py_lt_312=py_lt_312, mask_count=mask_count)
            if state is None:
                return False
        return is_eos_allowed(state)

    def _abstract_key(self, state: LexState, py_lt_312: bool, mask_count: int | None) -> tuple:
        norm_partial = state.mask_partial
        if mask_count is not None and norm_partial.startswith(_MASK_PREFIX):
            digits = norm_partial[len(_MASK_PREFIX) :]
            if digits and (digits == "!" or int(digits) >= mask_count):
                norm_partial = "<mask_!"
        key_mask_count = mask_count if (norm_partial or self._has_inline_mask_tokens) else None

        if state.abstained:
            return ("ABSTAINED", state.has_content, state.utf8_pending, norm_partial, key_mask_count)
        tail = state.stack[-self.stack_cache_window :]
        deeper = state.stack[: -self.stack_cache_window] if len(state.stack) > self.stack_cache_window else ()
        # Key on deeper-prefix pre-3.12 f-string context separately from tail so multi-char
        # tokens that pop tail frames still see exact enclosing FSTR_EXPR / FSTR_LIT restrictions.
        deeper_fexpr = _any_fstr_expr(deeper) if py_lt_312 else False
        deeper_forb = _forbidden_pre312_quotes(deeper) if py_lt_312 else frozenset()
        deeper_fspec_q = _nearest_fstr_lit_quote(deeper) if deeper else None
        return (
            tail,
            bool(deeper),
            state.in_escape,
            state.triple_close,
            state.prefix_buf.lower(),
            state.prev_is_ident,
            state.just_closed_kind,
            state.just_closed_quote,
            state.pending_fbrace_close,
            state.utf8_pending,
            state.has_content,
            norm_partial,
            key_mask_count,
            py_lt_312,
            deeper_fexpr,
            deeper_forb,
            deeper_fspec_q,
        )

    def disallowed_mask(self, state: LexState, *, py_lt_312: bool, mask_count: int | None) -> torch.Tensor:
        """Return CPU BoolTensor[vocab_size] where True means disallowed (excluding per-request atomic mask ban)."""
        key = self._abstract_key(state, py_lt_312, mask_count)
        cached = self._mask_cache.get(key)
        if cached is not None:
            self._mask_cache.move_to_end(key)
            return cached

        ban = self.static_ban.clone()
        if self.eos_token_id is not None and not is_eos_allowed(state):
            ban[self.eos_token_id] = True

        # Inert tokens: check one representative non-syntax character ("z")
        inert_ok = step_text(state, "z", py_lt_312=py_lt_312, mask_count=mask_count) is not None
        if not inert_ok and self.inert_ids:
            ban[self.inert_id_tensor] = True

        # Atomic masks are valid unless waiting for '}' in f-string or completing a UTF-8 codepoint
        if self.atomic_mask_ids and (state.pending_fbrace_close or state.utf8_pending):
            ban[self.atomic_mask_id_tensor] = True

        # Check the compact active subset (syntax tokens + ByteLevel partial UTF-8 byte tokens)
        for tid in self.active_ids:
            if self.step_token(state, tid, py_lt_312=py_lt_312, mask_count=mask_count) is None:
                ban[tid] = True

        self._mask_cache[key] = ban
        if len(self._mask_cache) > _MAX_MASK_CACHE:
            self._mask_cache.popitem(last=False)
        return ban


class StatementLogitsProcessor:
    """HuggingFace-compatible LogitsProcessor enforcing statement lexical & mask invariants.

    Beam-search safe with O(batch_beams) step-rolling state tracking and batched device
    transfers (zero per-row CUDA stream synchronizations).
    """

    def __init__(
        self,
        index: TokenizerConstraintIndex,
        mask_counts: list[int | None],
        *,
        py_lt_312: bool = False,
    ):
        self.index = index
        self.mask_counts = mask_counts
        self.py_lt_312 = py_lt_312
        # Step-rolling state cache: retains only the most recent prefix length (O(batch_beams) memory)
        self._last_len: int = -1
        self._last_states: dict[tuple[int, tuple[int, ...]], LexState] = {}
        self._device_static_ban: dict[tuple[torch.device, int], torch.Tensor] = {}
        self._request_mask_bans: dict[tuple[torch.device, int, int], torch.Tensor] = {}

    def _get_atomic_mask_ban(self, device: torch.device, mask_count: int, vocab_size: int) -> torch.Tensor | None:
        if not self.index.atomic_mask_ids:
            return None
        key = (device, mask_count, vocab_size)
        cached = self._request_mask_bans.get(key)
        if cached is not None:
            return cached
        # Filter on CPU once before transferring to device so hot-path GPU indexing never triggers aten::nonzero syncs
        cpu_ids = self.index.atomic_mask_id_tensor
        cpu_nums = self.index.atomic_mask_num_tensor
        banned_ids = cpu_ids[(cpu_nums >= mask_count) & (cpu_ids < vocab_size)].to(device)
        self._request_mask_bans[key] = banned_ids
        return banned_ids

    def _step_or_replay(self, req_idx: int, prefix: tuple[int, ...], mask_count: int | None) -> LexState:
        if not prefix:
            return INITIAL_STATE
        if len(prefix) == self._last_len:
            same = self._last_states.get((req_idx, prefix))
            if same is not None:
                return same
        if len(prefix) == self._last_len + 1:
            prev = self._last_states.get((req_idx, prefix[:-1]))
            if prev is not None:
                nxt = self.index.step_token(prev, prefix[-1], py_lt_312=self.py_lt_312, mask_count=mask_count)
                return nxt if nxt is not None else LexState(abstained=True, has_content=True)
        # Fallback for out-of-order calls (e.g. direct unit test invocations)
        state = INITIAL_STATE
        for tid in prefix:
            nxt = self.index.step_token(state, tid, py_lt_312=self.py_lt_312, mask_count=mask_count)
            state = nxt if nxt is not None else LexState(abstained=True, has_content=True)
        return state

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        batch_beams, vocab_size = scores.shape
        device = scores.device
        eos_id = self.index.eos_token_id
        num_reqs = len(self.mask_counts)
        beams_per_req = max(1, batch_beams // num_reqs) if num_reqs else 1

        static_key = (device, vocab_size)
        if static_key not in self._device_static_ban:
            static = self.index.static_ban
            if static.shape[0] != vocab_size:
                resized = torch.zeros(vocab_size, dtype=torch.bool)
                n = min(vocab_size, static.shape[0])
                resized[:n] = static[:n]
                static = resized
            self._device_static_ban[static_key] = static.to(device)
        static_ban_dev = self._device_static_ban[static_key]

        # Single batched GPU->CPU transfer for all beam prefixes
        all_seqs = input_ids[:, 1:].tolist()
        cur_len = len(all_seqs[0]) if all_seqs else 0

        active_rows: list[int] = []
        active_mask_counts: list[int | None] = []
        cpu_bans: list[torch.Tensor] = []
        next_states: dict[tuple[int, tuple[int, ...]], LexState] = {}

        for row, seq in enumerate(all_seqs):
            if eos_id is not None and eos_id in seq:
                continue
            req_idx = row // beams_per_req if num_reqs else 0
            mask_count = self.mask_counts[req_idx] if req_idx < num_reqs else None
            prefix = tuple(seq)
            state = self._step_or_replay(req_idx, prefix, mask_count)
            next_states[(req_idx, prefix)] = state

            ban = self.index.disallowed_mask(state, py_lt_312=self.py_lt_312, mask_count=mask_count)
            if ban.shape[0] != vocab_size:
                effective = torch.zeros(vocab_size, dtype=torch.bool)
                n = min(vocab_size, ban.shape[0])
                effective[:n] = ban[:n]
                ban = effective
            active_rows.append(row)
            active_mask_counts.append(mask_count)
            cpu_bans.append(ban)

        self._last_len = cur_len
        self._last_states = next_states

        if not active_rows:
            return scores

        # Single batched H2D transfer for all active rows
        ban_batch = torch.stack(cpu_bans, dim=0).to(device=device, non_blocking=(device.type == "cuda"))
        fallback_ban_batch = static_ban_dev.unsqueeze(0).expand(len(active_rows), vocab_size).clone()

        for local_idx, mask_count in enumerate(active_mask_counts):
            if mask_count is not None:
                valid_oob = self._get_atomic_mask_ban(device, mask_count, vocab_size)
                if valid_oob is not None and valid_oob.numel() > 0:
                    ban_batch[local_idx, valid_oob] = True
                    fallback_ban_batch[local_idx, valid_oob] = True

        # Allow BOS (<s>) at step 0 right after T5's decoder_start_token_id
        if cur_len == 0 and self.index.allowed_initial_special_ids:
            for bos_tid in self.index.allowed_initial_special_ids:
                if bos_tid < vocab_size:
                    ban_batch[:, bos_tid] = False
                    fallback_ban_batch[:, bos_tid] = False

        row_idx_tensor = torch.tensor(active_rows, dtype=torch.long, device=device)
        active_scores = scores.index_select(0, row_idx_tensor)
        masked = active_scores.masked_fill(ban_batch, float("-inf"))

        # Vectorized liveness guard (zero CUDA syncs): checks isfinite (catching both -inf and
        # NaN/+inf). If lexical+mask constraints leave no finite logit, fall back first to
        # static+OOB bans only; if even that has no finite logit (e.g. all--inf or all-NaN input),
        # fall back to finite zeros respecting static+OOB bans so output always has finite logits
        # without releasing OOB mask protection.
        no_finite_masked = (~torch.isfinite(masked)).all(dim=-1, keepdim=True)
        fallback = active_scores.masked_fill(fallback_ban_batch, float("-inf"))
        no_finite_fallback = (~torch.isfinite(fallback)).all(dim=-1, keepdim=True)
        uniform_fallback = torch.zeros_like(active_scores).masked_fill(fallback_ban_batch, float("-inf"))
        no_finite_uniform = (~torch.isfinite(uniform_fallback)).all(dim=-1, keepdim=True)
        last_resort = torch.where(no_finite_uniform, torch.zeros_like(active_scores), uniform_fallback)
        safe_fallback = torch.where(no_finite_fallback, last_resort, fallback)
        final_active = torch.where(no_finite_masked, safe_fallback, masked)

        scores.index_copy_(0, row_idx_tensor, final_active)
        return scores
