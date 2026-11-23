"""Unit tests for lexical & mask-reference translation constraints."""

from __future__ import annotations

import torch
from tokenizers import Tokenizer, models as token_models, pre_tokenizers
from transformers import PreTrainedTokenizerFast

from pylingual.translation_constraints import (
    INITIAL_STATE,
    StatementLogitsProcessor,
    TokenizerConstraintIndex,
    check_statement_constraints,
    is_eos_allowed,
    step_text,
)


def _make_bpe_like_tokenizer(extra_tokens: list[str] | None = None):
    vocab_list = [
        "<pad>",  # 0
        "<s>",  # 1
        "</s>",  # 2
        "<unk>",  # 3
        "<mask>",  # 4
        "(",  # 5
        ")",  # 6
        "[",  # 7
        "]",  # 8
        "{",  # 9
        "}",  # 10
        "'",  # 11
        '"',  # 12
        "\\",  # 13
        "#",  # 14
        ":",  # 15
        "=",  # 16
        "f",  # 17
        "r",  # 18
        "t",  # 19
        "x",  # 20
        "def",  # 21
        "if",  # 22
        "<mask_0>",  # 23
        "<mask_1>",  # 24
        "<mask_2>",  # 25
        "<extra_id_0>",  # 26
        "<opcode:LOAD_CONST>",  # 27
        "\n",  # 28
        "():",  # 29
        ">'})",  # 30
        "('<",  # 31
        "mask",  # 32
        "_",  # 33
        "0",  # 34
        "1",  # 35
        "5",  # 36
        ">",  # 37
        "<",  # 38
        " ",  # 39
        ":=",  # 40
    ]
    if extra_tokens:
        vocab_list.extend(extra_tokens)
    backend = Tokenizer(token_models.WordLevel({t: i for i, t in enumerate(vocab_list)}, unk_token="<unk>"))
    backend.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    tok = PreTrainedTokenizerFast(
        tokenizer_object=backend,
        pad_token="<pad>",
        bos_token="<s>",
        eos_token="</s>",
        unk_token="<unk>",
        mask_token="<mask>",
    )
    return tok, {t: i for i, t in enumerate(vocab_list)}


def test_balanced_brackets_and_quotes_accepted():
    valid = [
        "x = (<mask_0>, [<mask_1>], {'<mask_2>': 1})",
        "def <mask_0>(<mask_1>: <mask_2>=None) -> <mask_3>:",
        "x = r'\\'' + '''<mask_0>'''",
        "x = f'<mask_0>{{<mask_1>}}{<mask_2>:#x}'",
        "x = f'{<mask_0>:=10}'",
        "x = f'{ {1: 2} }'",
        "x = f'{(a := 1)}'",
        "from <mask_0><mask_1> import <mask_2>",
        "@<mask_0>",
        "elif <mask_0>:",
        "case <mask_0>:",
    ]
    for s in valid:
        assert check_statement_constraints(s, py_lt_312=False, mask_count=5), f"falsely rejected: {s}"


def test_unclosed_and_mismatched_delimiters_rejected():
    invalid = [
        "x = (<mask_0>",
        "x = (<mask_0>]",
        "x = <mask_0>)",
        "x = '<mask_0>",
        "x = '''<mask_0>''",
        "x = r'\\'",
        "x = f'{<mask_0>'",
        "x = f'<mask_0>}'",
        "x = f'<mask_0>{<mask_1>}}'",
        "x = <mask_5>",
        "x = <mask_01>",
        "x = 1\ny = 2",
        "x = <extra_id_0>",
    ]
    for s in invalid:
        assert not check_statement_constraints(s, py_lt_312=False, mask_count=3), f"should reject: {s}"


def test_fstring_escape_format_spec_and_pre312_rules():
    # Valid on Python 3.11 and 3.12+: backslash does NOT escape '{' or '}' in f-string literals,
    # and backslashes + escaped outer quotes are legal in top-level format specs.
    valid_311 = [
        r'f"\{x}"',
        r'rf"\{x}"',
        r'rf"C:\{subdir}\file"',
        r'f"{1:\x3e10}"',
        r'f"{1:\n}"',
        r'f"{x:\>8}"',
        r'f"{1:\"}"',
        "f'{1:\\'}'",
        "x = f'{d[\"k\"]}'",
        'x = f"{d[\'k\']}"',
        "x = f'''{'a'}'''",
        "x = f'\\n{a}'",
        r'f"{1:\{a}}"',
    ]
    for s in valid_311:
        assert check_statement_constraints(s, py_lt_312=True), f"falsely rejected on <3.12: {s}"
        assert check_statement_constraints(s, py_lt_312=False), f"falsely rejected on >=3.12: {s}"

    # Invalid on all Python versions
    assert not check_statement_constraints(r'f"a\}"', py_lt_312=True)
    assert not check_statement_constraints(r'f"a\}"', py_lt_312=False)

    # Forbidden on Python < 3.12 (including nested f-string literals & nested specs with backslashes)
    invalid_311 = [
        "x = f'{d['k']}'",
        'x = f"{d["k"]}"',
        "x = f'{d[\"\\n\"]}'",
        "x = f'''{'''a'''}'''",
        "f\"{f'\\n'}\"",
        "f\"{f'{1:\\n}'}\"",
        "f\"{1:{'\\\\'}}\"",
    ]
    for s in invalid_311:
        assert not check_statement_constraints(s, py_lt_312=True), f"should reject on <3.12: {s}"

    # Allowed on >= 3.12 (PEP 701)
    assert check_statement_constraints("x = f'{d['k']}'", py_lt_312=False)
    assert check_statement_constraints("x = f'{d[\"\\n\"]}'", py_lt_312=False)
    assert check_statement_constraints("f\"{f'\\n'}\"", py_lt_312=False)


