"""Inference-time lexical and mask-reference constraints for statement translation.

Provides a lightweight, tokenizer-indexed HuggingFace ``LogitsProcessor`` enforcing
model-agnostic invariants on generated masked Python statements:
- Static output bans (control bytes, raw newlines, invalid UTF-8, ``<extra_id_*>``).
- Exact per-request input-mask whitelist for both atomic ``<mask_N>`` tokens and
  multi-piece BPE spellings of ``<mask_N>``.
- Character-level delimiter, quote, and f-string stack PDA rejecting provably
  unmatched closers, forbidding EOS while delimiters/strings/escapes are open,
  and enforcing Python < 3.12 PEP 701 f-string quote/backslash rules inside
  replacement expressions.
"""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import TYPE_CHECKING, NamedTuple

import torch

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

_ATOMIC_MASK_RE = re.compile(r"^<mask_(\d+)>$")
_EXTRA_ID_RE = re.compile(r"^<extra_id_\d+>$")
_MASK_PREFIX = "<mask_"
_OPEN_TO_CLOSE = {"(": ")", "[": "]", "{": "}"}
_CLOSE_TO_OPEN = {")": "(", "]": "[", "}": "{"}
_STRING_PREFIX_CHARS = frozenset("rRbBuUfFtT")
_VALID_PREFIX_PAIRS = frozenset(("fr", "rf", "br", "rb", "tr", "rt"))
_SYNTAX_CHARS = frozenset("()[]{}'\"\\#:<>\n\r")
_MASK_SPELL_CHARS = frozenset("<mask_0123456789>")
_STACK_CACHE_WINDOW = 6
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
    abstained: bool = False  # unsupported exotic construct (e.g. 3.14 t-string); skip lexical gating


INITIAL_STATE = LexState()


def _in_fstr_expr(stack: tuple) -> bool:
    """True if currently inside an f-string replacement expression (not its format spec)."""
    for frame in reversed(stack):
        if frame == "FSTR_SPEC":
            return False
        if isinstance(frame, tuple):
            tag = frame[0]
            if tag == "FSTR_EXPR":
                return True
            if tag == "FSTR_LIT":
                return False
    return False


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
    """Update partial '<mask_<digits>' state. Returns (new_partial, allowed)."""
    if not partial:
        return ("<", True) if ch == "<" else ("", True)

    # Matching "<mask_" character by character
    if len(partial) < len(_MASK_PREFIX):
        if ch == _MASK_PREFIX[len(partial)]:
            nxt = partial + ch
            if nxt == _MASK_PREFIX and mask_count == 0:
                return ("", False)
            return (nxt, True)
        return ("<", True) if ch == "<" else ("", True)

    digits = partial[len(_MASK_PREFIX) :]
    if ch.isdigit():
        if digits == "0":
            # Leading zero like <mask_01> is never a valid normalized mask
            return ("", False)
        new_digits = digits + ch
        if mask_count is not None and int(new_digits) >= mask_count:
            return ("", False)
        return (partial + ch, True)

    if ch == ">":
        if not digits:
            return ("", True)
        if mask_count is not None and int(digits) >= mask_count:
            return ("", False)
        return ("", True)

    # Diverged from "<mask_<digits>>" (e.g. `a < mask_val`)
    return ("<", True) if ch == "<" else ("", True)


