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


def _make_bpe_like_tokenizer():
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
    ]
    for s in invalid:
        assert not check_statement_constraints(s, py_lt_312=False, mask_count=3), f"should reject: {s}"


def test_pre312_fstring_quote_and_backslash_rules():
    # Forbidden on < 3.12
    assert not check_statement_constraints("x = f'{d['k']}'", py_lt_312=True)
    assert not check_statement_constraints('x = f"{d["k"]}"', py_lt_312=True)
    assert not check_statement_constraints("x = f'{d[\"\\n\"]}'", py_lt_312=True)
    assert not check_statement_constraints("x = f'''{'''a'''}'''", py_lt_312=True)

    # Allowed on < 3.12 (different quote or single quote inside triple-quoted f-string)
    assert check_statement_constraints("x = f'{d[\"k\"]}'", py_lt_312=True)
    assert check_statement_constraints('x = f"{d[\'k\']}"', py_lt_312=True)
    assert check_statement_constraints("x = f'''{'a'}'''", py_lt_312=True)
    assert check_statement_constraints("x = f'\\n{a}'", py_lt_312=True)

    # Allowed on >= 3.12 (PEP 701)
    assert check_statement_constraints("x = f'{d['k']}'", py_lt_312=False)
    assert check_statement_constraints("x = f'{d[\"\\n\"]}'", py_lt_312=False)


def test_prefix_not_triggered_after_identifier():
    # `if'a'` has `if` as an identifier before `'`, so it opens a plain STR, not FSTR_LIT
    st = step_text(INITIAL_STATE, "if'{")
    assert st is not None
    assert st.stack == (("STR", "'"),)
    # `= f'{` has `f` after non-identifier, so it opens FSTR_LIT then FSTR_EXPR
    st2 = step_text(INITIAL_STATE, "= f'{")
    assert st2 is not None
    assert st2.stack == (("FSTR_LIT", "'"), ("FSTR_EXPR", True))


def test_template_string_abstains_cleanly():
    assert check_statement_constraints("x = t'hello {name}'", py_lt_312=False)


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
    # BOS (<s>) allowed at step 0 (T5 predicts <s> right after decoder_start_token_id), banned after step 0
    assert torch.isfinite(out[0, ids["<s>"]])
    out_step1 = proc(torch.tensor([[0, ids["<s>"]]], dtype=torch.long), scores.clone())
    assert torch.isneginf(out_step1[0, ids["<s>"]])
    # Mask 0 allowed, masks 1 and 2 banned
    assert torch.isfinite(out[0, ids["<mask_0>"]])
    assert torch.isneginf(out[0, ids["<mask_1>"]])
    assert torch.isneginf(out[0, ids["<mask_2>"]])
    # Unmatched closer ')' banned at root
    assert torch.isneginf(out[0, ids[")"]])

    # Spelled-out "<mask_" prefix: digit '0' allowed, digit '1' and '5' banned when mask_count=1
    spelled_prefix = torch.tensor([[0, ids["<"], ids["mask"], ids["_"]]], dtype=torch.long)
    out2 = proc(spelled_prefix, scores.clone())
    assert torch.isfinite(out2[0, ids["0"]])
    assert torch.isneginf(out2[0, ids["1"]])
    assert torch.isneginf(out2[0, ids["5"]])


def test_logits_processor_forbids_eos_when_unclosed_and_tracks_beams():
    tok, ids = _make_bpe_like_tokenizer()
    index = TokenizerConstraintIndex(tok)
    # 1 request, 2 beams: beam 0 has open '(', beam 1 has closed '()'
    proc = StatementLogitsProcessor(index, mask_counts=[2], py_lt_312=False, num_beams=2)
    input_ids = torch.tensor(
        [
            [0, ids["("], ids["x"]],
            [0, ids["("], ids[")"]],
        ],
        dtype=torch.long,
    )
    scores = torch.zeros((2, len(tok)), dtype=torch.float32)
    out = proc(input_ids, scores.clone())

    # Beam 0: EOS and ']' disallowed, ')' allowed
    assert torch.isneginf(out[0, ids["</s>"]])
    assert torch.isneginf(out[0, ids["]"]])
    assert torch.isfinite(out[0, ids[")"]])
    # Beam 1: EOS allowed, ')' disallowed
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
        "f'a}",
        "'abc\\",
        "<mask_",
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
                    assert bool(fast[tid]) == expected_ban, f"mismatch tid={tid} ({index.token_strings[tid]!r}) prefix={prefix!r} py_lt_312={py_lt_312} mask_count={mask_count}"