def test_multi_piece_mask_defers_until_closing_angle_and_handles_unicode_digits():
    # Must NOT reject before '>' closes a canonical <mask_N>
    assert check_statement_constraints("x=a<mask_2", mask_count=0)
    assert check_statement_constraints("x = '<mask_'", mask_count=0)
    assert check_statement_constraints("x = '<mask_9x'", mask_count=2)
    assert check_statement_constraints("x = '<mask_01x'", mask_count=5)
    # Non-ASCII Unicode digit '²' must not raise ValueError
    assert check_statement_constraints("x = '<mask_\u00b2>'", mask_count=2)
    # Complete out-of-range or leading-zero masks ARE rejected when '>' closes them
    assert not check_statement_constraints("x = <mask_2>", mask_count=2)
    assert not check_statement_constraints("x = <mask_01>", mask_count=5)


def test_prefix_not_triggered_after_identifier():
    st = step_text(INITIAL_STATE, "if'{")
    assert st is not None
    assert st.stack == (("STR", "'"),)
    st2 = step_text(INITIAL_STATE, "= f'{")
    assert st2 is not None
    assert st2.stack == (("FSTR_LIT", "'"), ("FSTR_EXPR", True))


def test_template_string_abstains_cleanly():
    assert check_statement_constraints("x = t'hello {name}'", py_lt_312=False)


def test_utf8_byte_bpe_pieces_not_banned():
    # Simulate a byte-BPE tokenizer where individual byte pieces decode to U+FFFD in isolation
    tok, ids = _make_bpe_like_tokenizer(["\ufffd", "é", "😀"])
    index = TokenizerConstraintIndex(tok)
    assert not bool(index.static_ban[ids["\ufffd"]])
    assert not bool(index.static_ban[ids["é"]])
    assert not bool(index.static_ban[ids["😀"]])
    assert index.check_token_sequence([ids["x"], ids["="], ids["'"], ids["\ufffd"], ids["'"], ids["</s>"]])


def test_cache_key_soundness_for_deep_stacks_and_inline_masks():
    # Deep closer token: 7 closing parens must distinguish stack '(((((((' from '[(((((('
    tok, ids = _make_bpe_like_tokenizer([")))))))", "<mask_9>x"])
    index = TokenizerConstraintIndex(tok)
    assert index.stack_cache_window >= 8

    st_all_parens = step_text(INITIAL_STATE, "(((((((")
    st_bracket_bottom = step_text(INITIAL_STATE, "[((((((")
    assert st_all_parens is not None and st_bracket_bottom is not None
    ban_parens = index.disallowed_mask(st_all_parens, py_lt_312=False, mask_count=5)
    ban_bracket = index.disallowed_mask(st_bracket_bottom, py_lt_312=False, mask_count=5)
    assert not bool(ban_parens[ids[")))))))"]])
    assert bool(ban_bracket[ids[")))))))"]])

    # Inline mask token '<mask_9>x': cache key must include mask_count even when mask_partial == ""
    ban_mc1 = index.disallowed_mask(INITIAL_STATE, py_lt_312=False, mask_count=1)
    ban_mc10 = index.disallowed_mask(INITIAL_STATE, py_lt_312=False, mask_count=10)
    assert bool(ban_mc1[ids["<mask_9>x"]])
    assert not bool(ban_mc10[ids["<mask_9>x"]])