def step_char(state: LexState, ch: str, *, py_lt_312: bool = False, mask_count: int | None = None) -> LexState | None:
    """Advance ``state`` by one character. Returns ``None`` if provably invalid."""
    mask_partial, mask_ok = _advance_mask_partial(state.mask_partial, ch, mask_count)
    if not mask_ok:
        return None

    if state.abstained:
        return state._replace(mask_partial=mask_partial)

    stack = state.stack
    top = stack[-1] if stack else None

    # 1. Inside a regular string literal
    if isinstance(top, tuple) and top[0] == "STR":
        quote = top[1]
        if state.in_escape:
            return state._replace(in_escape=False, triple_close=0, mask_partial=mask_partial)
        if ch == "\\":
            if py_lt_312 and _in_fstr_expr(stack[:-1]):
                return None
            return state._replace(in_escape=True, triple_close=0, mask_partial=mask_partial)
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
                )
            return state._replace(triple_close=0, mask_partial=mask_partial)
        # Triple-quoted string
        if ch == quote[0]:
            cnt = state.triple_close + 1
            if cnt == 3:
                return LexState(stack=stack[:-1], mask_partial=mask_partial)
            return state._replace(triple_close=cnt, mask_partial=mask_partial)
        return state._replace(triple_close=0, mask_partial=mask_partial)

    # 2. Inside an f-string literal text segment
    if isinstance(top, tuple) and top[0] == "FSTR_LIT":
        quote = top[1]
        if state.pending_fbrace_close:
            if ch == "}":
                return state._replace(pending_fbrace_close=False, triple_close=0, mask_partial=mask_partial)
            return None
        if state.in_escape:
            return state._replace(in_escape=False, triple_close=0, mask_partial=mask_partial)
        if ch == "\\":
            return state._replace(in_escape=True, triple_close=0, mask_partial=mask_partial)
        if ch == "{":
            return LexState(
                stack=stack + (("FSTR_EXPR", True),),
                mask_partial=mask_partial,
            )
        if ch == "}":
            return state._replace(pending_fbrace_close=True, triple_close=0, mask_partial=mask_partial)
        if len(quote) == 1:
            if ch == quote:
                just_kind = "FSTR_LIT" if state.triple_close == -1 else ""
                just_q = quote if state.triple_close == -1 else ""
                return LexState(
                    stack=stack[:-1],
                    just_closed_kind=just_kind,
                    just_closed_quote=just_q,
                    mask_partial=mask_partial,
                )
            return state._replace(triple_close=0, mask_partial=mask_partial)
        # Triple-quoted f-string literal
        if ch == quote[0]:
            cnt = state.triple_close + 1
            if cnt == 3:
                return LexState(stack=stack[:-1], mask_partial=mask_partial)
            return state._replace(triple_close=cnt, mask_partial=mask_partial)
        return state._replace(triple_close=0, mask_partial=mask_partial)

    # 3. Inside an f-string format specifier
    if top == "FSTR_SPEC":
        if ch == "{":
            return LexState(stack=stack + (("FSTR_EXPR", False),), mask_partial=mask_partial)
        if ch == "}":
            return LexState(stack=stack[:-1], mask_partial=mask_partial)
        # On Python < 3.12, an unescaped outer single/double quote terminates the enclosing f-string early
        if py_lt_312 and len(stack) >= 2 and isinstance(stack[-2], tuple) and stack[-2][0] == "FSTR_LIT":
            outer_q = stack[-2][1]
            if len(outer_q) == 1 and ch == outer_q:
                return None
            if ch == "\\":
                return None
        return state._replace(mask_partial=mask_partial)

    # 4. Code context (top-level, inside (), [], {}, or inside FSTR_EXPR)
    in_fexpr_top = isinstance(top, tuple) and top[0] == "FSTR_EXPR"
    if in_fexpr_top and top[1]:
        # Immediately after '{' inside FSTR_LIT: a second '{' is an escaped literal '{{'
        if ch == "{":
            return LexState(stack=stack[:-1], mask_partial=mask_partial)
        # Otherwise lock this frame as a genuine replacement expression
        stack = stack[:-1] + (("FSTR_EXPR", False),)
        top = stack[-1]

    # Check if upgrading an immediately closed empty string '' or "" to triple-quoted ''' or """
    if state.just_closed_quote and ch == state.just_closed_quote:
        triple = ch * 3
        if py_lt_312 and _in_fstr_expr(stack) and triple in _forbidden_pre312_quotes(stack):
            return None
        return LexState(
            stack=stack + ((state.just_closed_kind, triple),),
            mask_partial=mask_partial,
        )

    # Opening a new string or f-string
    if ch in ("'", '"'):
        prefix_lower = state.prefix_buf.lower()
        if "t" in prefix_lower:
            # Python 3.14+ template strings: abstain rather than risk false rejection
            return LexState(stack=stack, abstained=True, mask_partial=mask_partial)
        kind = "FSTR_LIT" if "f" in prefix_lower else "STR"
        if py_lt_312 and _in_fstr_expr(stack):
            if ch in _forbidden_pre312_quotes(stack):
                return None
        # Use triple_close=-1 as a sentinel meaning "0 chars seen inside this 1-char quote so far"
        return LexState(
            stack=stack + ((kind, ch),),
            triple_close=-1,
            mask_partial=mask_partial,
        )

    # Backslash in code (normalized single-line statements never use line continuations,
    # and Python < 3.12 forbids '\' anywhere inside f-string expressions)
    if ch == "\\":
        return None

    # Comment '#' in code: abstain on any comment outside strings/format specs
    # (normalized single-line targets from ast.unparse have no comments, but abstaining
    # avoids falsely breaking unexpected '#' tokens if any appear)
    if ch == "#":
        return None

    # Colon directly inside FSTR_EXPR (bracket depth 0) transitions to FSTR_SPEC
    if ch == ":" and in_fexpr_top:
        return LexState(stack=stack[:-1] + ("FSTR_SPEC",), mask_partial=mask_partial)

    # Opening bracket / brace
    if ch in _OPEN_TO_CLOSE:
        return LexState(stack=stack + (ch,), mask_partial=mask_partial)

    # Closing bracket / brace
    if ch in _CLOSE_TO_OPEN:
        if ch == "}" and in_fexpr_top:
            return LexState(stack=stack[:-1], mask_partial=mask_partial)
        expected_open = _CLOSE_TO_OPEN[ch]
        if top != expected_open:
            return None
        return LexState(stack=stack[:-1], mask_partial=mask_partial)

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
    )


