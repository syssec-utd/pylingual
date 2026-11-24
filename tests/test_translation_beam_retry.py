"""Tests for CacheTranslator constraints, cap-exhaustion retry, safe backoff, and Decompiler beam retry."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import torch
from tokenizers import Tokenizer, models as token_models, pre_tokenizers
from transformers import PreTrainedTokenizerFast

from pylingual.control_flow_reconstruction.source import SourceLine
from pylingual.decompiler import Decompiler
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


def test_cap_exhaustion_retries_once_and_never_caches_unfinished():
    tok = _make_tok()

    def gen_finishes(**kwargs):
        ml = kwargs["max_length"]
        if ml == 4:
            return torch.tensor([[0, 10, 11, 12]])
        return torch.tensor([[0, 10, 11, 12, 8, 13, 2]])

    model = _StubGenModel(tok, gen_finishes)
    translator = CacheTranslator(model, tok, cache_namespace="stmt@rev", max_length=4, retry_max_length=12)
    out = translator(["LOAD_CONST <mask_0>"], version=PythonVersion((3, 12)))
    assert len(model.calls) == 2
    assert model.calls[0]["max_length"] == 4
    assert model.calls[1]["max_length"] == 12
    assert out == ["x = ( <mask_0> )"]
    assert len(translator.cache) == 1

    # If even the retry lacks natural EOS, return text but NEVER cache it
    def gen_never_finishes(**kwargs):
        return torch.tensor([[0, 10, 11, 12, 8]])

    model2 = _StubGenModel(tok, gen_never_finishes)
    translator2 = CacheTranslator(model2, tok, cache_namespace="stmt@rev", max_length=4, retry_max_length=8)
    out2 = translator2(["LOAD_CONST <mask_0>"], version=PythonVersion((3, 12)))
    assert out2 == ["x = ( <mask_0>"]
    assert len(translator2.cache) == 0

    # If a liveness-fallback EOS output violates lexical constraints (e.g. stray ')'), never cache it
    model3 = _StubGenModel(tok, lambda **kwargs: torch.tensor([[0, 13, 2]]))
    translator3 = CacheTranslator(model3, tok, cache_namespace="stmt@rev")
    out3 = translator3(["LOAD_CONST <mask_0>"], version=PythonVersion((3, 12)))
    assert out3 == [")"]
    assert len(translator3.cache) == 0


def test_programming_error_surfaces_while_oom_backs_off_without_caching():
    tok = _make_tok()

    def raise_value_error(**kwargs):
        raise ValueError("processor bug")

    buggy = _StubGenModel(tok, raise_value_error)
    tr_buggy = CacheTranslator(buggy, tok, cache_namespace="stmt@rev")
    with pytest.raises(ValueError, match="processor bug"):
        tr_buggy(["LOAD_CONST <mask_0>"])

    def raise_oom(**kwargs):
        raise MemoryError("simulated OOM")

    oom_model = _StubGenModel(tok, raise_oom)
    tr_oom = CacheTranslator(oom_model, tok, cache_namespace="stmt@rev")
    out = tr_oom(["LOAD_CONST <mask_0>"])
    assert out == [_TRANSLATION_FALLBACK]
    assert len(tr_oom.cache) == 0


def test_version_prefix_and_pre312_cache_key_isolation():
    tok = _make_tok()
    model = _StubGenModel(tok, lambda **kwargs: torch.tensor([[0, 8, 2]] * kwargs["input_ids"].shape[0]))
    tr = CacheTranslator(model, tok, cache_namespace="stmt@rev", use_version_prefix=False)
    # Pre-3.12 constraints apply to every output, so 3.11 and 3.12 cache keys are always isolated
    assert tr._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 11))) != tr._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 12)))
    assert tr._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 12))) == tr._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 13)))

    tr_vp = CacheTranslator(model, tok, cache_namespace="stmt@rev", use_version_prefix=True)
    assert tr_vp._format_encoder_input("LOAD_CONST <mask_0>", PythonVersion((3, 11))).startswith("v3.11 <SEP> <opcode:LOAD_CONST>")
    assert tr_vp._format_encoder_input("LOAD_CONST <mask_0>", "3.11.5") == tr_vp._format_encoder_input("LOAD_CONST <mask_0>", "3.11")
    assert tr_vp._cache_key("LOAD_CONST <mask_0>", "3.11.5") == tr_vp._cache_key("LOAD_CONST <mask_0>", "3.11")
    assert tr_vp._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 11))) != tr_vp._cache_key("LOAD_CONST <mask_0>", PythonVersion((3, 12)))
    with pytest.raises(ValueError, match="version is required"):
        tr_vp._format_encoder_input("LOAD_CONST <mask_0>", None)
    with pytest.raises(ValueError, match="version is required"):
        tr_vp._cache_key("LOAD_CONST <mask_0>", None)


def test_translate_beam_early_stopping_eos_and_oob_filtering():
    tok = _make_tok()

    def gen(**kwargs):
        assert kwargs["num_beams"] == 5
        assert kwargs["num_return_sequences"] == 5
        assert kwargs["early_stopping"] is True
        return torch.tensor(
            [
                [0, 8, 2, 0],  # valid completed: <mask_0> -> <mask_7>
                [0, 8, 2, 0],  # duplicate completed
                [0, 10, 11, 12],  # unterminated (no EOS id 2) -> must be dropped
                [0, 9, 2, 0],  # OOB <mask_1> when input only has 1 mask -> must be dropped
                [0, 12, 2, 0],  # lexically unclosed '(' with EOS (e.g. liveness fallback) -> must be dropped
            ]
        )

    model = _StubGenModel(tok, gen)
    tr = CacheTranslator(model, tok, cache_namespace="stmt@rev")
    cands = tr.translate_beam(["LOAD_CONST <mask_7>"], num_beams=5, version=PythonVersion((3, 12)))
    assert cands == [["<mask_7>"]]
    assert len(tr.cache) == 0


def test_decompiler_suspect_mapping_uses_source_idx_for_duplicates_and_sanitized():
    d = Decompiler.__new__(Decompiler)
    fake_co = object()
    d.translation_results = [["pass", "elif x:", "pass"]]
    d.source_lines = ["pass", "elif x:", "pass"]
    d.source_context = SimpleNamespace(source_lines=lambda: [])

    # Duplicate line at position 2 must map to [2, 1], not [0]
    assert d._suspect_statement_indices(0, SourceLine("pass", 0, fake_co, source_idx=2)) == [2, 1]
    # Sanitized 'elif x:' rendered as 'if x:' still maps cleanly via source_idx=1
    assert d._suspect_statement_indices(0, SourceLine("if x:", 0, fake_co, source_idx=1)) == [1, 0]
    # Duplicate synthetic lines (source_idx=None) resolve via error_lno rather than first match
    rendered = [
        SourceLine("pass", 0, fake_co, source_idx=0),
        SourceLine("pass", 0, fake_co, source_idx=None),
        SourceLine("elif x:", 0, fake_co, source_idx=1),
        SourceLine("pass", 0, fake_co, source_idx=None),
    ]
    d.source_context = SimpleNamespace(source_lines=lambda: rendered)
    assert d._suspect_statement_indices(0, rendered[3], error_lno=4) == [1, 0]


def test_decompiler_beam_retry_rolls_back_inst_source_line_and_handles_exception():
    d = Decompiler.__new__(Decompiler)
    d.name = "beam-rollback-test"
    d.version = PythonVersion((3, 12))
    d.check_timeout = Mock()
    fake_co = object()
    fake_bc = SimpleNamespace(codeobj=fake_co, name="f")
    class _FakeInst:
        def __init__(self, starts_line, source_line):
            self.starts_line = starts_line
            self.source_line = source_line

    inst = _FakeInst(starts_line=1, source_line="orig line")
    d.ordered_bytecodes = [fake_bc]
    d.ordered_instructions = [[inst]]
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
            self.cache = {"k": "v"}
            self.reads = {fake_co: {inst: "x = ("}}
            self.lines = ["x = ("]

        def snapshot(self):
            return (list(self.lines), dict(self.cache), {co: dict(r) for co, r in self.reads.items()})

        def restore(self, snap):
            self.lines, cache, reads = snap
            self.cache = dict(cache)
            self.reads = {co: dict(r) for co, r in reads.items()}

        def update_lines(self, lines):
            self.lines = list(lines)

        def source_lines(self):
            return [SourceLine(s, 0, fake_co, source_idx=idx) for idx, s in enumerate(self.lines)]

    d.source_context = FakeContext()
    d.update_source_lines = lambda: setattr(d, "source_lines", list(d.translation_results[0]))
    d.unmask_lines = lambda: None
    d.reconstruct_source = lambda: setattr(d, "indented_source", "\n".join(d.source_lines))
    d.check_reconstruction = lambda src: [Exception("SyntaxError: line 1")]
    # Candidate 1 raises during bc_to_cft; candidate 2 mutates inst.source_line & fails compile check
    d.translator = SimpleNamespace(translate_beam=lambda reqs, **kw: [["CRASH", "BAD_CAND"]])

    import pylingual.decompiler as dec_mod

    def fake_bc_to_cft(bc, lines):
        inst.source_line = lines[0]
        inst.starts_line = 99
        if lines[0] == "CRASH":
            raise RuntimeError("cfg failure")
        return SimpleNamespace(header_lines=[])

    orig_bc_to_cft = dec_mod.bc_to_cft
    dec_mod.bc_to_cft = fake_bc_to_cft
    try:
        fixed = d.correct_translation_beam(0, SourceLine("x = (", 0, fake_co, source_idx=0), error_lno=1)
    finally:
        dec_mod.bc_to_cft = orig_bc_to_cft

    assert fixed is False
    assert inst.source_line == "orig line"
    assert inst.starts_line == 1
    assert d.translation_results[0] == ["x = ("]
    assert d.source_lines == ["x = ("]
    assert d.indented_source == "x = ("
    assert d.source_context.cfts[fake_co] is orig_cft
    assert d.source_context.reads[fake_co][inst] == "x = ("


def test_decompiler_beam_retry_accepts_advancing_error_in_multi_error_codeobj():
    d = Decompiler.__new__(Decompiler)
    d.name = "beam-multi-error-test"
    d.version = PythonVersion((3, 12))
    d.check_timeout = Mock()
    fake_co = object()
    fake_bc = SimpleNamespace(codeobj=fake_co, name="f")
    d.ordered_bytecodes = [fake_bc]
    d.ordered_instructions = [[]]
    d.codeobj_instruction_lists = [["LOAD_CONST <mask_0>", "LOAD_CONST <mask_1>"]]
    d.segmentation_results = [[{"entity": "B", "score": 1.0}, {"entity": "B", "score": 1.0}]]
    d.translation_results = [["x = (", "y = ["]]
    d.source_lines = ["x = (", "y = ["]
    d.indented_source = "x = (\ny = ["
    d.equivalence_results = [Exception("SyntaxError: line 1")]

    orig_cft = SimpleNamespace(header_lines=[])

    class FakeContext:
        def __init__(self):
            self.cfts = {fake_co: orig_cft}
            self.cache = {}
            self.reads = {fake_co: {}}
            self.lines = ["x = (", "y = ["]

        def snapshot(self):
            return (list(self.lines), dict(self.cache), {co: dict(r) for co, r in self.reads.items()})

        def restore(self, snap):
            self.lines, self.cache, self.reads = snap

        def update_lines(self, lines):
            self.lines = list(lines)

        def source_lines(self):
            return [SourceLine(s, 0, fake_co, source_idx=idx) for idx, s in enumerate(self.lines)]

        def __str__(self):
            return "\n".join(self.lines)

    d.source_context = FakeContext()
    d.update_source_lines = lambda: setattr(d, "source_lines", list(d.translation_results[0]))
    d.unmask_lines = lambda: None
    d.reconstruct_source = lambda: setattr(d, "indented_source", "\n".join(d.source_lines))

    def fake_check(src):
        lines = src.splitlines()
        if lines[0] == "x = (":
            return [Exception("SyntaxError: line 1")]
        if lines[1] == "y = [":
            return [Exception("SyntaxError: line 2")]
        return [SimpleNamespace(success=True, bc_a=fake_bc)]

    d.check_reconstruction = fake_check
    d.translator = SimpleNamespace(
        translate_beam=lambda reqs, **kw: [["x = 1"] if "mask_0" in r else ["y = 2"] for r in reqs]
    )

    import pylingual.decompiler as dec_mod

    orig_bc_to_cft = dec_mod.bc_to_cft
    dec_mod.bc_to_cft = lambda bc, lines: SimpleNamespace(header_lines=[])
    try:
        # First call fixes line 1; error advances to line 2 in the SAME code object -> must accept!
        assert d.correct_translation_beam(0, SourceLine("x = (", 0, fake_co, source_idx=0), error_lno=1) is True
        assert d.translation_results[0] == ["x = 1", "y = ["]
        # Second call fixes line 2 -> fully compiling!
        assert d.correct_translation_beam(0, SourceLine("y = [", 0, fake_co, source_idx=1), error_lno=2) is True
        assert d.translation_results[0] == ["x = 1", "y = 2"]
    finally:
        dec_mod.bc_to_cft = orig_bc_to_cft


def test_decompiler_beam_retry_falls_back_on_beam_error_but_propagates_timeout():
    d = Decompiler.__new__(Decompiler)
    d.name = "beam-error-fallback"
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
    d.source_context = SimpleNamespace(
        cfts={fake_co: SimpleNamespace(header_lines=[])},
        snapshot=lambda: None,
        source_lines=lambda: [SourceLine("x = (", 0, fake_co, source_idx=0)],
    )
    d.translator = SimpleNamespace(translate_beam=Mock(side_effect=RuntimeError("unexpected beam bug")))
    assert d.correct_translation_beam(0, SourceLine("x = (", 0, fake_co, source_idx=0), error_lno=1) is False

    d.translator = SimpleNamespace(translate_beam=Mock(side_effect=TimeoutError("timed out")))
    with pytest.raises(TimeoutError, match="timed out"):
        d.correct_translation_beam(0, SourceLine("x = (", 0, fake_co, source_idx=0), error_lno=1)
