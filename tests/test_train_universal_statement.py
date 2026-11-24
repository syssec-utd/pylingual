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
    assert check_masked_statement_parses("try:", "3.11")
    assert check_masked_statement_parses("elif <mask_0>:", "3.11")
    assert check_masked_statement_parses("match <mask_0>:", "3.11")
    assert check_masked_statement_parses("case {<mask_0>: <mask_1>}:", "3.11")
    assert check_masked_statement_parses("case -<mask_0>:", "3.11")
    assert check_masked_statement_parses("@<mask_0>", "3.11")
    assert not check_masked_statement_parses("x = (<mask_0>", "3.11")
    # Pre-3.12 f-string quote reuse must fail for 3.11 even when host Python is >= 3.12
    assert not check_masked_statement_parses('f"{"x"}"', "3.11")
    assert check_masked_statement_parses('f"{"x"}"', "3.12")


def test_evaluate_generation_budgets_attention_backs_off_and_requires_eos():
    tok = _tiny_tokenizer()
    index = TokenizerConstraintIndex(tok)
    pad_id = tok.pad_token_id
    eos_id = tok.eos_token_id
    ret_id = tok.convert_tokens_to_ids("return")
    m0_id = tok.convert_tokens_to_ids("<mask_0>")
    op_id = tok.convert_tokens_to_ids("<opcode:LOAD_CONST>")
    # 4 long-encoder examples (1536 tokens each): must pack as singletons under 5.2M budget
    long_examples = [
        EncodedExample([op_id] * 1536, [ret_id, m0_id, eos_id], "3.12", "enc_long", i, source_text="return <mask_0>", mask_count=1)
        for i in range(4)
    ]
    short_examples = [
        EncodedExample([op_id] * 16, [ret_id, m0_id, eos_id], "3.12", "short", 10 + i, source_text="return <mask_0>", mask_count=1)
        for i in range(4)
    ]
    recorded_shapes: list[tuple[int, int, int]] = []
    oom_once = {"fired": False}

    class _RecordingModel:
        def __init__(self):
            self.training = False
            self.config = type("Cfg", (), {"use_cache": False})()
            self.generation_config = type("GC", (), {"bad_words_ids": []})()

        def eval(self):
            self.training = False

        def train(self):
            self.training = True

        def generate(self, *, input_ids, attention_mask, max_length, logits_processor):
            b, e = input_ids.shape
            recorded_shapes.append((b, e, max_length))
            # Simulate OOM once on a multi-example short batch to verify backoff splitting
            if b > 1 and not oom_once["fired"]:
                oom_once["fired"] = True
                raise MemoryError("simulated eval OOM")
            if max_length == 512 and e == 1536:
                # Exhaust initial cap without EOS (trigger retry at 1024)
                return torch.full((b, max_length), ret_id, dtype=torch.long)
            if max_length == 1024:
                # Still no EOS on retry -> must NOT count toward constraint_ok/parse_ok/exact
                return torch.tensor([[pad_id, ret_id, m0_id]] * b, dtype=torch.long)
            # Short examples complete with EOS and exact gold match
            return torch.tensor([[pad_id, ret_id, m0_id, eos_id]] * b, dtype=torch.long)

    res = evaluate_generation(
        _RecordingModel(),
        tok,
        index,
        {"short": short_examples, "enc_long": long_examples, "tgt_long": []},
        torch.device("cpu"),
        max_samples=8,
        max_length=512,
        retry_max_length=1024,
        batch_size=16,
        max_attention_cost=5_200_000,
    )
    # Every 1536-token batch (both initial 512 and retry 1024) must be singleton (batch size 1)
    long_calls = [(b, ml) for b, e, ml in recorded_shapes if e == 1536]
    assert long_calls and all(b == 1 for b, _ in long_calls)
    assert any(ml == 1024 for _, ml in long_calls)
    assert oom_once["fired"] is True
    # Short examples succeeded with EOS; exhausted enc_long without EOS must score 0.0 across all rates
    assert res["short"]["eos_rate"] == 1.0
    assert res["short"]["parse_rate"] == 1.0
    assert res["short"]["exact_match"] == 1.0
    assert res["enc_long"]["eos_rate"] == 0.0
    assert res["enc_long"]["constraint_rate"] == 0.0
    assert res["enc_long"]["parse_rate"] == 0.0
    assert res["enc_long"]["exact_match"] == 0.0

    # Lowered attention budget (4_000_000): singleton retry cap must shrink to <= 725 so cost never exceeds budget
    recorded_shapes.clear()
    evaluate_generation(
        _RecordingModel(),
        tok,
        index,
        {"short": [], "enc_long": long_examples[:1], "tgt_long": []},
        torch.device("cpu"),
        max_samples=1,
        max_length=512,
        retry_max_length=1024,
        batch_size=16,
        max_attention_cost=4_000_000,
    )
    for b, e, ml in recorded_shapes:
        assert b * (e * e + ml * ml + e * ml) <= 4_000_000
    assert any(ml == 725 for _, _, ml in recorded_shapes)

    # Budget too small even for encoder alone must fail loudly
    with pytest.raises(ValueError, match="exceeds max_attention_cost"):
        evaluate_generation(
            _RecordingModel(),
            tok,
            index,
            {"short": [], "enc_long": long_examples[:1], "tgt_long": []},
            torch.device("cpu"),
            max_samples=1,
            max_length=512,
            retry_max_length=1024,
            max_attention_cost=2_000_000,
        )