def step_atomic_mask(state: LexState, mask_idx: int, *, mask_count: int | None = None) -> LexState | None:
    """Advance ``state`` by an atomic ``<mask_N>`` token (treated as a placeholder, not '<'/'>')."""
    if mask_count is not None and mask_idx >= mask_count:
        return None
    if state.abstained:
        return state._replace(mask_partial="")
    stack = state.stack
    top = stack[-1] if stack else None
    if isinstance(top, tuple) and top[0] == "STR":
        return state._replace(in_escape=False, triple_close=0, mask_partial="")
    if isinstance(top, tuple) and top[0] == "FSTR_LIT":
        if state.pending_fbrace_close:
            return None
        return state._replace(in_escape=False, triple_close=0, mask_partial="")
    if top == "FSTR_SPEC":
        return state._replace(mask_partial="")
    if isinstance(top, tuple) and top[0] == "FSTR_EXPR" and top[1]:
        stack = stack[:-1] + (("FSTR_EXPR", False),)
    return LexState(
        stack=stack,
        prev_is_ident=True,
        mask_partial="",
    )


def step_text(state: LexState, text: str, *, py_lt_312: bool = False, mask_count: int | None = None) -> LexState | None:
    """Advance ``state`` through every character of ``text``."""
    cur: LexState | None = state
    for ch in text:
        cur = step_char(cur, ch, py_lt_312=py_lt_312, mask_count=mask_count)
        if cur is None:
            return None
    return cur


def is_eos_allowed(state: LexState) -> bool:
    """Whether EOS is allowed at ``state`` (no open brackets, strings, escapes, or pending '}')."""
    if state.abstained:
        return True
    return not state.stack and not state.in_escape and not state.pending_fbrace_close