def test_logits_processor_masks_oob_atomic_and_spelled_masks():
    tok, ids = _make_bpe_like_tokenizer()
    index = TokenizerConstraintIndex(tok, bad_words_ids=[[ids["<opcode:LOAD_CONST>"]]])
    proc = StatementLogitsProcessor(index, mask_counts=[1], py_lt_312=True)

    # At start of sequence (decoder_start_token_id = 0)
    input_ids = torch.tensor([[0]], dtype=torch.long)
    scores = torch.zeros((1, len(tok)), dtype=torch.float32)
    out = proc(input_ids, scores.clone())

    # Static bans applied
    assert torch.isneginf(out[0, ids["<opcode:LOAD_CONST>"]])
    assert torch.isneginf(out[0, ids["<extra_id_0>"]])
    assert torch.isneginf(out[0, ids["\n"]])
    # BOS (<s>) allowed at step 0, banned after step 0
    assert torch.isfinite(out[0, ids["<s>"]])
    out_step1 = proc(torch.tensor([[0, ids["<s>"]]], dtype=torch.long), scores.clone())
    assert torch.isneginf(out_step1[0, ids["<s>"]])
    # Mask 0 allowed, masks 1 and 2 banned
    assert torch.isfinite(out[0, ids["<mask_0>"]])
    assert torch.isneginf(out[0, ids["<mask_1>"]])
    assert torch.isneginf(out[0, ids["<mask_2>"]])
    # Unmatched closer ')' banned at root
    assert torch.isneginf(out[0, ids[")"]])

    # Spelled-out "<mask_1" prefix: '>' is banned when mask_count=1, but digits stay allowed for non-mask text
    spelled_oob = torch.tensor([[0, ids["<"], ids["mask"], ids["_"], ids["1"]]], dtype=torch.long)
    out2 = proc(spelled_oob, scores.clone())
    assert torch.isneginf(out2[0, ids[">"]])
    assert torch.isfinite(out2[0, ids["x"]])

    # Spelled-out "<mask_0" prefix: '>' is allowed when mask_count=1
    spelled_ok = torch.tensor([[0, ids["<"], ids["mask"], ids["_"], ids["0"]]], dtype=torch.long)
    out3 = proc(spelled_ok, scores.clone())
    assert torch.isfinite(out3[0, ids[">"]])


def test_logits_processor_liveness_fallback_preserves_oob_mask_ban():
    tok, ids = _make_bpe_like_tokenizer()
    index = TokenizerConstraintIndex(tok)
    proc = StatementLogitsProcessor(index, mask_counts=[1], py_lt_312=False)

    # All lexically valid tokens are pre-masked to -inf; only ')' (lexically invalid) and '<mask_2>' (OOB) have finite scores
    scores = torch.full((1, len(tok)), float("-inf"), dtype=torch.float32)
    scores[0, ids[")"]] = 1.0
    scores[0, ids["<mask_2>"]] = 5.0
    out = proc(torch.tensor([[0]], dtype=torch.long), scores)
    # Fallback releases lexical ban on ')' for liveness, while keeping OOB '<mask_2>' banned
    assert torch.isfinite(out[0, ids[")"]])
    assert torch.isneginf(out[0, ids["<mask_2>"]])


def test_logits_processor_forbids_eos_when_unclosed_and_tracks_beams():
    tok, ids = _make_bpe_like_tokenizer()
    index = TokenizerConstraintIndex(tok)
    proc = StatementLogitsProcessor(index, mask_counts=[2], py_lt_312=False)
    input_ids = torch.tensor(
        [
            [0, ids["("], ids["x"]],
            [0, ids["("], ids[")"]],
        ],
        dtype=torch.long,
    )
    scores = torch.zeros((2, len(tok)), dtype=torch.float32)
    out = proc(input_ids, scores.clone())

    assert torch.isneginf(out[0, ids["</s>"]])
    assert torch.isneginf(out[0, ids["]"]])
    assert torch.isfinite(out[0, ids[")"]])
    assert torch.isfinite(out[1, ids["</s>"]])
    assert torch.isneginf(out[1, ids[")"]])


def test_logits_processor_leaves_finished_sequences_untouched():
    tok, ids = _make_bpe_like_tokenizer()
    index = TokenizerConstraintIndex(tok)
    proc = StatementLogitsProcessor(index, mask_counts=[1], py_lt_312=False)
    input_ids = torch.tensor([[0, ids["x"], ids["</s>"]]], dtype=torch.long)
    scores = torch.ones((1, len(tok)), dtype=torch.float32)
    out = proc(input_ids, scores.clone())
    assert torch.equal(out, scores)


def test_fast_disallowed_mask_matches_exhaustive_reference():
    tok, ids = _make_bpe_like_tokenizer()
    index = TokenizerConstraintIndex(tok, bad_words_ids=[[ids["<opcode:LOAD_CONST>"]]])
    prefixes = [
        "",
        "(",
        "f'",
        "f'{",
        "f'{x:",
        "f'{x:\\",
        "f'a}",
        "'abc\\",
        "<",
        "<mask_",
        "<mask_0",
        "<mask_1",
        "''",
    ]
    for py_lt_312 in (False, True):
        for mask_count in (0, 1, 2):
            for prefix in prefixes:
                state = step_text(INITIAL_STATE, prefix, py_lt_312=py_lt_312, mask_count=mask_count)
                if state is None:
                    continue
                fast = index.disallowed_mask(state, py_lt_312=py_lt_312, mask_count=mask_count)
                for tid in range(len(tok)):
                    if tid in index.mask_id_to_num:
                        continue  # atomic mask bounds are applied per request in StatementLogitsProcessor
                    if tid == index.eos_token_id:
                        expected_ban = not is_eos_allowed(state)
                    elif index.static_ban[tid]:
                        expected_ban = True
                    else:
                        expected_ban = step_text(state, index.token_strings[tid], py_lt_312=py_lt_312, mask_count=mask_count) is None
                    assert bool(fast[tid]) == expected_ban, (
                        f"mismatch tid={tid} ({index.token_strings[tid]!r}) prefix={prefix!r} py_lt_312={py_lt_312} mask_count={mask_count}"
                    )