def test_preflight_checks_fail_loudly(tmp_path, monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    args = build_arg_parser().parse_args(["--work-dir", str(tmp_path)])
    assert args.min_free_gib == 8.0
    assert args.min_free_ram_gib == 4.0
    assert args.min_free_vram_gib == 16.0
    with pytest.raises(RuntimeError, match="CUDA is not available"):
        _preflight_checks(tmp_path, args)

    args_disk = build_arg_parser().parse_args(
        ["--work-dir", str(tmp_path), "--cpu", "--min-free-ram-gib", "0", "--min-free-gib", "999999999"]
    )
    with pytest.raises(RuntimeError, match="Insufficient free space"):
        _preflight_checks(tmp_path, args_disk)

    args_ram = build_arg_parser().parse_args(
        ["--work-dir", str(tmp_path), "--cpu", "--min-free-gib", "0", "--min-free-ram-gib", "999999999"]
    )
    with pytest.raises(RuntimeError, match="Insufficient available host RAM"):
        _preflight_checks(tmp_path, args_ram)

    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "is_bf16_supported", lambda: True)
    monkeypatch.setattr(torch.cuda, "mem_get_info", lambda dev: (4 * 1024**3, 24 * 1024**3))
    args_vram = build_arg_parser().parse_args(
        ["--work-dir", str(tmp_path), "--min-free-gib", "0", "--min-free-ram-gib", "0", "--min-free-vram-gib", "16"]
    )
    with pytest.raises(RuntimeError, match="Insufficient free CUDA VRAM"):
        _preflight_checks(tmp_path, args_vram)


