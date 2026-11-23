"""Tests for CacheTranslator constraints, cap-exhaustion retry, safe backoff, and Decompiler beam retry."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import torch
from tokenizers import Tokenizer, models as token_models, pre_tokenizers
from transformers import PreTrainedTokenizerFast

from pylingual.decompiler import Decompiler
from pylingual.control_flow_reconstruction.source import SourceLine
from pylingual.models import CacheTranslator, _TRANSLATION_FALLBACK
from pylingual.utils.version import PythonVersion


def _make_tok():
    vocab = [
        "<pad>",  # 0
        "<s>",  # 1
        "</s>",  # 2
        "<unk>",  # 3
        "<mask>",  # 4
        "LOAD_CONST",  # 5
        "<opcode:LOAD_CONST>",  # 6
        "<opcode:FORMAT_VALUE>",  # 7
        "<mask_0>",  # 8
        "<mask_1>",  # 9
        "x",  # 10
        "=",  # 11
        "(",  # 12
        ")",  # 13
        "v3.11",  # 14
        "<SEP>",  # 15
    ]
    backend = Tokenizer(token_models.WordLevel({t: i for i, t in enumerate(vocab)}, unk_token="<unk>"))
    backend.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    return PreTrainedTokenizerFast(
        tokenizer_object=backend,
        pad_token="<pad>",
        bos_token="<s>",
        eos_token="</s>",
        unk_token="<unk>",
        mask_token="<mask>",
    )


class _StubGenModel(torch.nn.Module):
    def __init__(self, tok, fn):
        super().__init__()
        self.embedding = torch.nn.Embedding(len(tok), 1)
        self.generation_config = SimpleNamespace(bad_words_ids=[[6], [7]])
        self.config = SimpleNamespace(pylingual_version_prefix=False)
        self._fn = fn
        self.calls = []

    def get_input_embeddings(self):
        return self.embedding

    def generate(self, **kwargs):
        self.calls.append(kwargs)
        return self._fn(**kwargs)


def test_cap_exhaustion_retries_once_at_retry_max_length():
    tok = _make_tok()

    def gen(**kwargs):
        ml = kwargs["max_length"]
        if ml == 4:
            # Hit max_length=4 without EOS (token id 2)
            return torch.tensor([[0, 10, 11, 12]])
        return torch.tensor([[0, 10, 11, 12, 8, 13, 2]])

    model = _StubGenModel(tok, gen)
    translator = CacheTranslator(model, tok, cache_namespace="stmt@rev", max_length=4, retry_max_length=12)
    out = translator(["LOAD_CONST <mask_0>"], version=PythonVersion((3, 12)))
    assert len(model.calls) == 2
    assert model.calls[0]["max_length"] == 4
    assert model.calls[1]["max_length"] == 12
    assert out == ["x = ( <mask_0> )"]


def test_programming_error_surfaces_while_oom_backs_off_without_caching():
    tok = _make_tok()

    def raise_value_error(**kwargs):
        raise ValueError("processor bug")

    buggy = _StubGenModel(tok, raise_value_error)
    tr_buggy = CacheTranslator(buggy, tok, cache_namespace="stmt@rev")
    with pytest.raises(ValueError, match="processor bug"):
        tr_buggy(["LOAD_CONST <mask_0>"])

    oom_calls = 0

    def raise_oom(**kwargs):
        nonlocal oom_calls
        oom_calls += 1
        raise MemoryError("simulated OOM")

    oom_model = _StubGenModel(tok, raise_oom)
    tr_oom = CacheTranslator(oom_model, tok, cache_namespace="stmt@rev")
    out = tr_oom(["LOAD_CONST <mask_0>"])
    assert out == [_TRANSLATION_FALLBACK]
    assert len(tr_oom.cache) == 0  # Fallback string must NOT be cached


def test_version_prefix_and_pre312_cache_key_isolation():
    tok = _make_tok()
    model = _StubGenModel(tok, lambda **kwargs: torch.tensor([[0, 8, 2]] * kwargs["input_ids"].shape[0]))
    tr = CacheTranslator(model, tok, cache_namespace="stmt@rev", use_version_prefix=False)
    # Non-fstring shares cache across 3.11 and 3.12
    assert tr._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 11))) == tr._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 12)))
    # F-string isolates pre-3.12 from 3.12+
    assert tr._cache_key("FORMAT_VALUE <mask_0>", PythonVersion((3, 11))) != tr._cache_key("FORMAT_VALUE <mask_0>", PythonVersion((3, 12)))

    # Version-prefixed model always includes version in encoder input and cache key
    tr_vp = CacheTranslator(model, tok, cache_namespace="stmt@rev", use_version_prefix=True)
    assert tr_vp._format_encoder_input("LOAD_CONST <mask_0>", PythonVersion((3, 11))).startswith("v3.11 <SEP> <opcode:LOAD_CONST>")
    assert tr_vp._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 11))) != tr_vp._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 12)))


def test_translate_beam_deduplicates_and_does_not_mutate_cache():
    tok = _make_tok()

    def gen(**kwargs):
        assert kwargs["num_beams"] == 3
        assert kwargs["num_return_sequences"] == 3
        return torch.tensor([[0, 8, 2], [0, 8, 2], [0, 10, 2]])

    model = _StubGenModel(tok, gen)
    tr = CacheTranslator(model, tok, cache_namespace="stmt@rev")
    cands = tr.translate_beam(["LOAD_CONST <mask_7>"], num_beams=3, version=PythonVersion((3, 12)))
    assert cands == [["<mask_7>", "x"]]
    assert len(tr.cache) == 0


def test_decompiler_beam_retry_fixes_suspect_statement_and_preserves_cache():
    d = Decompiler.__new__(Decompiler)
    d.name = "beam-retry-test"
    d.version = PythonVersion((3, 12))
    d.check_timeout = Mock()
    fake_co = object()
    fake_bc = SimpleNamespace(codeobj=fake_co, name="f")
    d.ordered_bytecodes = [fake_bc]
    d.ordered_instructions = [[]]
    d.codeobj_instruction_lists = [["LOAD_CONST <mask_0>"]]
    d.segmentation_results = [[{"entity": "B", "score": 1.0}]]
    d.translation_results = [["x = ("]]
    d.source_lines = ["x = ("]
    d.indented_source = "x = ("
    d.equivalence_results = [Exception("SyntaxError: line 1")]

    orig_cft = SimpleNamespace(header_lines=[SourceLine("global g", 0, fake_co)])

    class FakeContext:
        def __init__(self):
            self.cfts = {fake_co: orig_cft}
            self.cache = {}

        def snapshot(self):
            return (dict(self.cfts), list(d.source_lines))

        def restore(self, snap):
            self.cache.clear()

        def update_lines(self, lines):
            self.lines = list(lines)

    d.source_context = FakeContext()
    d.update_source_lines = lambda: setattr(d, "source_lines", list(d.translation_results[0]))
    d.unmask_lines = lambda: None
    d.reconstruct_source = lambda: setattr(d, "indented_source", "\n".join(d.source_lines))
    d.check_reconstruction = lambda src: [SimpleNamespace(success=(src == "x = 1"), bc_a=fake_bc)] if src == "x = 1" else [Exception("SyntaxError: line 1")]
    d.translator = SimpleNamespace(translate_beam=lambda reqs, **kw: [["x = (", "x = 1"]])

    import pylingual.decompiler as dec_mod

    orig_bc_to_cft = dec_mod.bc_to_cft
    dec_mod.bc_to_cft = lambda bc, lines: SimpleNamespace(header_lines=[])
    try:
        fixed = d.correct_translation_beam(0, SourceLine("x = (", 0, fake_co))
    finally:
        dec_mod.bc_to_cft = orig_bc_to_cft

    assert fixed is True
    assert d.translation_results[0] == ["x = 1"]
    assert d.indented_source == "x = 1"
    assert d.source_context.cfts[fake_co].header_lines == orig_cft.header_lines