def check_statement_constraints(text: str, *, py_lt_312: bool = False, mask_count: int | None = None) -> bool:
    """Check whether a complete masked statement satisfies all lexical and mask invariants."""
    state: LexState | None = INITIAL_STATE
    pos = 0
    for match in re.finditer(r"<mask_(\d+)>", text):
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
        # <extra_id_*>, control characters / raw newlines / invalid UTF-8.
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
        self.active_ids: list[int] = []
        self.mask_spell_ids: list[int] = []
        self.inert_ids: list[int] = []

        for tid in range(self.vocab_size):
            if tid == self.eos_token_id:
                continue
            s = self.token_strings[tid]
            if _EXTRA_ID_RE.match(s):
                static_ban[tid] = True
                continue
            if not static_ban[tid]:
                if not s or any(ord(c) < 32 or ord(c) == 127 or c == "\ufffd" for c in s):
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

            # Only tokens containing syntax characters can fail lexical checks when
            # mask_partial is empty; tokens containing mask-spelling characters are only
            # checked individually while a "<mask_..." prefix is active.
            if any(c in _SYNTAX_CHARS for c in s):
                self.active_ids.append(tid)
            elif any(c in _MASK_SPELL_CHARS for c in s):
                self.mask_spell_ids.append(tid)
            else:
                self.inert_ids.append(tid)

        self.static_ban = static_ban
        self.atomic_mask_id_tensor = torch.tensor(self.atomic_mask_ids, dtype=torch.long)
        self.atomic_mask_num_tensor = torch.tensor(self.atomic_mask_nums, dtype=torch.long)
        self.mask_spell_id_tensor = torch.tensor(self.mask_spell_ids, dtype=torch.long)
        self.inert_id_tensor = torch.tensor(self.inert_ids, dtype=torch.long)
        self._mask_cache: OrderedDict[tuple, torch.Tensor] = OrderedDict()

    def step_token(self, state: LexState, tid: int, *, py_lt_312: bool, mask_count: int | None) -> LexState | None:
        """Advance ``state`` by token ID ``tid``."""
        if tid == self.eos_token_id or tid in self.special_non_output_ids:
            return state
        num = self.mask_id_to_num.get(tid)
        if num is not None:
            return step_atomic_mask(state, num, mask_count=mask_count)
        return step_text(state, self.token_strings[tid], py_lt_312=py_lt_312, mask_count=mask_count)

    def _abstract_key(self, state: LexState, py_lt_312: bool, mask_count: int | None) -> tuple:
        if state.abstained:
            return ("ABSTAINED", state.mask_partial, mask_count if state.mask_partial else None)
        # Only the top _STACK_CACHE_WINDOW frames plus pre-3.12 f-string context affect one-token transitions.
        tail = state.stack[-_STACK_CACHE_WINDOW:]
        has_deeper = len(state.stack) > _STACK_CACHE_WINDOW
        fexpr = _in_fstr_expr(state.stack) if py_lt_312 else False
        forb = _forbidden_pre312_quotes(state.stack) if fexpr else frozenset()
        return (
            tail,
            has_deeper,
            state.in_escape,
            state.triple_close,
            state.prefix_buf.lower(),
            state.prev_is_ident,
            state.just_closed_kind,
            state.just_closed_quote,
            state.pending_fbrace_close,
            state.mask_partial,
            mask_count if state.mask_partial else None,
            py_lt_312,
            fexpr,
            forb,
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

        # Inert tokens: check one representative non-syntax identifier-like string ("z")
        inert_ok = step_text(state, "z", py_lt_312=py_lt_312, mask_count=mask_count) is not None
        if not inert_ok:
            if self.inert_ids:
                ban[self.inert_id_tensor] = True
            if self.mask_spell_ids and not state.mask_partial:
                ban[self.mask_spell_id_tensor] = True

        # Atomic masks are valid unless pending_fbrace_close is waiting specifically for '}'
        if self.atomic_mask_ids and state.pending_fbrace_close:
            ban[self.atomic_mask_id_tensor] = True

        # Check the small active subset (~150 syntax tokens)
        for tid in self.active_ids:
            if step_text(state, self.token_strings[tid], py_lt_312=py_lt_312, mask_count=mask_count) is None:
                ban[tid] = True

        # Check mask-spelling tokens individually only while "<mask_..." is actively being spelled
        if state.mask_partial:
            for tid in self.mask_spell_ids:
                if step_text(state, self.token_strings[tid], py_lt_312=py_lt_312, mask_count=mask_count) is None:
                    ban[tid] = True

        self._mask_cache[key] = ban
        if len(self._mask_cache) > _MAX_MASK_CACHE:
            self._mask_cache.popitem(last=False)
        return ban


class StatementLogitsProcessor:
    """HuggingFace-compatible LogitsProcessor enforcing statement lexical & mask invariants.

    Beam-search safe: tracks immutable ``LexState`` keyed by generated token prefix so
    reordering/forking beams never corrupts state.
    """

    def __init__(
        self,
        index: TokenizerConstraintIndex,
        mask_counts: list[int | None],
        *,
        py_lt_312: bool = False,
        num_beams: int = 1,
    ):
        self.index = index
        self.mask_counts = mask_counts
        self.py_lt_312 = py_lt_312
        self.num_beams = num_beams
        # Per-request prefix -> LexState caches: list of dicts, one per original batch item
        self._prefix_states: list[dict[tuple[int, ...], LexState]] = [{(): INITIAL_STATE} for _ in mask_counts]
        self._device_static_ban: dict[torch.device, torch.Tensor] = {}
        self._device_atomic_ids: dict[torch.device, torch.Tensor] = {}
        self._device_atomic_nums: dict[torch.device, torch.Tensor] = {}
        self._request_mask_bans: dict[tuple[torch.device, int], torch.Tensor] = {}

    def _get_atomic_mask_ban(self, device: torch.device, mask_count: int) -> torch.Tensor | None:
        if not self.index.atomic_mask_ids:
            return None
        key = (device, mask_count)
        cached = self._request_mask_bans.get(key)
        if cached is not None:
            return cached
        if device not in self._device_atomic_ids:
            self._device_atomic_ids[device] = self.index.atomic_mask_id_tensor.to(device)
            self._device_atomic_nums[device] = self.index.atomic_mask_num_tensor.to(device)
        banned_ids = self._device_atomic_ids[device][self._device_atomic_nums[device] >= mask_count]
        self._request_mask_bans[key] = banned_ids
        return banned_ids

    def _state_for_prefix(self, req_idx: int, prefix: tuple[int, ...], mask_count: int | None) -> LexState:
        cache = self._prefix_states[req_idx]
        found = cache.get(prefix)
        if found is not None:
            return found
        # Walk back to the longest cached prefix and step forward
        cur_len = len(prefix) - 1
        while cur_len > 0 and prefix[:cur_len] not in cache:
            cur_len -= 1
        state = cache[prefix[:cur_len]]
        for step_idx in range(cur_len, len(prefix)):
            tid = prefix[step_idx]
            nxt = self.index.step_token(state, tid, py_lt_312=self.py_lt_312, mask_count=mask_count)
            # If an earlier liveness fallback emitted an out-of-grammar token, abstain cleanly
            state = nxt if nxt is not None else LexState(abstained=True)
            cache[prefix[: step_idx + 1]] = state
        return state

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        batch_beams, vocab_size = scores.shape
        device = scores.device
        eos_id = self.index.eos_token_id
        num_reqs = len(self.mask_counts)
        beams_per_req = max(1, batch_beams // num_reqs) if num_reqs else 1

        if device not in self._device_static_ban:
            self._device_static_ban[device] = self.index.static_ban.to(device)
        static_ban_dev = self._device_static_ban[device]

        for row in range(batch_beams):
            req_idx = row // beams_per_req if num_reqs else 0
            mask_count = self.mask_counts[req_idx] if req_idx < num_reqs else None

            # T5 starts with decoder_start_token_id at position 0; strip it for lexical state
            seq = input_ids[row, 1:].tolist()
            if eos_id is not None and eos_id in seq:
                # Already finished beam/sequence: leave untouched so HF can pad cleanly
                continue

            state = self._state_for_prefix(req_idx, tuple(seq), mask_count)
            row_scores = scores[row]
            ban = self.index.disallowed_mask(state, py_lt_312=self.py_lt_312, mask_count=mask_count).to(device)
            if vocab_size != ban.shape[0]:
                # Defensive guard if model embedding vocab differs slightly from tokenizer length
                effective = torch.zeros(vocab_size, dtype=torch.bool, device=device)
                n = min(vocab_size, ban.shape[0])
                effective[:n] = ban[:n]
                ban = effective

            if mask_count is not None:
                oob_ids = self._get_atomic_mask_ban(device, mask_count)
                if oob_ids is not None and oob_ids.numel() > 0:
                    ban = ban.clone()
                    ban[oob_ids[oob_ids < vocab_size]] = True

            # Allow BOS (<s>) at step 0 right after T5's decoder_start_token_id
            if not seq and self.index.allowed_initial_special_ids:
                ban = ban.clone()
                for bos_tid in self.index.allowed_initial_special_ids:
                    if bos_tid < vocab_size:
                        ban[bos_tid] = False

            masked = row_scores.masked_fill(ban, float("-inf"))
            # Mandatory liveness guard: never leave all logits -inf (causes NaN in beam log_softmax)
            if torch.isneginf(masked).all():
                fallback_ban = static_ban_dev[:vocab_size] if static_ban_dev.shape[0] >= vocab_size else static_ban_dev
                if fallback_ban.shape[0] == vocab_size:
                    masked = row_scores.masked_fill(fallback_ban, float("-inf"))
                if torch.isneginf(masked).all():
                    masked = row_scores
            scores[row] = masked

        return scores
