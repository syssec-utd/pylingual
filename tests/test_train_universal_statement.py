"""Unit tests for the universal statement continuation training pipeline."""

from __future__ import annotations

from collections import Counter

import pyarrow as pa
import pyarrow.parquet as pq
import torch
from tokenizers import Tokenizer, models as token_models, pre_tokenizers
from transformers import PreTrainedTokenizerFast, T5Config, T5ForConditionalGeneration

from dev_scripts.train_universal_statement import (
    EncodedExample,
    StratifiedBinSampler,
    build_arg_parser,
    evaluate_pools,
    filter_and_encode_statements,
    format_model_input,
    lr_for_step,
    pack_2d_microbatches,
    prepare_training_pools,
    save_weights_bundle,
)


def _tiny_tokenizer() -> PreTrainedTokenizerFast:
    vocab = [
        "<pad>",
        "<s>",
        "</s>",
        "<unk>",
        "<mask>",
        "v3.11",
        "v3.12",
        "<SEP>",
        "<opcode:LOAD_CONST>",
        "<opcode:RETURN_VALUE>",
        "<mask_0>",
        "return",
        "x",
        "=",
        "(",
        ")",
        ",",
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


def test_format_model_input_with_and_without_version_prefix():
    bc = "LOAD_CONST <mask_0> <SEP> RETURN_VALUE"
    assert format_model_input(bc, "3.11", use_version_prefix=False) == "<opcode:LOAD_CONST> <mask_0> <SEP> <opcode:RETURN_VALUE>"
    assert format_model_input(bc, "3.11", use_version_prefix=True) == "v3.11 <SEP> <opcode:LOAD_CONST> <mask_0> <SEP> <opcode:RETURN_VALUE>"


def test_filter_drops_overlength_and_invalid_targets_without_truncating():
    tok = _tiny_tokenizer()
    stats: Counter = Counter()
    stmts = [
        # Valid short
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return <mask_0>"},
        # Unclosed bracket -> rejected by constraint filter
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return ( <mask_0>"},
        # Out-of-bounds mask -> rejected by constraint filter
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return <mask_5>"},
        # Target too long (> 6 tokens) -> dropped, NOT truncated
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "x = ( <mask_0> , <mask_0> , <mask_0> )"},
    ]
    kept = filter_and_encode_statements(
        stmts,
        "3.11",
        tok,
        use_version_prefix=True,
        max_input_len=32,
        max_target_len=6,
        stats=stats,
    )
    assert len(kept) == 1
    assert stats["drop_constraint_fail"] == 2
    assert stats["drop_target_too_long"] == 1
    assert stats["kept_short"] == 1


def test_stratified_sampler_respects_long_exposure_cap():
    short_items = [EncodedExample([1, 2], [3, 4], "3.11", "short", i) for i in range(10)]
    long_items = [EncodedExample([1] * 300, [3] * 300, "3.11", "tgt_long", 100)]
    sampler = StratifiedBinSampler(
        {"short": short_items, "enc_long": [], "tgt_long": long_items},
        weights={"short": 0.5, "enc_long": 0.0, "tgt_long": 0.5},
        max_long_exposures=2,
        seed=42,
    )
    drawn = sampler.take(40)
    assert len(drawn) == 40
    assert sampler.exposures[100] == 2
    assert sampler.bin_draws["tgt_long"] == 2
    assert sampler.bin_draws["short"] == 38


def test_pack_2d_microbatches_enforces_attention_budget():
    examples = [
        EncodedExample([1] * 10, [2] * 10, "3.11", "short", 0),
        EncodedExample([1] * 10, [2] * 10, "3.11", "short", 1),
        EncodedExample([1] * 500, [2] * 500, "3.11", "tgt_long", 2),
        EncodedExample([1] * 500, [2] * 500, "3.11", "tgt_long", 3),
    ]
    batches = pack_2d_microbatches(examples, max_attention_cost=900_000, max_microbatch_size=8)
    # Two short examples fit together; each 500x500 costs 750_000 so they must split into separate microbatches
    assert [len(b) for b in batches] == [2, 1, 1]


def test_prepare_eval_and_save_bundle_smoke(tmp_path):
    tok = _tiny_tokenizer()
    shard = tmp_path / "shard.parquet"
    rows = [
        {
            "version": "3.11",
            "canonical_sha256": f"hash-{i}",
            "statement": [
                {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return <mask_0>"},
            ],
        }
        for i in range(20)
    ]
    pq.write_table(pa.Table.from_pylist(rows), shard)

    train_pools, val_pools, stats = prepare_training_pools(
        [shard],
        tok,
        use_version_prefix=True,
        max_input_len=64,
        max_target_len=64,
        short_cap_per_version=100,
        val_short_per_version=50,
        holdout_files_per_version=7500,  # ~50% holdout for tiny smoke test
        seed=7,
    )
    assert stats["files_seen"] == 20
    assert len(train_pools["short"]) > 0
    assert len(val_pools["short"]) > 0

    cfg = T5Config(vocab_size=len(tok), d_model=16, d_kv=8, d_ff=32, num_layers=1, num_heads=2, pad_token_id=0, eos_token_id=2, decoder_start_token_id=0)
    model = T5ForConditionalGeneration(cfg)
    val = evaluate_pools(model, val_pools, 0, torch.device("cpu"), max_attention_cost=100_000, max_microbatch_size=4, use_bf16=False)
    assert val["short"] > 0

    out_dir = tmp_path / "saved"
    save_weights_bundle(model, out_dir, use_version_prefix=True, metadata={"step": 1})
    reloaded = T5ForConditionalGeneration.from_pretrained(out_dir)
    assert reloaded.config.pylingual_version_prefix is True
    assert reloaded.config.use_cache is True
    assert lr_for_step(0, 100, 1e-5) > 0
    assert build_arg_parser().parse_args(["--work-dir", str(tmp_path)]).max_input_len == 1536
