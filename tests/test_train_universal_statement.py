"""Unit tests for the universal statement continuation training pipeline."""

from __future__ import annotations

from collections import Counter

import pyarrow as pa
import pyarrow.parquet as pq
import pytest
import torch
from tokenizers import Tokenizer, models as token_models, pre_tokenizers
from transformers import PreTrainedTokenizerFast, T5Config, T5ForConditionalGeneration

from dev_scripts.train_universal_statement import (
    EncodedExample,
    StratifiedBinSampler,
    _is_holdout_file,
    _preflight_checks,
    build_arg_parser,
    check_masked_statement_parses,
    evaluate_generation,
    evaluate_pools,
    filter_and_encode_statements,
    format_model_input,
    lr_for_step,
    pack_2d_microbatches,
    prepare_training_pools,
    save_weights_bundle,
    train,
)
from pylingual.translation_constraints import TokenizerConstraintIndex


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


def test_cross_version_holdout_is_hash_only():
    # Identical canonical source hash always lands on the same split side regardless of version
    for idx in range(50):
        h = f"same-source-{idx}"
        assert _is_holdout_file(h, 1500) == _is_holdout_file(h, 1500)


def test_ab_validation_and_bin_parity_across_version_prefix(tmp_path):
    tok = _tiny_tokenizer()
    shard = tmp_path / "ab_parity.parquet"
    # Include boundary inputs right at 254..258 tokens so naive post-prefix binning would drift
    rows = []
    for i in range(40):
        ver = "3.11" if i % 2 == 0 else "3.12"
        bc_len = 254 if i % 4 == 0 else 4
        bc = " ".join(["LOAD_CONST"] * bc_len) + " <mask_0> <SEP> RETURN_VALUE"
        rows.append(
            {
                "version": ver,
                "canonical_sha256": f"file-{i}",
                "statement": [{"bytecode": bc, "source": "return <mask_0>"}],
            }
        )
    pq.write_table(pa.Table.from_pylist(rows), shard)

    train_no, val_no, stats_no = prepare_training_pools(
        [shard],
        tok,
        use_version_prefix=False,
        max_input_len=512,
        max_target_len=64,
        short_cap_per_version=100,
        val_short_per_version=5,
        holdout_files_per_version=7500,
        seed=123,
        max_attention_cost=5_200_000,
    )
    train_vp, val_vp, stats_vp = prepare_training_pools(
        [shard],
        tok,
        use_version_prefix=True,
        max_input_len=512,
        max_target_len=64,
        short_cap_per_version=100,
        val_short_per_version=5,
        holdout_files_per_version=7500,
        seed=123,
        max_attention_cost=5_200_000,
    )
    # Exact same bin counts and exact same paired validation statements
    for b in ("short", "enc_long", "tgt_long"):
        assert [(ex.example_id, ex.version, ex.source_text) for ex in val_no[b]] == [
            (ex.example_id, ex.version, ex.source_text) for ex in val_vp[b]
        ]
        assert len(train_no[b]) == len(train_vp[b])
    assert stats_no["kept_short"] == stats_vp["kept_short"]
    assert stats_no["kept_enc_long"] == stats_vp["kept_enc_long"]


def test_filter_drops_overlength_invalid_and_banned_token_targets():
    tok = _tiny_tokenizer()
    bad_idx = TokenizerConstraintIndex(tok, bad_words_ids=[[tok.convert_tokens_to_ids("<opcode:LOAD_CONST>")]])
    stats: Counter = Counter()
    stmts = [
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return <mask_0>"},
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return ( <mask_0>"},
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return <mask_5>"},
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "x = ( <mask_0> , <mask_0> , <mask_0> )"},
        # Contains statically banned opcode token in target -> caught by TokenizerConstraintIndex
        {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "<opcode:LOAD_CONST>"},
    ]
    kept = filter_and_encode_statements(
        stmts,
        "3.11",
        tok,
        use_version_prefix=True,
        max_input_len=32,
        max_target_len=6,
        stats=stats,
        constraint_index=bad_idx,
    )
    assert len(kept) == 1
    assert stats["drop_constraint_fail"] == 2
    assert stats["drop_target_too_long"] == 1
    assert stats["drop_token_constraint_fail"] == 1
    assert stats["kept_short"] == 1


