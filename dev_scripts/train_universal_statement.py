"""Continuation trainer for the universal PyLingual statement translation model.

Streams the audited parquet corpus (`syssec-utd/pylingual-shared-backbone-corpus-v3`),
drops statements exceeding sequence budgets or failing lexical/mask invariants rather
than silently truncating targets mid-expression, balances short vs. long examples with
an exposure cap, and trains with 2D length-bucketed BF16 microbatches on a single GPU.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
import torch
from huggingface_hub import HfApi, hf_hub_download
from transformers import PreTrainedTokenizerFast, T5ForConditionalGeneration

from pylingual.masking.model_disasm import encode_opcodes
from pylingual.translation_constraints import check_statement_constraints

DEFAULT_CORPUS_REPO = "syssec-utd/pylingual-shared-backbone-corpus-v3"
DEFAULT_CORPUS_REV = "6b71d099fcbfeabbe159dd011e907ae52ab6e4ed"
DEFAULT_BASE_MODEL = "syssec-utd/pylingual-shared-statement-v3"
DEFAULT_BASE_REV = "a20bc4d28fe8641df0f90aa3665431368930c329"
DEFAULT_TOKENIZER_REPO = "syssec-utd/pylingual-shared-tokenizer-v1"
DEFAULT_TOKENIZER_REV = "d23233a4bb237dcc3b1660e46a42f9189eaf0f6c"
VERSIONS = tuple(f"3.{minor}" for minor in range(6, 16))
_MASK_RE = re.compile(r"<mask_(\d+)>")


@dataclass
class EncodedExample:
    input_ids: list[int]
    label_ids: list[int]
    version: str
    bin_name: str  # "short", "enc_long", "tgt_long"
    example_id: int


def format_model_input(bytecode: str, version: str, *, use_version_prefix: bool) -> str:
    """Format raw normalized statement bytecode to match ``CacheTranslator`` byte-for-byte."""
    encoded = encode_opcodes(bytecode)
    if use_version_prefix:
        return f"v{version} <SEP> {encoded}"
    return encoded


def _mask_count(bytecode: str) -> int:
    nums = [int(m) for m in _MASK_RE.findall(bytecode)]
    return (max(nums) + 1) if nums else 0


def _is_holdout_file(canonical_sha256: str, version: str, holdout_files_per_version: int, total_files_per_version: int = 15000) -> bool:
    """Deterministic file-level holdout split by canonical source hash (zero intra-file leakage)."""
    if holdout_files_per_version <= 0:
        return False
    digest = hashlib.blake2b(f"{version}:{canonical_sha256}".encode(), digest_size=8).digest()
    bucket = int.from_bytes(digest, "little") % total_files_per_version
    return bucket < holdout_files_per_version


def filter_and_encode_statements(
    statements: list[dict[str, str]],
    version: str,
    tokenizer: PreTrainedTokenizerFast,
    *,
    use_version_prefix: bool,
    max_input_len: int,
    max_target_len: int,
    stats: Counter,
) -> list[tuple[list[int], list[int], str]]:
    """Filter and tokenize one file's statements without truncating targets.

    Returns list of ``(input_ids, label_ids, bin_name)`` tuples.
    """
    if not statements:
        return []
    py_lt_312 = tuple(map(int, version.split("."))) < (3, 12)
    valid_inputs: list[str] = []
    valid_targets: list[str] = []

    for row in statements:
        bc = row.get("bytecode") or ""
        src = row.get("source") or ""
        if not bc or not src:
            stats["drop_empty"] += 1
            continue
        if not check_statement_constraints(src, py_lt_312=py_lt_312, mask_count=_mask_count(bc)):
            stats["drop_constraint_fail"] += 1
            continue
        valid_inputs.append(format_model_input(bc, version, use_version_prefix=use_version_prefix))
        valid_targets.append(src)

    if not valid_inputs:
        return []

    enc_inputs = tokenizer(valid_inputs, truncation=False, add_special_tokens=True)["input_ids"]
    enc_targets = tokenizer(valid_targets, truncation=False, add_special_tokens=True)["input_ids"]
    empty_specials = {
        tid
        for role in ("bos", "eos", "pad")
        if (tid := getattr(tokenizer, f"{role}_token_id", None)) is not None
    }

    kept: list[tuple[list[int], list[int], str]] = []
    for inp_ids, tgt_ids in zip(enc_inputs, enc_targets):
        if len(inp_ids) > max_input_len:
            stats["drop_input_too_long"] += 1
            continue
        if len(tgt_ids) > max_target_len:
            stats["drop_target_too_long"] += 1
            continue
        if not any(tid not in empty_specials for tid in tgt_ids):
            stats["drop_empty"] += 1
            continue
        if len(tgt_ids) > 256:
            bin_name = "tgt_long"
        elif len(inp_ids) > 256:
            bin_name = "enc_long"
        else:
            bin_name = "short"
        stats[f"kept_{bin_name}"] += 1
        kept.append((inp_ids, tgt_ids, bin_name))
    return kept


def prepare_training_pools(
    shard_paths: list[Path],
    tokenizer: PreTrainedTokenizerFast,
    *,
    use_version_prefix: bool,
    max_input_len: int,
    max_target_len: int,
    short_cap_per_version: int,
    val_short_per_version: int,
    holdout_files_per_version: int,
    seed: int,
) -> tuple[dict[str, list[EncodedExample]], dict[str, list[EncodedExample]], dict[str, int]]:
    """Stream parquet shards into bounded in-memory train & val pools by length bin."""
    rng = random.Random(seed)
    stats: Counter = Counter()

    train_short_reservoir: dict[str, list[EncodedExample]] = defaultdict(list)
    train_short_seen: Counter = Counter()
    train_enc_long: list[EncodedExample] = []
    train_tgt_long: list[EncodedExample] = []

    val_short_reservoir: dict[str, list[EncodedExample]] = defaultdict(list)
    val_short_seen: Counter = Counter()
    val_enc_long: list[EncodedExample] = []
    val_tgt_long: list[EncodedExample] = []

    next_id = 0
    for shard_idx, shard_path in enumerate(shard_paths):
        pf = pq.ParquetFile(shard_path)
        for rg in range(pf.num_row_groups):
            table = pf.read_row_group(rg, columns=["version", "canonical_sha256", "statement"])
            versions = table["version"].to_pylist()
            hashes = table["canonical_sha256"].to_pylist()
            stmt_lists = table["statement"].to_pylist()
            for version, canon_hash, stmts in zip(versions, hashes, stmt_lists):
                stats["files_seen"] += 1
                is_val = _is_holdout_file(str(canon_hash), str(version), holdout_files_per_version)
                kept = filter_and_encode_statements(
                    stmts or [],
                    str(version),
                    tokenizer,
                    use_version_prefix=use_version_prefix,
                    max_input_len=max_input_len,
                    max_target_len=max_target_len,
                    stats=stats,
                )
                for inp_ids, tgt_ids, bin_name in kept:
                    ex = EncodedExample(inp_ids, tgt_ids, str(version), bin_name, next_id)
                    next_id += 1
                    if is_val:
                        if bin_name == "short":
                            val_short_seen[version] += 1
                            res = val_short_reservoir[version]
                            if len(res) < val_short_per_version:
                                res.append(ex)
                            else:
                                j = rng.randrange(val_short_seen[version])
                                if j < val_short_per_version:
                                    res[j] = ex
                        elif bin_name == "enc_long":
                            val_enc_long.append(ex)
                        else:
                            val_tgt_long.append(ex)
                    else:
                        if bin_name == "short":
                            train_short_seen[version] += 1
                            res = train_short_reservoir[version]
                            if len(res) < short_cap_per_version:
                                res.append(ex)
                            else:
                                j = rng.randrange(train_short_seen[version])
                                if j < short_cap_per_version:
                                    res[j] = ex
                        elif bin_name == "enc_long":
                            train_enc_long.append(ex)
                        else:
                            train_tgt_long.append(ex)
        print(
            json.dumps(
                {
                    "event": "shard_prepared",
                    "shard": shard_idx + 1,
                    "total_shards": len(shard_paths),
                    "train_short": sum(len(v) for v in train_short_reservoir.values()),
                    "train_enc_long": len(train_enc_long),
                    "train_tgt_long": len(train_tgt_long),
                    "val_tgt_long": len(val_tgt_long),
                }
            ),
            flush=True,
        )

    train_pools = {
        "short": [ex for v in sorted(train_short_reservoir) for ex in train_short_reservoir[v]],
        "enc_long": train_enc_long,
        "tgt_long": train_tgt_long,
    }
    val_pools = {
        "short": [ex for v in sorted(val_short_reservoir) for ex in val_short_reservoir[v]],
        "enc_long": val_enc_long,
        "tgt_long": val_tgt_long,
    }
    return train_pools, val_pools, dict(stats)


class StratifiedBinSampler:
    """Samples examples from short / enc_long / tgt_long pools with version stratification and long exposure caps."""

    def __init__(
        self,
        pools: dict[str, list[EncodedExample]],
        *,
        weights: dict[str, float],
        max_long_exposures: int,
        seed: int,
    ):
        self.rng = random.Random(seed)
        self.weights = dict(weights)
        self.max_long_exposures = max_long_exposures
        self.exposures: Counter = Counter()
        self.bin_draws: Counter = Counter()

        self._by_bin_ver: dict[str, dict[str, list[EncodedExample]]] = {}
        self._cursors: dict[str, dict[str, int]] = {}
        for bin_name, items in pools.items():
            grouped: dict[str, list[EncodedExample]] = defaultdict(list)
            for item in items:
                grouped[item.version].append(item)
            for ver_items in grouped.values():
                self.rng.shuffle(ver_items)
            self._by_bin_ver[bin_name] = dict(grouped)
            self._cursors[bin_name] = {ver: 0 for ver in grouped}

    def _draw_from_bin(self, bin_name: str) -> EncodedExample | None:
        ver_map = self._by_bin_ver.get(bin_name)
        if not ver_map:
            return None
        versions = list(ver_map.keys())
        self.rng.shuffle(versions)
        cap = self.max_long_exposures if bin_name in ("enc_long", "tgt_long") and self.max_long_exposures > 0 else None
        for ver in versions:
            items = ver_map[ver]
            n = len(items)
            if n == 0:
                continue
            cur = self._cursors[bin_name][ver]
            for _ in range(n):
                if cur >= n:
                    self.rng.shuffle(items)
                    cur = 0
                ex = items[cur]
                cur += 1
                if cap is None or self.exposures[ex.example_id] < cap:
                    self._cursors[bin_name][ver] = cur
                    self.exposures[ex.example_id] += 1
                    self.bin_draws[bin_name] += 1
                    return ex
            self._cursors[bin_name][ver] = cur
        return None

    def take(self, count: int) -> list[EncodedExample]:
        out: list[EncodedExample] = []
        bins = [b for b in ("short", "enc_long", "tgt_long") if self._by_bin_ver.get(b)]
        if not bins:
            raise RuntimeError("No training examples available in any bin")
        for _ in range(count):
            # Pick a bin by configured weight, falling back if a long bin reached its exposure cap
            available = list(bins)
            chosen: EncodedExample | None = None
            while available and chosen is None:
                ws = [self.weights[b] for b in available]
                b = self.rng.choices(available, weights=ws, k=1)[0]
                chosen = self._draw_from_bin(b)
                if chosen is None:
                    available.remove(b)
                    if b in bins:
                        bins.remove(b)
            if chosen is None:
                raise RuntimeError("All training bins exhausted")
            out.append(chosen)
        return out


def pack_2d_microbatches(
    examples: list[EncodedExample],
    *,
    max_attention_cost: int,
    max_microbatch_size: int,
) -> list[list[EncodedExample]]:
    """Sort examples by (input_len, label_len) and pack into attention-budgeted microbatches."""
    ordered = sorted(examples, key=lambda ex: (len(ex.input_ids), len(ex.label_ids)))
    batches: list[list[EncodedExample]] = []
    cur: list[EncodedExample] = []
    max_e = 0
    max_d = 0
    for ex in ordered:
        e = len(ex.input_ids)
        d = len(ex.label_ids)
        cand_e = max(max_e, e)
        cand_d = max(max_d, d)
        cand_n = len(cur) + 1
        cand_cost = cand_n * (cand_e * cand_e + cand_d * cand_d + cand_e * cand_d)
        if cur and (cand_n > max_microbatch_size or cand_cost > max_attention_cost):
            batches.append(cur)
            cur = [ex]
            max_e, max_d = e, d
        else:
            cur.append(ex)
            max_e, max_d = cand_e, cand_d
    if cur:
        batches.append(cur)
    return batches


def collate_batch(examples: list[EncodedExample], pad_token_id: int, device: torch.device) -> dict[str, torch.Tensor]:
    max_in = max(len(ex.input_ids) for ex in examples)
    max_lbl = max(len(ex.label_ids) for ex in examples)
    input_ids = torch.full((len(examples), max_in), pad_token_id, dtype=torch.long, device=device)
    attention_mask = torch.zeros((len(examples), max_in), dtype=torch.long, device=device)
    labels = torch.full((len(examples), max_lbl), -100, dtype=torch.long, device=device)
    for row, ex in enumerate(examples):
        n_in = len(ex.input_ids)
        n_lbl = len(ex.label_ids)
        input_ids[row, :n_in] = torch.tensor(ex.input_ids, dtype=torch.long, device=device)
        attention_mask[row, :n_in] = 1
        labels[row, :n_lbl] = torch.tensor(ex.label_ids, dtype=torch.long, device=device)
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}


def build_optimizer(model: torch.nn.Module, lr: float, weight_decay: float) -> torch.optim.Optimizer:
    decay_params = []
    no_decay_params = []
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if param.ndim < 2 or "bias" in name or "layer_norm" in name or "norm" in name:
            no_decay_params.append(param)
        else:
            decay_params.append(param)
    groups = [
        {"params": decay_params, "weight_decay": weight_decay},
        {"params": no_decay_params, "weight_decay": 0.0},
    ]
    return torch.optim.AdamW(groups, lr=lr, betas=(0.9, 0.999))


def lr_for_step(step: int, total_steps: int, base_lr: float, min_lr: float = 1e-6, warmup_frac: float = 0.03) -> float:
    warmup = max(1, int(total_steps * warmup_frac))
    if step < warmup:
        return base_lr * float(step + 1) / float(warmup)
    progress = min(1.0, float(step - warmup) / float(max(1, total_steps - warmup)))
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return min_lr + (base_lr - min_lr) * cosine


@torch.no_grad()
def evaluate_pools(
    model: T5ForConditionalGeneration,
    val_pools: dict[str, list[EncodedExample]],
    pad_token_id: int,
    device: torch.device,
    *,
    max_attention_cost: int,
    max_microbatch_size: int,
    use_bf16: bool,
) -> dict[str, float]:
    """Compute exact per-token cross-entropy loss separately on short, enc_long, and tgt_long slices."""
    was_training = model.training
    model.eval()
    results: dict[str, float] = {}
    amp_enabled = use_bf16 and device.type == "cuda"
    for bin_name in ("short", "enc_long", "tgt_long"):
        items = val_pools.get(bin_name) or []
        if not items:
            results[bin_name] = float("nan")
            continue
        total_loss = 0.0
        total_tokens = 0
        for micro in pack_2d_microbatches(items, max_attention_cost=max_attention_cost, max_microbatch_size=max_microbatch_size):
            batch = collate_batch(micro, pad_token_id, device)
            n_tok = int((batch["labels"] != -100).sum().item())
            if n_tok == 0:
                continue
            with torch.amp.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=amp_enabled):
                loss = model(**batch).loss
            total_loss += float(loss.item()) * n_tok
            total_tokens += n_tok
        results[bin_name] = total_loss / max(1, total_tokens)
    if was_training:
        model.train()
    return results


def download_corpus_shards(corpus_repo: str, corpus_rev: str, shard_dir: Path, max_shards: int = 0) -> list[Path]:
    """Download pinned parquet shards from HuggingFace into ``shard_dir``."""
    api = HfApi()
    info = api.dataset_info(corpus_repo, revision=corpus_rev)
    parquet_files = sorted(f.rfilename for f in info.siblings if f.rfilename.endswith(".parquet"))
    if max_shards > 0:
        parquet_files = parquet_files[:max_shards]
    paths: list[Path] = []
    shard_dir.mkdir(parents=True, exist_ok=True)
    for rel in parquet_files:
        local = Path(
            hf_hub_download(
                corpus_repo,
                rel,
                repo_type="dataset",
                revision=corpus_rev,
                local_dir=str(shard_dir),
            )
        )
        paths.append(local)
    return paths


def save_weights_bundle(
    model: T5ForConditionalGeneration,
    out_dir: Path,
    *,
    use_version_prefix: bool,
    metadata: dict[str, Any],
) -> None:
    """Atomically save weights-only model directory with version-prefix metadata."""
    tmp_dir = out_dir.with_name(out_dir.name + ".tmp")
    if tmp_dir.exists():
        import shutil

        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prev_use_cache = model.config.use_cache
    model.config.use_cache = True
    model.config.pylingual_version_prefix = bool(use_version_prefix)
    try:
        model.save_pretrained(tmp_dir)
    finally:
        model.config.use_cache = prev_use_cache
    (tmp_dir / "pylingual_training_meta.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if out_dir.exists():
        import shutil

        shutil.rmtree(out_dir)
    tmp_dir.replace(out_dir)


def train(args: argparse.Namespace) -> dict[str, Any]:
    work_dir = Path(args.work_dir).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() and not args.cpu else "cpu")
    if device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    tokenizer = PreTrainedTokenizerFast.from_pretrained(
        args.tokenizer_repo,
        revision=args.tokenizer_rev,
        subfolder="statement",
    )
    model = T5ForConditionalGeneration.from_pretrained(args.base_model, revision=args.base_rev)
    if model.get_input_embeddings().num_embeddings != len(tokenizer):
        raise ValueError("Model embedding size does not match frozen statement tokenizer")
    model.to(device)
    model.config.use_cache = False
    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    if args.local_shards:
        shard_paths = [Path(p) for p in args.local_shards]
    else:
        shard_paths = download_corpus_shards(
            args.corpus_repo,
            args.corpus_rev,
            work_dir / "shards",
            max_shards=args.max_shards,
        )

    train_pools, val_pools, data_stats = prepare_training_pools(
        shard_paths,
        tokenizer,
        use_version_prefix=args.version_prefix,
        max_input_len=args.max_input_len,
        max_target_len=args.max_target_len,
        short_cap_per_version=args.short_cap_per_version,
        val_short_per_version=args.val_short_per_version,
        holdout_files_per_version=args.holdout_files_per_version,
        seed=args.seed,
    )
    print(json.dumps({"event": "data_ready", "stats": data_stats, "train_sizes": {k: len(v) for k, v in train_pools.items()}, "val_sizes": {k: len(v) for k, v in val_pools.items()}}), flush=True)

    sampler = StratifiedBinSampler(
        train_pools,
        weights={"short": args.weight_short, "enc_long": args.weight_enc_long, "tgt_long": args.weight_tgt_long},
        max_long_exposures=args.max_long_exposures,
        seed=args.seed,
    )
    optimizer = build_optimizer(model, lr=args.lr, weight_decay=args.weight_decay)
    use_bf16 = not args.no_bf16 and device.type == "cuda"
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else 0

    # Baseline validation before update 0
    val0 = evaluate_pools(
        model,
        val_pools,
        pad_id,
        device,
        max_attention_cost=args.max_attention_cost,
        max_microbatch_size=args.max_microbatch_size,
        use_bf16=use_bf16,
    )
    print(json.dumps({"event": "eval", "step": 0, "val": val0}), flush=True)
    baseline_short = val0.get("short", float("inf"))

    def _selection_score(val_dict: dict[str, float]) -> float:
        # Equal weight on short, enc_long, tgt_long (ignoring NaN empty slices in smoke runs)
        vals = [v for v in val_dict.values() if not math.isnan(v)]
        return sum(vals) / max(1, len(vals))

    best_score = _selection_score(val0)
    history: list[dict[str, Any]] = [{"step": 0, "val": val0}]
    started = time.monotonic()
    model.train()

    for step in range(1, args.steps + 1):
        lr = lr_for_step(step - 1, args.steps, args.lr, min_lr=args.min_lr, warmup_frac=args.warmup_frac)
        for group in optimizer.param_groups:
            group["lr"] = lr

        # Draw examples until reaching target_tokens_per_step non-pad target tokens
        step_examples: list[EncodedExample] = []
        step_target_tokens = 0
        while step_target_tokens < args.target_tokens_per_step:
            chunk = sampler.take(32)
            for ex in chunk:
                step_examples.append(ex)
                step_target_tokens += len(ex.label_ids)
                if step_target_tokens >= args.target_tokens_per_step:
                    break

        microbatches = pack_2d_microbatches(
            step_examples,
            max_attention_cost=args.max_attention_cost,
            max_microbatch_size=args.max_microbatch_size,
        )
        optimizer.zero_grad(set_to_none=True)
        step_loss_sum = 0.0
        actual_tokens = 0

        for micro in microbatches:
            batch = collate_batch(micro, pad_id, device)
            n_tok = int((batch["labels"] != -100).sum().item())
            if n_tok == 0:
                continue
            with torch.amp.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=use_bf16):
                loss = model(**batch).loss
            if not torch.isfinite(loss):
                raise RuntimeError(f"Non-finite training loss at step {step}: {loss.item()}")
            # Weight each microbatch strictly by its exact share of non-pad target tokens
            scaled = loss * (n_tok / float(step_target_tokens))
            scaled.backward()
            step_loss_sum += float(loss.item()) * n_tok
            actual_tokens += n_tok

        grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip))
        if not math.isfinite(grad_norm):
            raise RuntimeError(f"Non-finite gradient norm at step {step}: {grad_norm}")
        optimizer.step()

        if step % args.log_every == 0 or step == args.steps:
            rec = {
                "event": "train",
                "step": step,
                "steps": args.steps,
                "loss": round(step_loss_sum / max(1, actual_tokens), 5),
                "lr": round(lr, 8),
                "grad_norm": round(grad_norm, 4),
                "microbatches": len(microbatches),
                "target_tokens": actual_tokens,
                "bin_draws": dict(sampler.bin_draws),
                "seconds": round(time.monotonic() - started, 1),
                "peak_cuda_gib": round(torch.cuda.max_memory_allocated() / (1024**3), 2) if device.type == "cuda" else 0.0,
            }
            print(json.dumps(rec), flush=True)

        if step % args.eval_every == 0 or step == args.steps:
            val = evaluate_pools(
                model,
                val_pools,
                pad_id,
                device,
                max_attention_cost=args.max_attention_cost,
                max_microbatch_size=args.max_microbatch_size,
                use_bf16=use_bf16,
            )
            score = _selection_score(val)
            short_ok = math.isnan(val.get("short", float("nan"))) or math.isnan(baseline_short) or val["short"] <= baseline_short + 0.015
            improved = score < best_score and short_ok
            history.append({"step": step, "val": val, "score": score, "improved": improved})
            print(json.dumps({"event": "eval", "step": step, "val": val, "score": round(score, 5), "improved": improved}), flush=True)

            meta = {
                "base_model": args.base_model,
                "base_rev": args.base_rev,
                "tokenizer_repo": args.tokenizer_repo,
                "tokenizer_rev": args.tokenizer_rev,
                "corpus_repo": args.corpus_repo,
                "corpus_rev": args.corpus_rev,
                "version_prefix": args.version_prefix,
                "max_input_len": args.max_input_len,
                "max_target_len": args.max_target_len,
                "step": step,
                "total_steps": args.steps,
                "val": val,
                "bin_draws": dict(sampler.bin_draws),
                "data_stats": data_stats,
            }
            save_weights_bundle(model, work_dir / "latest_model", use_version_prefix=args.version_prefix, metadata=meta)
            if improved:
                best_score = score
                save_weights_bundle(model, work_dir / "best_model", use_version_prefix=args.version_prefix, metadata=meta)
                if args.hub_repo:
                    api = HfApi()
                    api.create_repo(args.hub_repo, exist_ok=True, private=not args.public)
                    api.upload_folder(
                        folder_path=str(work_dir / "best_model"),
                        repo_id=args.hub_repo,
                        commit_message=f"Best checkpoint at step {step} (val={val})",
                    )

    summary = {
        "complete": True,
        "steps": args.steps,
        "best_score": best_score,
        "bin_draws": dict(sampler.bin_draws),
        "data_stats": data_stats,
        "history": history,
        "seconds": round(time.monotonic() - started, 1),
    }
    (work_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--work-dir", type=Path, required=True)
    p.add_argument("--base-model", default=DEFAULT_BASE_MODEL)
    p.add_argument("--base-rev", default=DEFAULT_BASE_REV)
    p.add_argument("--tokenizer-repo", default=DEFAULT_TOKENIZER_REPO)
    p.add_argument("--tokenizer-rev", default=DEFAULT_TOKENIZER_REV)
    p.add_argument("--corpus-repo", default=DEFAULT_CORPUS_REPO)
    p.add_argument("--corpus-rev", default=DEFAULT_CORPUS_REV)
    p.add_argument("--local-shards", nargs="*", default=None)
    p.add_argument("--max-shards", type=int, default=0, help="Limit downloaded shards (0 = all)")
    p.add_argument("--version-prefix", action="store_true", help="Prepend 'v{version} <SEP> ' to encoded bytecode")
    p.add_argument("--max-input-len", type=int, default=1536)
    p.add_argument("--max-target-len", type=int, default=1024)
    p.add_argument("--short-cap-per-version", type=int, default=100000)
    p.add_argument("--val-short-per-version", type=int, default=500)
    p.add_argument("--holdout-files-per-version", type=int, default=150)
    p.add_argument("--weight-short", type=float, default=0.70)
    p.add_argument("--weight-enc-long", type=float, default=0.20)
    p.add_argument("--weight-tgt-long", type=float, default=0.10)
    p.add_argument("--max-long-exposures", type=int, default=4)
    p.add_argument("--target-tokens-per-step", type=int, default=8192)
    p.add_argument("--max-attention-cost", type=int, default=4_000_000)
    p.add_argument("--max-microbatch-size", type=int, default=64)
    p.add_argument("--steps", type=int, default=2500)
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--min-lr", type=float, default=1e-6)
    p.add_argument("--warmup-frac", type=float, default=0.03)
    p.add_argument("--weight-decay", type=float, default=0.01)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--eval-every", type=int, default=250)
    p.add_argument("--log-every", type=int, default=25)
    p.add_argument("--seed", type=int, default=20261123)
    p.add_argument("--gradient-checkpointing", action="store_true", default=True)
    p.add_argument("--no-gradient-checkpointing", dest="gradient_checkpointing", action="store_false")
    p.add_argument("--no-bf16", action="store_true")
    p.add_argument("--cpu", action="store_true")
    p.add_argument("--hub-repo", default=None)
    p.add_argument("--public", action="store_true")
    return p


if __name__ == "__main__":
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")
    train(build_arg_parser().parse_args())
