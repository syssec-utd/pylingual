"""Tests for CacheTranslator constraints, cap-exhaustion retry, safe backoff, and cache isolation."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
import torch
from tokenizers import Tokenizer, models as token_models, pre_tokenizers
from transformers import PreTrainedTokenizerFast

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


def test_cap_exhaustion_retries_once_and_never_caches_unfinished_or_invalid():
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

    # If output contains an out-of-bounds mask (<mask_1> when input only has <mask_0>), never cache it
    model4 = _StubGenModel(tok, lambda **kwargs: torch.tensor([[0, 9, 2]]))
    translator4 = CacheTranslator(model4, tok, cache_namespace="stmt@rev", use_constraints=False)
    out4 = translator4(["LOAD_CONST <mask_0>"], version=PythonVersion((3, 12)))
    assert out4 == ["<mask_1>"]
    assert len(translator4.cache) == 0


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