def test_stratified_sampler_caps_retires_bins_and_resumes_identically():
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
    # Exhausted bin permanently retired (never rescanned)
    assert "tgt_long" not in sampler._active_bins

    # Long-only 4-example pool yields all 8 exposures via take_one() before exhausting on draw 9
    long_only = [EncodedExample([1] * 10, [2] * 10, "3.11", "tgt_long", i) for i in range(4)]
    s_long = StratifiedBinSampler(
        {"short": [], "enc_long": [], "tgt_long": long_only},
        weights={"short": 0.0, "enc_long": 0.0, "tgt_long": 1.0},
        max_long_exposures=2,
        seed=9,
    )
    got = [s_long.take_one() for _ in range(8)]
    assert len(got) == 8
    with pytest.raises(RuntimeError, match="exhausted"):
        s_long.take_one()

    # Exact state_dict / load_state_dict continuity
    s1 = StratifiedBinSampler(
        {"short": short_items, "enc_long": [], "tgt_long": long_items},
        weights={"short": 0.5, "enc_long": 0.0, "tgt_long": 0.5},
        max_long_exposures=2,
        seed=7,
    )
    _ = [s1.take_one() for _ in range(5)]
    snap = s1.state_dict()
    s2 = StratifiedBinSampler(
        {"short": short_items, "enc_long": [], "tgt_long": long_items},
        weights={"short": 0.5, "enc_long": 0.0, "tgt_long": 0.5},
        max_long_exposures=2,
        seed=999,
    )
    s2.load_state_dict(snap)
    assert [s1.take_one().example_id for _ in range(15)] == [s2.take_one().example_id for _ in range(15)]


def test_pack_2d_microbatches_enforces_hard_attention_budget():
    examples = [
        EncodedExample([1] * 10, [2] * 10, "3.11", "short", 0),
        EncodedExample([1] * 10, [2] * 10, "3.11", "short", 1),
        EncodedExample([1] * 500, [2] * 500, "3.11", "tgt_long", 2),
        EncodedExample([1] * 500, [2] * 500, "3.11", "tgt_long", 3),
    ]
    batches = pack_2d_microbatches(examples, max_attention_cost=900_000, max_microbatch_size=8)
    assert [len(b) for b in batches] == [2, 1, 1]

    # Single example exceeding max_attention_cost must fail loudly instead of silently overflowing
    too_big = [EncodedExample([1] * 1536, [2] * 1023, "3.11", "tgt_long", 9)]
    with pytest.raises(ValueError, match="exceeds max_attention_cost"):
        pack_2d_microbatches(too_big, max_attention_cost=4_000_000, max_microbatch_size=8)
    # Fits cleanly under default 5_200_000 budget
    assert len(pack_2d_microbatches(too_big, max_attention_cost=5_200_000, max_microbatch_size=8)) == 1


def test_check_masked_statement_parses():
    assert check_masked_statement_parses("return <mask_0>", "3.11")
    assert check_masked_statement_parses("elif <mask_0>:", "3.11")
    assert check_masked_statement_parses("@<mask_0>", "3.11")
    assert not check_masked_statement_parses("x = (<mask_0>", "3.11")


def test_preflight_checks_fail_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    args = build_arg_parser().parse_args(["--work-dir", str(tmp_path)])
    with pytest.raises(RuntimeError, match="CUDA is not available"):
        _preflight_checks(tmp_path, args)

    args_disk = build_arg_parser().parse_args(["--work-dir", str(tmp_path), "--cpu", "--min-free-gib", "999999999"])
    with pytest.raises(RuntimeError, match="Insufficient free space"):
        _preflight_checks(tmp_path, args_disk)