def test_train_and_exact_resume_equivalence(tmp_path):
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
    torch.manual_seed(99)
    base_dir = tmp_path / "base_model"
    T5ForConditionalGeneration(cfg).save_pretrained(base_dir)

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

    def _base_args(work_dir):
        return [
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
            "--steps",
            "4",
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
            "--min-free-ram-gib",
            "0",
            "--seed",
            "1234",
        ]

    # 1. Uninterrupted 4-step run (also exercises gradient_checkpointing=True on tiny CPU T5)
    uninterrupted_dir = tmp_path / "uninterrupted"
    gc_args = [a for a in _base_args(uninterrupted_dir) if a != "--no-gradient-checkpointing"]
    s_full = train(build_arg_parser().parse_args(gc_args))
    assert s_full["complete"] is True

    # 2. Interrupted after step 2, then resumed to step 4 with identical --steps 4 schedule
    resumed_dir = tmp_path / "resumed"
    gc_res_args = [a for a in _base_args(resumed_dir) if a != "--no-gradient-checkpointing"]
    s_part = train(build_arg_parser().parse_args(gc_res_args + ["--stop-after-step", "2"]))
    assert s_part["complete"] is False
    assert (resumed_dir / "latest_model" / "trainer_state.pt").exists()
    assert not (resumed_dir / "latest_model.prev").exists()

    s_res = train(build_arg_parser().parse_args(gc_res_args + ["--resume"]))
    assert s_res["complete"] is True
    assert s_res["bin_draws"] == s_full["bin_draws"]
    assert s_res["history"][-1]["val"] == pytest.approx(s_full["history"][-1]["val"], rel=1e-6, abs=1e-6, nan_ok=True)

    # Weights must match uninterrupted run bit-for-bit / numerically identically
    m_full = T5ForConditionalGeneration.from_pretrained(uninterrupted_dir / "latest_model")
    m_res = T5ForConditionalGeneration.from_pretrained(resumed_dir / "latest_model")
    for (n1, p1), (n2, p2) in zip(m_full.named_parameters(), m_res.named_parameters()):
        assert n1 == n2
        assert torch.allclose(p1, p2, atol=1e-6), f"Weight drift on resume for {n1}"

    # 3. Resume must reject trajectory-changing config mismatches (including local shard, token budget, grad clip)
    for extra in (
        ["--max-attention-cost", "1234567"],
        ["--target-tokens-per-step", "16"],
        ["--grad-clip", "0.5"],
        ["--weight-decay", "0.05"],
        ["--no-gradient-checkpointing"],
    ):
        with pytest.raises(ValueError, match="Resume config mismatch"):
            train(build_arg_parser().parse_args(gc_res_args + ["--resume"] + extra))

    other_shard = tmp_path / "other_shard.parquet"
    pq.write_table(pa.Table.from_pylist(rows), other_shard)
    altered_args = list(gc_res_args)
    altered_args[altered_args.index(str(shard))] = str(other_shard)
    with pytest.raises(ValueError, match="Resume config mismatch"):
        train(build_arg_parser().parse_args(altered_args + ["--resume"]))

    meta_path = resumed_dir / "latest_model" / "pylingual_training_meta.json"
    meta_path.write_text('{"step": 999}\n')
    with pytest.raises(ValueError, match="step mismatch"):
        train(build_arg_parser().parse_args(gc_res_args + ["--resume"]))

    # Smoke check save_weights_bundle, lr_for_step, evaluate_pools, evaluate_generation
    assert m_res.config.pylingual_version_prefix is True
    assert m_res.config.use_cache is True
    save_weights_bundle(m_res, resumed_dir / "latest_model", use_version_prefix=True, metadata={"step": 4})
    assert not (resumed_dir / "latest_model.prev").exists()
    assert lr_for_step(0, 100, 1e-5) > 0
    assert build_arg_parser().parse_args(["--work-dir", str(tmp_path)]).max_target_len == 1023
    assert build_arg_parser().parse_args(["--work-dir", str(tmp_path)]).max_attention_cost == 5_200_000
    _, val_pools, _ = prepare_training_pools(
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
    assert evaluate_pools(m_res, val_pools, 0, torch.device("cpu"), max_attention_cost=100_000, max_microbatch_size=4, use_bf16=False)["short"] > 0
    gen_res = evaluate_generation(m_res, tok, TokenizerConstraintIndex(tok), val_pools, torch.device("cpu"), max_samples=2, max_length=16, retry_max_length=32)
    assert "short" in gen_res and 0.0 <= gen_res["short"]["eos_rate"] <= 1.0