def test_train_and_exact_resume_end_to_end_smoke(tmp_path):
    tok = _tiny_tokenizer()
    tok_dir = tmp_path / "tok" / "statement"
    tok_dir.mkdir(parents=True)
    tok.save_pretrained(tok_dir)

    cfg = T5Config(
        vocab_size=len(tok),
        d_model=16,
        d_kv=8,
        d_ff=32,
        num_layers=1,
        num_heads=2,
        pad_token_id=0,
        eos_token_id=2,
        decoder_start_token_id=0,
    )
    base_dir = tmp_path / "base_model"
    model = T5ForConditionalGeneration(cfg)
    model.save_pretrained(base_dir)

    shard = tmp_path / "shard.parquet"
    rows = [
        {
            "version": "3.11" if i % 2 == 0 else "3.12",
            "canonical_sha256": f"hash-{i}",
            "statement": [
                {"bytecode": "LOAD_CONST <mask_0> <SEP> RETURN_VALUE", "source": "return <mask_0>"},
            ],
        }
        for i in range(24)
    ]
    pq.write_table(pa.Table.from_pylist(rows), shard)

    work_dir = tmp_path / "run"
    common = [
        "--work-dir",
        str(work_dir),
        "--base-model",
        str(base_dir),
        "--base-rev",
        "main",
        "--tokenizer-repo",
        str(tmp_path / "tok"),
        "--tokenizer-rev",
        "main",
        "--local-shards",
        str(shard),
        "--cpu",
        "--no-gradient-checkpointing",
        "--version-prefix",
        "--max-input-len",
        "64",
        "--max-target-len",
        "64",
        "--target-tokens-per-step",
        "8",
        "--eval-every",
        "2",
        "--eval-gen-samples",
        "4",
        "--log-every",
        "1",
        "--holdout-files-per-version",
        "7500",
        "--min-free-gib",
        "0",
        "--seed",
        "1234",
    ]
    # Run steps 1..2
    s1 = train(build_arg_parser().parse_args(common + ["--steps", "2"]))
    assert s1["complete"] is True
    assert (work_dir / "latest_model").exists()
    assert (work_dir / "trainer_state.pt").exists()
    assert not (work_dir / "latest_model.prev").exists()
    assert "gen" in s1["history"][-1]
    assert "best_saved" in s1

    # Resume from step 2 to step 4
    s2 = train(build_arg_parser().parse_args(common + ["--steps", "4", "--resume"]))
    assert s2["complete"] is True
    assert s2["history"][-1]["step"] == 4
    assert sum(s2["bin_draws"].values()) > sum(s1["bin_draws"].values())

    # Smoke check evaluate_pools, evaluate_generation, save_weights_bundle, lr_for_step
    reloaded = T5ForConditionalGeneration.from_pretrained(work_dir / "latest_model")
    assert reloaded.config.pylingual_version_prefix is True
    assert reloaded.config.use_cache is True
    save_weights_bundle(reloaded, work_dir / "latest_model", use_version_prefix=True, metadata={"step": 4})
    assert not (work_dir / "latest_model.prev").exists()
    assert lr_for_step(0, 100, 1e-5) > 0
    assert build_arg_parser().parse_args(["--work-dir", str(tmp_path)]).max_target_len == 1023
    assert build_arg_parser().parse_args(["--work-dir", str(tmp_path)]).max_attention_cost == 5_200_000
    train_pools, val_pools, _ = prepare_training_pools(
        [shard],
        tok,
        use_version_prefix=True,
        max_input_len=64,
        max_target_len=64,
        short_cap_per_version=50,
        val_short_per_version=50,
        holdout_files_per_version=7500,
        seed=1,
    )
    assert evaluate_pools(reloaded, val_pools, 0, torch.device("cpu"), max_attention_cost=100_000, max_microbatch_size=4, use_bf16=False)["short"] > 0
    gen_res = evaluate_generation(reloaded, tok, TokenizerConstraintIndex(tok), val_pools, torch.device("cpu"), max_samples=2, max_length=16, retry_max_length=32)
    assert "short" in gen_res and 0.0 <= gen_res["short"]["eos_rate"] <= 1.0
