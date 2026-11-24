"""Continuation trainer for the universal PyLingual statement translation model.

Streams the audited parquet corpus (`syssec-utd/pylingual-shared-backbone-corpus-v3`)
one shard at a time, drops statements exceeding sequence/attention budgets or failing
exact tokenizer-level lexical/mask invariants rather than silently truncating targets,
balances short vs. long examples with an exposure cap, and trains with 2D length-bucketed
BF16 microbatches, exact resumable checkpoints, and paired generation evaluation.
"""

from __future__ import annotations

import os

# Disable hf_xet before importing huggingface_hub so shard streaming never writes to ~/.cache/huggingface/xet on tight root disks.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import argparse
import ast
import gc
import hashlib
import heapq
import json
import math
import random
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import pyarrow.parquet as pq
import torch
from huggingface_hub import HfApi, constants as hf_constants, hf_hub_download
from transformers import PreTrainedTokenizerFast, T5ForConditionalGeneration

from pylingual.masking.model_disasm import encode_opcodes
from pylingual.translation_constraints import (
    StatementLogitsProcessor,
    TokenizerConstraintIndex,
    check_statement_constraints,
)

DEFAULT_CORPUS_REPO = "syssec-utd/pylingual-shared-backbone-corpus-v3"
DEFAULT_CORPUS_REV = "6b71d099fcbfeabbe159dd011e907ae52ab6e4ed"
DEFAULT_BASE_MODEL = "syssec-utd/pylingual-shared-statement-v3"
DEFAULT_BASE_REV = "a20bc4d28fe8641df0f90aa3665431368930c329"
DEFAULT_TOKENIZER_REPO = "syssec-utd/pylingual-shared-tokenizer-v1"
DEFAULT_TOKENIZER_REV = "d23233a4bb237dcc3b1660e46a42f9189eaf0f6c"
PREFIX_HEADROOM = 8
_MASK_RE = re.compile(r"<mask_(\d+)>")
_CANONICAL_MASK_RE = re.compile(r"<mask_(0|[1-9][0-9]*)>", re.ASCII)
_BLOCK_STARTERS = (
    "if ",
    "elif ",
    "else:",
    "for ",
    "async for ",
    "while ",
    "def ",
    "async def ",
    "class ",
    "with ",
    "async with ",
    "try:",
    "except",
    "finally:",
    "match ",
    "case ",
)


@dataclass
class EncodedExample:
    input_ids: list[int]
    label_ids: list[int]
    version: str
    bin_name: str  # "short", "enc_long", "tgt_long"
    example_id: int
    source_text: str = ""
    mask_count: int = 0


def format_model_input(bytecode: str, version: str, *, use_version_prefix: bool) -> str:
    """Format raw normalized statement bytecode to match ``CacheTranslator`` byte-for-byte."""
    encoded = encode_opcodes(bytecode)
    if use_version_prefix:
        return f"v{version} <SEP> {encoded}"
    return encoded


def _mask_count(bytecode: str) -> int:
    nums = [int(m) for m in _MASK_RE.findall(bytecode)]
    return (max(nums) + 1) if nums else 0


def _attention_cost(enc_len: int, dec_len: int) -> int:
    return enc_len * enc_len + dec_len * dec_len + enc_len * dec_len


def _is_holdout_file(canonical_sha256: str, holdout_files_per_version: int, total_files_per_version: int = 15000) -> bool:
    """Deterministic cross-version file-level holdout split by canonical source hash alone."""
    if holdout_files_per_version <= 0:
        return False
    digest = hashlib.blake2b(canonical_sha256.encode(), digest_size=8).digest()
    bucket = int.from_bytes(digest, "little") % total_files_per_version
    return bucket < holdout_files_per_version


def _deterministic_priority(seed: int, canonical_sha256: str, version: str, stmt_idx: int) -> int:
    """Stable per-statement hash priority independent of prefix/filtering shifts."""
    key = f"{seed}:{canonical_sha256}:{version}:{stmt_idx}".encode()
    return int.from_bytes(hashlib.blake2b(key, digest_size=8).digest(), "little")


class _BoundedHashReservoir:
    """Deterministic top-K (lowest hash priority) reservoir keeping memory strictly bounded."""

    def __init__(self, cap: int):
        self.cap = cap
        self._heap: list[tuple[int, int, EncodedExample]] = []  # max-heap via (-priority, -example_id, ex)

    def add(self, priority: int, example: EncodedExample) -> None:
        if self.cap <= 0:
            return
        entry = (-priority, -example.example_id, example)
        if len(self._heap) < self.cap:
            heapq.heappush(self._heap, entry)
        elif entry > self._heap[0]:
            heapq.heapreplace(self._heap, entry)

    def items(self) -> list[EncodedExample]:
        # Sort by ascending (priority, example_id) for exact A/B determinism
        ordered = sorted(self._heap, key=lambda x: (-x[0], -x[1]))
        return [ex for _, _, ex in ordered]

    def __len__(self) -> int:
        return len(self._heap)


def check_masked_statement_parses(text: str, version: str) -> bool:
    """Check whether a masked statement parses as valid Python syntax (for generation eval)."""
    stripped = text.strip()
    if not stripped:
        return False
    ver_tuple = tuple(map(int, version.split(".")[:2]))
    # Enforce Python < 3.12 PEP 701 f-string quote/backslash rules even when running on a newer host Python
    if not check_statement_constraints(stripped, py_lt_312=(ver_tuple < (3, 12))):
        return False
    # Substitute <mask_N> with valid identifier placeholders first; also allow literal '1'
    # fallback for syntactic positions that require literals (e.g. match/case mapping keys
    # like `case {<mask_0>: <mask_1>}:` or negative/complex numeric patterns).
    unmasked_variants = [
        _CANONICAL_MASK_RE.sub(lambda m: f"_m{m.group(1)}", stripped),
        _CANONICAL_MASK_RE.sub("1", stripped),
    ]
    # Build minimal valid syntactic wrappers for single-line statement headers/clauses
    candidates: list[str] = []
    for unmasked in unmasked_variants:
        candidates.append(unmasked)
        if stripped.endswith(":"):
            if stripped == "try:":
                candidates.append(f"{unmasked}\n    pass\nexcept Exception:\n    pass")
            elif stripped.startswith(("elif ", "else:")):
                candidates.append(f"if _c:\n    pass\n{unmasked}\n    pass")
            elif stripped.startswith(("except", "finally:")):
                candidates.append(f"try:\n    pass\n{unmasked}\n    pass")
            elif stripped.startswith("case "):
                candidates.append(f"match _c:\n    {unmasked}\n        pass")
            elif stripped.startswith("match "):
                candidates.append(f"{unmasked}\n    case _:\n        pass")
            elif any(stripped.startswith(p) for p in _BLOCK_STARTERS):
                candidates.append(f"{unmasked}\n    pass")
        elif stripped.startswith("@"):
            candidates.append(f"{unmasked}\ndef _f():\n    pass")
        elif stripped in ("break", "continue"):
            candidates.append(f"while True:\n    {unmasked}")
        elif stripped.startswith("return") or stripped.startswith("yield"):
            candidates.append(f"def _f():\n    {unmasked}")

    # Python's ast.parse rejects feature_version > host version; clamp to host minor if needed
    feat_ver = min(ver_tuple, (sys.version_info.major, sys.version_info.minor))
    for cand in candidates:
        try:
            ast.parse(cand, feature_version=feat_ver)
            return True
        except SyntaxError:
            continue
    return False


def filter_and_encode_statements(
    statements: list[dict[str, str]],
    version: str,
    tokenizer: PreTrainedTokenizerFast,
    *,
    use_version_prefix: bool,
    max_input_len: int,
    max_target_len: int,
    stats: Counter,
    constraint_index: TokenizerConstraintIndex | None = None,
    max_attention_cost: int | None = None,
    keep_source_text: bool = False,
) -> list[tuple[list[int], list[int], str, int, str, int]]:
    """Filter and tokenize one file's statements without truncating targets.

    Admission and bin assignment are computed strictly on unprefixed bytecode lengths
    (reserving ``PREFIX_HEADROOM`` tokens) so ``--version-prefix`` and baseline runs
    evaluate and train on identical statement populations.

    Returns list of ``(input_ids, label_ids, bin_name, stmt_idx, source_text, mask_count)``.
    """
    if not statements:
        return []
    py_lt_312 = tuple(map(int, version.split(".")[:2])) < (3, 12)
    index = constraint_index if constraint_index is not None else TokenizerConstraintIndex(tokenizer)

    raw_inputs: list[str] = []
    model_inputs: list[str] = []
    valid_targets: list[str] = []
    valid_meta: list[tuple[int, int]] = []  # (stmt_idx, mask_count)

    for stmt_idx, row in enumerate(statements):
        bc = row.get("bytecode") or ""
        src = row.get("source") or ""
        if not bc or not src:
            stats["drop_empty"] += 1
            continue
        mc = _mask_count(bc)
        if not check_statement_constraints(src, py_lt_312=py_lt_312, mask_count=mc):
            stats["drop_constraint_fail"] += 1
            continue
        raw_enc = encode_opcodes(bc)
        raw_inputs.append(raw_enc)
        model_inputs.append(f"v{version} <SEP> {raw_enc}" if use_version_prefix else raw_enc)
        valid_targets.append(src)
        valid_meta.append((stmt_idx, mc))

    if not raw_inputs:
        return []

    enc_raw_inputs = tokenizer(raw_inputs, truncation=False, add_special_tokens=True)["input_ids"]
    enc_model_inputs = (
        tokenizer(model_inputs, truncation=False, add_special_tokens=True)["input_ids"]
        if use_version_prefix
        else enc_raw_inputs
    )
    enc_targets = tokenizer(valid_targets, truncation=False, add_special_tokens=True)["input_ids"]
    empty_specials = {
        tid
        for role in ("bos", "eos", "pad")
        if (tid := getattr(tokenizer, f"{role}_token_id", None)) is not None
    }
    raw_input_cap = max(1, max_input_len - PREFIX_HEADROOM)

    kept: list[tuple[list[int], list[int], str, int, str, int]] = []
    for raw_ids, inp_ids, tgt_ids, src, (stmt_idx, mc) in zip(
        enc_raw_inputs, enc_model_inputs, enc_targets, valid_targets, valid_meta
    ):
        if len(raw_ids) > raw_input_cap or len(inp_ids) > max_input_len:
            stats["drop_input_too_long"] += 1
            continue
        if len(tgt_ids) > max_target_len:
            stats["drop_target_too_long"] += 1
            continue
        if not any(tid not in empty_specials for tid in tgt_ids):
            stats["drop_empty"] += 1
            continue
        # Validate against exact inference TokenizerConstraintIndex contract
        if not index.check_token_sequence(tgt_ids, py_lt_312=py_lt_312, mask_count=mc):
            stats["drop_token_constraint_fail"] += 1
            continue
        # Enforce singleton attention budget identically across prefix/no-prefix runs
        if max_attention_cost is not None:
            effective_enc = max(len(inp_ids), len(raw_ids) + PREFIX_HEADROOM)
            if _attention_cost(effective_enc, len(tgt_ids)) > max_attention_cost:
                stats["drop_attention_budget"] += 1
                continue

        if len(tgt_ids) > 256:
            bin_name = "tgt_long"
        elif len(raw_ids) > 256:
            bin_name = "enc_long"
        else:
            bin_name = "short"
        stats[f"kept_{bin_name}"] += 1
        kept.append((inp_ids, tgt_ids, bin_name, stmt_idx, src if keep_source_text else "", mc))
    return kept


def iter_corpus_shards(
    corpus_repo: str,
    corpus_rev: str,
    shard_dir: Path,
    *,
    hf_cache_dir: Path,
    max_shards: int = 0,
    keep_shards: bool = False,
) -> Iterator[tuple[int, int, Path]]:
    """Download and yield one parquet shard at a time, cleaning disk after each shard."""
    api = HfApi()
    info = api.dataset_info(corpus_repo, revision=corpus_rev)
    parquet_files = sorted(f.rfilename for f in info.siblings if f.rfilename.endswith(".parquet"))
    if max_shards > 0:
        parquet_files = parquet_files[:max_shards]
    total = len(parquet_files)
    shard_dir.mkdir(parents=True, exist_ok=True)
    hf_cache_dir.mkdir(parents=True, exist_ok=True)
    for idx, rel in enumerate(parquet_files):
        local = Path(
            hf_hub_download(
                corpus_repo,
                rel,
                repo_type="dataset",
                revision=corpus_rev,
                local_dir=str(shard_dir),
                cache_dir=str(hf_cache_dir),
            )
        )
        try:
            yield idx, total, local
        finally:
            if not keep_shards:
                if local.exists() or local.is_symlink():
                    try:
                        resolved = local.resolve()
                        local.unlink(missing_ok=True)
                        if resolved != local and resolved.exists() and str(hf_cache_dir.resolve()) in str(resolved):
                            resolved.unlink(missing_ok=True)
                    except OSError:
                        pass
                xet_dir = hf_cache_dir / "xet"
                if xet_dir.exists():
                    shutil.rmtree(xet_dir, ignore_errors=True)


def prepare_training_pools(
    shard_iter: list[Path] | Iterator[tuple[int, int, Path]],
    tokenizer: PreTrainedTokenizerFast,
    *,
    use_version_prefix: bool,
    max_input_len: int,
    max_target_len: int,
    short_cap_per_version: int,
    val_short_per_version: int,
    holdout_files_per_version: int,
    seed: int,
    enc_long_cap_per_version: int = 50000,
    tgt_long_cap_per_version: int = 50000,
    val_long_per_version: int = 250,
    constraint_index: TokenizerConstraintIndex | None = None,
    max_attention_cost: int | None = None,
) -> tuple[dict[str, list[EncodedExample]], dict[str, list[EncodedExample]], dict[str, int]]:
    """Stream parquet shards into bounded deterministic train & val pools by length bin."""
    index = constraint_index if constraint_index is not None else TokenizerConstraintIndex(tokenizer)
    stats: Counter = Counter()

    train_caps = {
        "short": short_cap_per_version,
        "enc_long": enc_long_cap_per_version,
        "tgt_long": tgt_long_cap_per_version,
    }
    val_caps = {
        "short": val_short_per_version,
        "enc_long": val_long_per_version,
        "tgt_long": val_long_per_version,
    }
    train_res: dict[str, dict[str, _BoundedHashReservoir]] = {
        b: {} for b in ("short", "enc_long", "tgt_long")
    }
    val_res: dict[str, dict[str, _BoundedHashReservoir]] = {
        b: {} for b in ("short", "enc_long", "tgt_long")
    }

    if isinstance(shard_iter, list):
        total_shards = len(shard_iter)
        entries: Iterator[tuple[int, int, Path]] = ((i, total_shards, p) for i, p in enumerate(shard_iter))
    else:
        entries = shard_iter

    next_id = 0
    for shard_idx, total_shards, shard_path in entries:
        pf = pq.ParquetFile(shard_path)
        for rg in range(pf.num_row_groups):
            table = pf.read_row_group(rg, columns=["version", "canonical_sha256", "statement"])
            versions = table["version"].to_pylist()
            hashes = table["canonical_sha256"].to_pylist()
            stmt_lists = table["statement"].to_pylist()
            for raw_ver, canon_hash, stmts in zip(versions, hashes, stmt_lists):
                ver = str(raw_ver)
                canon = str(canon_hash)
                stats["files_seen"] += 1
                is_val = _is_holdout_file(canon, holdout_files_per_version)
                kept = filter_and_encode_statements(
                    stmts or [],
                    ver,
                    tokenizer,
                    use_version_prefix=use_version_prefix,
                    max_input_len=max_input_len,
                    max_target_len=max_target_len,
                    stats=stats,
                    constraint_index=index,
                    max_attention_cost=max_attention_cost,
                    keep_source_text=is_val,
                )
                for inp_ids, tgt_ids, bin_name, stmt_idx, src_text, mc in kept:
                    ex = EncodedExample(
                        input_ids=inp_ids,
                        label_ids=tgt_ids,
                        version=ver,
                        bin_name=bin_name,
                        example_id=next_id,
                        source_text=src_text,
                        mask_count=mc,
                    )
                    next_id += 1
                    prio = _deterministic_priority(seed, canon, ver, stmt_idx)
                    target_res = val_res if is_val else train_res
                    caps = val_caps if is_val else train_caps
                    ver_map = target_res[bin_name]
                    if ver not in ver_map:
                        ver_map[ver] = _BoundedHashReservoir(caps[bin_name])
                    ver_map[ver].add(prio, ex)

        print(
            json.dumps(
                {
                    "event": "shard_prepared",
                    "shard": shard_idx + 1,
                    "total_shards": total_shards,
                    "train_short": sum(len(r) for r in train_res["short"].values()),
                    "train_enc_long": sum(len(r) for r in train_res["enc_long"].values()),
                    "train_tgt_long": sum(len(r) for r in train_res["tgt_long"].values()),
                    "val_short": sum(len(r) for r in val_res["short"].values()),
                    "val_enc_long": sum(len(r) for r in val_res["enc_long"].values()),
                    "val_tgt_long": sum(len(r) for r in val_res["tgt_long"].values()),
                }
            ),
            flush=True,
        )

    train_pools = {
        b: [ex for v in sorted(train_res[b]) for ex in train_res[b][v].items()]
        for b in ("short", "enc_long", "tgt_long")
    }
    val_pools = {
        b: [ex for v in sorted(val_res[b]) for ex in val_res[b][v].items()]
        for b in ("short", "enc_long", "tgt_long")
    }
    return train_pools, val_pools, dict(stats)


class StratifiedBinSampler:
    """Samples examples from short / enc_long / tgt_long pools with version stratification,
    persistent exhaustion tracking, exact exposure accounting, and full resumable state.
    """

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

        self._by_id: dict[int, EncodedExample] = {}
        self._by_bin_ver: dict[str, dict[str, list[EncodedExample]]] = {}
        self._cursors: dict[str, dict[str, int]] = {}
        self._active_versions: dict[str, list[str]] = {}

        for bin_name in ("short", "enc_long", "tgt_long"):
            items = pools.get(bin_name) or []
            grouped: dict[str, list[EncodedExample]] = defaultdict(list)
            for item in items:
                self._by_id[item.example_id] = item
                grouped[item.version].append(item)
            for ver in sorted(grouped):
                self.rng.shuffle(grouped[ver])
            self._by_bin_ver[bin_name] = {ver: grouped[ver] for ver in sorted(grouped)}
            self._cursors[bin_name] = {ver: 0 for ver in sorted(grouped)}
            self._active_versions[bin_name] = [ver for ver in sorted(grouped) if grouped[ver]]

        self._active_bins: list[str] = [
            b for b in ("short", "enc_long", "tgt_long") if self._active_versions.get(b) and self.weights.get(b, 0.0) > 0.0
        ]

    def _draw_from_bin(self, bin_name: str) -> EncodedExample | None:
        active_vers = self._active_versions.get(bin_name)
        if not active_vers:
            return None
        ver_map = self._by_bin_ver[bin_name]
        cap = self.max_long_exposures if bin_name in ("enc_long", "tgt_long") and self.max_long_exposures > 0 else None

        order = list(active_vers)
        self.rng.shuffle(order)
        for ver in order:
            items = ver_map[ver]
            n = len(items)
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
            # Every example in (bin_name, ver) reached its exposure cap; permanently retire it
            self._cursors[bin_name][ver] = cur
            if ver in active_vers:
                active_vers.remove(ver)
        return None

    def take_one(self) -> EncodedExample:
        """Draw exactly one eligible example without wasting exposures."""
        while self._active_bins:
            ws = [self.weights[b] for b in self._active_bins]
            b = self.rng.choices(self._active_bins, weights=ws, k=1)[0]
            chosen = self._draw_from_bin(b)
            if chosen is not None:
                return chosen
            # Bin permanently exhausted; remove so it is never rescanned
            self._active_bins.remove(b)
        raise RuntimeError("All training bins exhausted")

    def take(self, count: int) -> list[EncodedExample]:
        return [self.take_one() for _ in range(count)]

    def state_dict(self) -> dict[str, Any]:
        return {
            "rng_state": self.rng.getstate(),
            "exposures": dict(self.exposures),
            "bin_draws": dict(self.bin_draws),
            "cursors": {b: dict(v) for b, v in self._cursors.items()},
            "active_bins": list(self._active_bins),
            "active_versions": {b: list(v) for b, v in self._active_versions.items()},
            "order_ids": {
                b: {ver: [ex.example_id for ex in items] for ver, items in ver_map.items()}
                for b, ver_map in self._by_bin_ver.items()
            },
        }

    def load_state_dict(self, state: dict[str, Any]) -> None:
        self.rng.setstate(state["rng_state"])
        self.exposures = Counter(state["exposures"])
        self.bin_draws = Counter(state["bin_draws"])
        self._cursors = {b: dict(v) for b, v in state["cursors"].items()}
        self._active_bins = list(state["active_bins"])
        self._active_versions = {b: list(v) for b, v in state["active_versions"].items()}
        for b, ver_orders in state["order_ids"].items():
            for ver, id_list in ver_orders.items():
                self._by_bin_ver[b][ver] = [self._by_id[eid] for eid in id_list]


def pack_2d_microbatches(
    examples: list[EncodedExample],
    *,
    max_attention_cost: int,
    max_microbatch_size: int,
) -> list[list[EncodedExample]]:
    """Sort examples by (input_len, label_len) and pack into strictly attention-budgeted microbatches."""
    ordered = sorted(examples, key=lambda ex: (len(ex.input_ids), len(ex.label_ids)))
    batches: list[list[EncodedExample]] = []
    cur: list[EncodedExample] = []
    max_e = 0
    max_d = 0
    for ex in ordered:
        e = len(ex.input_ids)
        d = len(ex.label_ids)
        singleton_cost = _attention_cost(e, d)
        if singleton_cost > max_attention_cost:
            raise ValueError(
                f"Single example ({e}x{d}, cost={singleton_cost}) exceeds max_attention_cost={max_attention_cost}"
            )
        cand_e = max(max_e, e)
        cand_d = max(max_d, d)
        cand_n = len(cur) + 1
        cand_cost = cand_n * _attention_cost(cand_e, cand_d)
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


def _max_safe_dec_len(enc_len: int, requested_dec_len: int, max_attention_cost: int) -> int:
    """Return the largest decoder length <= requested_dec_len fitting max_attention_cost for enc_len."""
    if _attention_cost(enc_len, requested_dec_len) <= max_attention_cost:
        return requested_dec_len
    if _attention_cost(enc_len, 1) > max_attention_cost:
        raise ValueError(
            f"Generation eval example (enc={enc_len}) exceeds max_attention_cost={max_attention_cost}"
        )
    disc = 4 * max_attention_cost - 3 * enc_len * enc_len
    d = min(requested_dec_len, max(1, (math.isqrt(disc) - enc_len) // 2))
    while d > 1 and _attention_cost(enc_len, d) > max_attention_cost:
        d -= 1
    return d


def _pack_eval_gen_batches(
    examples: list[EncodedExample],
    *,
    dec_len: int,
    max_attention_cost: int,
    max_batch_size: int,
) -> list[tuple[list[EncodedExample], int]]:
    """Pack generation-eval batches strictly under the hard attention budget (including singletons).

    Returns ``(chunk, eff_dec_len)`` pairs guaranteeing
    ``len(chunk) * _attention_cost(max_enc, eff_dec_len) <= max_attention_cost``.
    """
    ordered = sorted(examples, key=lambda ex: (len(ex.input_ids), ex.example_id))
    batches: list[tuple[list[EncodedExample], int]] = []
    cur: list[EncodedExample] = []
    cur_e = 0
    for ex in ordered:
        e = len(ex.input_ids)
        safe_d = _max_safe_dec_len(e, dec_len, max_attention_cost)
        if safe_d < dec_len:
            if cur:
                batches.append((cur, dec_len))
                cur = []
                cur_e = 0
            batches.append(([ex], safe_d))
            continue
        cand_n = len(cur) + 1
        cand_e = max(cur_e, e)
        if cur and (cand_n > max_batch_size or cand_n * _attention_cost(cand_e, dec_len) > max_attention_cost):
            batches.append((cur, dec_len))
            cur = [ex]
            cur_e = e
        else:
            cur.append(ex)
            cur_e = cand_e
    if cur:
        batches.append((cur, dec_len))
    return batches


def _is_oom_error(exc: BaseException) -> bool:
    if isinstance(exc, MemoryError):
        return True
    if hasattr(torch.cuda, "OutOfMemoryError") and isinstance(exc, torch.cuda.OutOfMemoryError):
        return True
    if isinstance(exc, RuntimeError):
        msg = str(exc).lower()
        return any(m in msg for m in ("out of memory", "cudnn_status_alloc_failed", "cuda error: out of memory"))
    return False


def _generate_chunk_with_backoff(
    model: T5ForConditionalGeneration,
    constraint_index: TokenizerConstraintIndex,
    chunk: list[EncodedExample],
    *,
    pad_id: int,
    device: torch.device,
    max_length: int,
    py_lt_312: bool,
    amp_enabled: bool,
) -> list[list[int]]:
    """Run constrained generation on ``chunk``, halving batch size on OOM."""
    max_in = max(len(ex.input_ids) for ex in chunk)
    inp = torch.full((len(chunk), max_in), pad_id, dtype=torch.long, device=device)
    attn = torch.zeros((len(chunk), max_in), dtype=torch.long, device=device)
    for row, ex in enumerate(chunk):
        inp[row, : len(ex.input_ids)] = torch.tensor(ex.input_ids, dtype=torch.long, device=device)
        attn[row, : len(ex.input_ids)] = 1
    mcs = [ex.mask_count for ex in chunk]

    try:
        with torch.amp.autocast(device_type=device.type, dtype=torch.bfloat16, enabled=amp_enabled):
            out = model.generate(
                input_ids=inp,
                attention_mask=attn,
                max_length=max_length,
                logits_processor=[StatementLogitsProcessor(constraint_index, mcs, py_lt_312=py_lt_312)],
            )
        return [r.tolist() for r in out]
    except Exception as exc:
        if not _is_oom_error(exc) or len(chunk) <= 1:
            raise
    if device.type == "cuda" and torch.cuda.is_available():
        torch.cuda.empty_cache()
    mid = len(chunk) // 2
    left = _generate_chunk_with_backoff(
        model,
        constraint_index,
        chunk[:mid],
        pad_id=pad_id,
        device=device,
        max_length=max_length,
        py_lt_312=py_lt_312,
        amp_enabled=amp_enabled,
    )
    right = _generate_chunk_with_backoff(
        model,
        constraint_index,
        chunk[mid:],
        pad_id=pad_id,
        device=device,
        max_length=max_length,
        py_lt_312=py_lt_312,
        amp_enabled=amp_enabled,
    )
    return left + right


@torch.no_grad()
def evaluate_generation(
    model: T5ForConditionalGeneration,
    tokenizer: PreTrainedTokenizerFast,
    constraint_index: TokenizerConstraintIndex,
    val_pools: dict[str, list[EncodedExample]],
    device: torch.device,
    *,
    max_samples: int,
    max_length: int = 512,
    retry_max_length: int = 1024,
    batch_size: int = 16,
    max_attention_cost: int = 5_200_000,
    use_bf16: bool = False,
) -> dict[str, Any]:
    """Evaluate actual constrained greedy generation on a fixed paired validation subset.

    Packs both initial and cap-exhaustion retry passes within ``max_attention_cost`` with
    OOM batch-halving backoff. Measures natural EOS completion, completed constraint compliance,
    completed Python AST syntax parseability, and completed exact gold match separately for
    short, enc_long, and tgt_long validation bins.
    """
    if max_samples <= 0:
        return {}
    was_training = model.training
    prev_use_cache = model.config.use_cache
    model.eval()
    model.config.use_cache = True
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else 0
    eos_id = tokenizer.eos_token_id
    roles = ("bos", "eos", "pad", "unk", "mask", "cls", "sep")
    excluded = {tid for role in roles if (tid := getattr(tokenizer, f"{role}_token_id", None)) is not None}
    bad_words_ids = getattr(getattr(model, "generation_config", None), "bad_words_ids", None) or []
    excluded.update(tid for group in bad_words_ids for tid in group)

    # Take a deterministic version-stratified slice across non-empty bins (so all versions are covered)
    non_empty = [b for b in ("short", "enc_long", "tgt_long") if val_pools.get(b)]
    if not non_empty:
        model.config.use_cache = prev_use_cache
        if was_training:
            model.train()
        return {}
    per_bin = max(1, max_samples // len(non_empty))
    sample: list[EncodedExample] = []
    for b in non_empty:
        by_ver: dict[str, list[EncodedExample]] = defaultdict(list)
        for ex in val_pools[b]:
            by_ver[ex.version].append(ex)
        vers = sorted(by_ver)
        picked = 0
        idx = 0
        while picked < per_bin:
            added_any = False
            for v in vers:
                if idx < len(by_ver[v]):
                    sample.append(by_ver[v][idx])
                    picked += 1
                    added_any = True
                    if picked >= per_bin:
                        break
            if not added_any:
                break
            idx += 1

    # Group by py_lt_312 so each batch runs a single StatementLogitsProcessor
    amp_enabled = use_bf16 and device.type == "cuda"
    totals: dict[str, Counter] = {"short": Counter(), "enc_long": Counter(), "tgt_long": Counter()}

    try:
        for py_lt_312 in (True, False):
            subset = [ex for ex in sample if (tuple(map(int, ex.version.split(".")[:2])) < (3, 12)) == py_lt_312]
            if not subset:
                continue
            rows_by_id: dict[int, list[int]] = {}
            exhausted_examples: list[EncodedExample] = []

            for chunk, eff_max_len in _pack_eval_gen_batches(
                subset,
                dec_len=max_length,
                max_attention_cost=max_attention_cost,
                max_batch_size=batch_size,
            ):
                rows = _generate_chunk_with_backoff(
                    model,
                    constraint_index,
                    chunk,
                    pad_id=pad_id,
                    device=device,
                    max_length=eff_max_len,
                    py_lt_312=py_lt_312,
                    amp_enabled=amp_enabled,
                )
                for ex, toks in zip(chunk, rows):
                    rows_by_id[ex.example_id] = toks
                    if (
                        eos_id is not None
                        and eff_max_len < retry_max_length
                        and len(toks) >= eff_max_len
                        and eos_id not in toks[1:]
                        and _max_safe_dec_len(len(ex.input_ids), retry_max_length, max_attention_cost) > eff_max_len
                    ):
                        exhausted_examples.append(ex)

            # Match CacheTranslator's cap-exhaustion retry, repacked under the retry_max_length budget
            if exhausted_examples:
                for retry_chunk, eff_retry_len in _pack_eval_gen_batches(
                    exhausted_examples,
                    dec_len=retry_max_length,
                    max_attention_cost=max_attention_cost,
                    max_batch_size=batch_size,
                ):
                    retry_rows = _generate_chunk_with_backoff(
                        model,
                        constraint_index,
                        retry_chunk,
                        pad_id=pad_id,
                        device=device,
                        max_length=eff_retry_len,
                        py_lt_312=py_lt_312,
                        amp_enabled=amp_enabled,
                    )
                    for ex, r_toks in zip(retry_chunk, retry_rows):
                        rows_by_id[ex.example_id] = r_toks

            for ex in subset:
                toks = rows_by_id[ex.example_id]
                c = totals[ex.bin_name]
                c["n"] += 1
                has_eos = eos_id is None or eos_id in toks[1:]
                if not has_eos:
                    continue
                c["eos"] += 1
                decoded = tokenizer.decode(
                    [t for t in toks if t not in excluded],
                    skip_special_tokens=False,
                    clean_up_tokenization_spaces=False,
                )
                if constraint_index.check_token_sequence(
                    toks[1:], py_lt_312=py_lt_312, mask_count=ex.mask_count
                ) and check_statement_constraints(decoded, py_lt_312=py_lt_312, mask_count=ex.mask_count):
                    c["constraint_ok"] += 1
                if check_masked_statement_parses(decoded, ex.version):
                    c["parse_ok"] += 1
                if ex.source_text and decoded.strip() == ex.source_text.strip():
                    c["exact"] += 1
    finally:
        model.config.use_cache = prev_use_cache
        if was_training:
            model.train()

    summary: dict[str, Any] = {}
    for bucket in ("short", "enc_long", "tgt_long"):
        c = totals[bucket]
        n = c["n"]
        if n > 0:
            summary[bucket] = {
                "n": n,
                "eos_rate": round(c["eos"] / n, 4),
                "constraint_rate": round(c["constraint_ok"] / n, 4),
                "parse_rate": round(c["parse_ok"] / n, 4),
                "exact_match": round(c["exact"] / n, 4),
            }
    return summary


def save_weights_bundle(
    model: T5ForConditionalGeneration,
    out_dir: Path,
    *,
    use_version_prefix: bool,
    metadata: dict[str, Any],
    trainer_state: dict[str, Any] | None = None,
) -> None:
    """Crash-safe atomic replacement of a checkpoint directory via .tmp / .prev swap.

    When ``trainer_state`` is provided, it is written inside ``tmp_dir`` before the directory
    swap so weights, metadata, and optimizer/sampler/RNG state update atomically together.
    """
    tmp_dir = out_dir.with_name(out_dir.name + ".tmp")
    prev_dir = out_dir.with_name(out_dir.name + ".prev")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    if prev_dir.exists():
        shutil.rmtree(prev_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prev_use_cache = model.config.use_cache
    model.config.use_cache = True
    model.config.pylingual_version_prefix = bool(use_version_prefix)
    try:
        model.save_pretrained(tmp_dir)
    finally:
        model.config.use_cache = prev_use_cache
    (tmp_dir / "pylingual_training_meta.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if trainer_state is not None:
        torch.save(trainer_state, tmp_dir / "trainer_state.pt")

    moved_old = False
    if out_dir.exists():
        out_dir.rename(prev_dir)
        moved_old = True
    try:
        tmp_dir.rename(out_dir)
    except Exception:
        if moved_old and prev_dir.exists() and not out_dir.exists():
            prev_dir.rename(out_dir)
        raise
    if moved_old and prev_dir.exists():
        shutil.rmtree(prev_dir)


def upload_bundle_resilient(folder: Path, repo_id: str, *, public: bool, commit_message: str, retries: int = 3) -> bool:
    """Upload a checkpoint bundle to HuggingFace Hub with retries; never crashes training."""
    api = HfApi()
    for attempt in range(1, retries + 1):
        try:
            api.create_repo(repo_id, exist_ok=True, private=not public)
            api.upload_folder(
                folder_path=str(folder),
                repo_id=repo_id,
                commit_message=commit_message,
            )
            print(json.dumps({"event": "hub_upload_ok", "repo_id": repo_id, "attempt": attempt}), flush=True)
            return True
        except Exception as exc:
            print(
                json.dumps(
                    {
                        "event": "hub_upload_error",
                        "repo_id": repo_id,
                        "attempt": attempt,
                        "retries": retries,
                        "error": repr(exc),
                    }
                ),
                flush=True,
            )
            if attempt < retries:
                time.sleep(min(30, 5 * attempt))
    return False


def _seed_everything(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _available_ram_gib() -> float | None:
    """Return available Linux host RAM in GiB from /proc/meminfo, or None if unavailable."""
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return None
    for line in meminfo.read_text().splitlines():
        if line.startswith("MemAvailable:"):
            parts = line.split()
            if len(parts) >= 2:
                return int(parts[1]) / (1024**2)
    return None


def _preflight_checks(work_dir: Path, args: argparse.Namespace) -> tuple[torch.device, bool]:
    """Fail loudly before spending compute if CUDA, BF16, VRAM, RAM, disk, or Hub access is insufficient."""
    free_vram_gib: float | None = None
    if args.cpu:
        device = torch.device("cpu")
        use_bf16 = False
    else:
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available (pass --cpu explicitly for CPU smoke runs)")
        device = torch.device("cuda")
        use_bf16 = not args.no_bf16
        if use_bf16 and not torch.cuda.is_bf16_supported():
            raise RuntimeError("BF16 requested on CUDA device that does not support bfloat16 (pass --no-bf16)")
        free_vram, total_vram = torch.cuda.mem_get_info(device)
        free_vram_gib = free_vram / (1024**3)
        if args.min_free_vram_gib > 0 and free_vram_gib < args.min_free_vram_gib:
            raise RuntimeError(
                f"Insufficient free CUDA VRAM on {device}: {free_vram_gib:.2f} GiB free "
                f"(total {total_vram / (1024**3):.2f} GiB) < required {args.min_free_vram_gib:.2f} GiB"
            )

    free_ram_gib = _available_ram_gib()
    if args.min_free_ram_gib > 0 and free_ram_gib is not None and free_ram_gib < args.min_free_ram_gib:
        raise RuntimeError(
            f"Insufficient available host RAM: {free_ram_gib:.2f} GiB available < required {args.min_free_ram_gib:.2f} GiB"
        )

    free_gib = shutil.disk_usage(work_dir).free / (1024**3)
    if args.min_free_gib > 0 and free_gib < args.min_free_gib:
        raise RuntimeError(
            f"Insufficient free space on {work_dir}: {free_gib:.2f} GiB free < required {args.min_free_gib:.2f} GiB"
        )
    if args.hub_repo:
        # Validate Hub credentials and write permissions before spending GPU compute
        HfApi().create_repo(args.hub_repo, exist_ok=True, private=not args.public)
    print(
        json.dumps(
            {
                "event": "preflight_ok",
                "device": str(device),
                "bf16": use_bf16,
                "free_disk_gib": round(free_gib, 2),
                "free_ram_gib": round(free_ram_gib, 2) if free_ram_gib is not None else None,
                "free_vram_gib": round(free_vram_gib, 2) if free_vram_gib is not None else None,
            }
        ),
        flush=True,
    )
    return device, use_bf16


def _recover_prev_dir(target_dir: Path) -> None:
    prev_dir = target_dir.with_name(target_dir.name + ".prev")
    if not target_dir.exists() and prev_dir.exists():
        prev_dir.rename(target_dir)


def train(args: argparse.Namespace) -> dict[str, Any]:
    work_dir = Path(args.work_dir).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    hf_cache_dir = work_dir / "hf_cache"
    hf_cache_dir.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HOME"] = str(hf_cache_dir)
    os.environ["HF_HUB_CACHE"] = str(hf_cache_dir / "hub")
    os.environ["HF_XET_CACHE"] = str(hf_cache_dir / "xet")
    hf_constants.HF_HOME = str(hf_cache_dir)
    hf_constants.HF_HUB_CACHE = str(hf_cache_dir / "hub")

    device, use_bf16 = _preflight_checks(work_dir, args)
    _seed_everything(args.seed)
    if device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True

    tokenizer = PreTrainedTokenizerFast.from_pretrained(
        args.tokenizer_repo,
        revision=args.tokenizer_rev,
        subfolder="statement",
        cache_dir=str(hf_cache_dir),
    )

    latest_dir = work_dir / "latest_model"
    best_dir = work_dir / "best_model"

    local_shard_meta = None
    if args.local_shards:
        local_shard_meta = []
        for p_str in args.local_shards:
            p = Path(p_str).resolve()
            st = p.stat()
            local_shard_meta.append({"path": str(p), "size": st.st_size, "mtime_ns": st.st_mtime_ns})

    config_fingerprint = {
        "base_model": args.base_model,
        "base_rev": args.base_rev,
        "tokenizer_repo": args.tokenizer_repo,
        "tokenizer_rev": args.tokenizer_rev,
        "corpus_repo": args.corpus_repo,
        "corpus_rev": args.corpus_rev,
        "local_shards": local_shard_meta,
        "max_shards": int(args.max_shards),
        "version_prefix": bool(args.version_prefix),
        "max_input_len": int(args.max_input_len),
        "max_target_len": int(args.max_target_len),
        "short_cap_per_version": int(args.short_cap_per_version),
        "enc_long_cap_per_version": int(args.enc_long_cap_per_version),
        "tgt_long_cap_per_version": int(args.tgt_long_cap_per_version),
        "val_short_per_version": int(args.val_short_per_version),
        "val_long_per_version": int(args.val_long_per_version),
        "holdout_files_per_version": int(args.holdout_files_per_version),
        "max_attention_cost": int(args.max_attention_cost),
        "target_tokens_per_step": int(args.target_tokens_per_step),
        "max_microbatch_size": int(args.max_microbatch_size),
        "weight_short": float(args.weight_short),
        "weight_enc_long": float(args.weight_enc_long),
        "weight_tgt_long": float(args.weight_tgt_long),
        "max_long_exposures": int(args.max_long_exposures),
        "steps": int(args.steps),
        "lr": float(args.lr),
        "min_lr": float(args.min_lr),
        "warmup_frac": float(args.warmup_frac),
        "weight_decay": float(args.weight_decay),
        "grad_clip": float(args.grad_clip),
        "use_bf16": bool(use_bf16),
        "gradient_checkpointing": bool(args.gradient_checkpointing),
        "seed": int(args.seed),
    }

    resuming = False
    resume_state: dict[str, Any] | None = None
    if args.resume:
        _recover_prev_dir(latest_dir)
        _recover_prev_dir(best_dir)
        state_path = latest_dir / "trainer_state.pt"
        if latest_dir.exists() and state_path.exists():
            resuming = True
            resume_state = torch.load(state_path, map_location="cpu", weights_only=False)
            meta_path = latest_dir / "pylingual_training_meta.json"
            if meta_path.exists():
                saved_meta = json.loads(meta_path.read_text())
                if saved_meta.get("step") != resume_state.get("step"):
                    raise ValueError(
                        f"Checkpoint weights/state step mismatch: meta={saved_meta.get('step')} vs state={resume_state.get('step')}"
                    )
            saved_fp = resume_state.get("config_fingerprint")
            if saved_fp is not None and saved_fp != config_fingerprint:
                raise ValueError(f"Resume config mismatch: saved={saved_fp} vs current={config_fingerprint}")
            model = T5ForConditionalGeneration.from_pretrained(latest_dir)
            print(json.dumps({"event": "resuming", "from_step": resume_state["step"], "latest_dir": str(latest_dir)}), flush=True)
        else:
            print(json.dumps({"event": "resume_not_found_starting_fresh", "work_dir": str(work_dir)}), flush=True)
            model = T5ForConditionalGeneration.from_pretrained(
                args.base_model, revision=args.base_rev, cache_dir=str(hf_cache_dir)
            )
    else:
        model = T5ForConditionalGeneration.from_pretrained(
            args.base_model, revision=args.base_rev, cache_dir=str(hf_cache_dir)
        )

    if model.get_input_embeddings().num_embeddings != len(tokenizer):
        raise ValueError("Model embedding size does not match frozen statement tokenizer")
    model.to(device)
    model.config.use_cache = False
    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    bad_words_ids = getattr(getattr(model, "generation_config", None), "bad_words_ids", None) or []
    constraint_index = TokenizerConstraintIndex(tokenizer, bad_words_ids=bad_words_ids)

    if args.local_shards:
        shard_source: list[Path] | Iterator[tuple[int, int, Path]] = [Path(p) for p in args.local_shards]
    else:
        shard_source = iter_corpus_shards(
            args.corpus_repo,
            args.corpus_rev,
            work_dir / "shards",
            hf_cache_dir=hf_cache_dir,
            max_shards=args.max_shards,
            keep_shards=args.keep_shards,
        )

    train_pools, val_pools, data_stats = prepare_training_pools(
        shard_source,
        tokenizer,
        use_version_prefix=args.version_prefix,
        max_input_len=args.max_input_len,
        max_target_len=args.max_target_len,
        short_cap_per_version=args.short_cap_per_version,
        val_short_per_version=args.val_short_per_version,
        enc_long_cap_per_version=args.enc_long_cap_per_version,
        tgt_long_cap_per_version=args.tgt_long_cap_per_version,
        val_long_per_version=args.val_long_per_version,
        holdout_files_per_version=args.holdout_files_per_version,
        seed=args.seed,
        constraint_index=constraint_index,
        max_attention_cost=args.max_attention_cost,
    )
    print(
        json.dumps(
            {
                "event": "data_ready",
                "stats": data_stats,
                "train_sizes": {k: len(v) for k, v in train_pools.items()},
                "val_sizes": {k: len(v) for k, v in val_pools.items()},
            }
        ),
        flush=True,
    )

    sampler = StratifiedBinSampler(
        train_pools,
        weights={"short": args.weight_short, "enc_long": args.weight_enc_long, "tgt_long": args.weight_tgt_long},
        max_long_exposures=args.max_long_exposures,
        seed=args.seed,
    )
    optimizer = build_optimizer(model, lr=args.lr, weight_decay=args.weight_decay)
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else 0

    def _selection_score(val_dict: dict[str, float]) -> float:
        vals = [v for v in val_dict.values() if not math.isnan(v)]
        return sum(vals) / max(1, len(vals))

    eval_gen_max_len = min(512, args.max_target_len + 1)
    eval_gen_retry_max_len = min(1024, args.max_target_len + 1)

    if resuming and resume_state is not None:
        optimizer.load_state_dict(resume_state["optimizer"])
        sampler.load_state_dict(resume_state["sampler"])
        random.setstate(resume_state["python_rng_state"])
        torch.set_rng_state(resume_state["torch_rng_state"])
        if device.type == "cuda" and resume_state.get("cuda_rng_state") is not None:
            torch.cuda.set_rng_state_all(resume_state["cuda_rng_state"])
        start_step = int(resume_state["step"]) + 1
        best_score = float(resume_state["best_score"])
        best_step: int | None = resume_state.get("best_step")
        best_saved = bool(resume_state.get("best_saved", False))
        best_uploaded_step: int | None = resume_state.get("best_uploaded_step")
        baseline_short = float(resume_state["baseline_short"])
        history: list[dict[str, Any]] = list(resume_state["history"])
        # Release CPU copy of resumed AdamW state immediately to avoid holding ~1.8 GiB extra RAM
        resume_state = None
        gc.collect()
    else:
        val0 = evaluate_pools(
            model,
            val_pools,
            pad_id,
            device,
            max_attention_cost=args.max_attention_cost,
            max_microbatch_size=args.max_microbatch_size,
            use_bf16=use_bf16,
        )
        gen0 = evaluate_generation(
            model,
            tokenizer,
            constraint_index,
            val_pools,
            device,
            max_samples=args.eval_gen_samples,
            max_length=eval_gen_max_len,
            retry_max_length=eval_gen_retry_max_len,
            max_attention_cost=args.max_attention_cost,
            use_bf16=use_bf16,
        )
        print(json.dumps({"event": "eval", "step": 0, "val": val0, "gen": gen0}), flush=True)
        baseline_short = val0.get("short", float("inf"))
        best_score = _selection_score(val0)
        best_step = None
        best_saved = False
        best_uploaded_step = None
        history = [{"step": 0, "val": val0, "gen": gen0}]
        start_step = 1

    started = time.monotonic()
    model.train()
    end_step = min(args.steps, args.stop_after_step) if args.stop_after_step > 0 else args.steps

    for step in range(start_step, end_step + 1):
        lr = lr_for_step(step - 1, args.steps, args.lr, min_lr=args.min_lr, warmup_frac=args.warmup_frac)
        for group in optimizer.param_groups:
            group["lr"] = lr

        # Draw exactly one example at a time until reaching target_tokens_per_step (zero wasted exposures)
        step_examples: list[EncodedExample] = []
        step_target_tokens = 0
        while step_target_tokens < args.target_tokens_per_step:
            ex = sampler.take_one()
            step_examples.append(ex)
            step_target_tokens += len(ex.label_ids)

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

        if step % args.log_every == 0 or step == end_step:
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
                "free_disk_gib": round(shutil.disk_usage(work_dir).free / (1024**3), 2),
            }
            print(json.dumps(rec), flush=True)

        if step % args.eval_every == 0 or step == end_step:
            val = evaluate_pools(
                model,
                val_pools,
                pad_id,
                device,
                max_attention_cost=args.max_attention_cost,
                max_microbatch_size=args.max_microbatch_size,
                use_bf16=use_bf16,
            )
            gen = evaluate_generation(
                model,
                tokenizer,
                constraint_index,
                val_pools,
                device,
                max_samples=args.eval_gen_samples,
                max_length=eval_gen_max_len,
                retry_max_length=eval_gen_retry_max_len,
                max_attention_cost=args.max_attention_cost,
                use_bf16=use_bf16,
            )
            score = _selection_score(val)
            short_ok = math.isnan(val.get("short", float("nan"))) or math.isnan(baseline_short) or val["short"] <= baseline_short + 0.015
            improved = score < best_score and short_ok
            history.append({"step": step, "val": val, "gen": gen, "score": score, "improved": improved})
            print(
                json.dumps({"event": "eval", "step": step, "val": val, "gen": gen, "score": round(score, 5), "improved": improved}),
                flush=True,
            )

            if improved:
                best_score = score
                best_step = step
                best_saved = True

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
                "gen": gen,
                "best_score": best_score,
                "best_step": best_step,
                "best_saved": best_saved,
                "bin_draws": dict(sampler.bin_draws),
                "data_stats": data_stats,
            }
            if improved:
                save_weights_bundle(model, best_dir, use_version_prefix=args.version_prefix, metadata=meta)
                if args.hub_repo:
                    if upload_bundle_resilient(
                        best_dir,
                        args.hub_repo,
                        public=args.public,
                        commit_message=f"Best checkpoint at step {step} (val={val})",
                    ):
                        best_uploaded_step = step

            # Save latest_model weights, metadata, and trainer_state.pt together in one atomic directory swap
            trainer_state = {
                "config_fingerprint": config_fingerprint,
                "step": step,
                "best_score": best_score,
                "best_step": best_step,
                "best_saved": best_saved,
                "best_uploaded_step": best_uploaded_step,
                "baseline_short": baseline_short,
                "history": history,
                "data_stats": data_stats,
                "optimizer": optimizer.state_dict(),
                "sampler": sampler.state_dict(),
                "python_rng_state": random.getstate(),
                "torch_rng_state": torch.get_rng_state(),
                "cuda_rng_state": torch.cuda.get_rng_state_all() if device.type == "cuda" else None,
            }
            save_weights_bundle(
                model,
                latest_dir,
                use_version_prefix=args.version_prefix,
                metadata=meta,
                trainer_state=trainer_state,
            )

    # Final upload retry if the best checkpoint failed an earlier Hub upload
    if args.hub_repo and best_saved and best_uploaded_step != best_step and best_dir.exists():
        if upload_bundle_resilient(
            best_dir,
            args.hub_repo,
            public=args.public,
            commit_message=f"Final upload of best checkpoint from step {best_step}",
        ):
            best_uploaded_step = best_step

    summary = {
        "complete": end_step >= args.steps,
        "steps": end_step,
        "total_steps": args.steps,
        "best_score": best_score,
        "best_step": best_step,
        "best_saved": best_saved,
        "best_uploaded": bool(args.hub_repo and best_saved and best_uploaded_step == best_step),
        "best_model_path": str(best_dir) if best_saved and best_dir.exists() else None,
        "bin_draws": dict(sampler.bin_draws),
        "data_stats": data_stats,
        "history": history,
        "seconds": round(time.monotonic() - started, 1),
    }
    if not best_saved:
        print(json.dumps({"event": "no_improvement_over_baseline", "baseline_score": best_score}), flush=True)
    tmp_summary = work_dir / "summary.json.tmp"
    tmp_summary.write_text(json.dumps(summary, indent=2) + "\n")
    os.replace(tmp_summary, work_dir / "summary.json")
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
    p.add_argument("--keep-shards", action="store_true", help="Keep downloaded shards on disk after streaming")
    p.add_argument("--version-prefix", action="store_true", help="Prepend 'v{version} <SEP> ' to encoded bytecode")
    p.add_argument("--max-input-len", type=int, default=1536)
    p.add_argument("--max-target-len", type=int, default=1023, help="Max target tokens (1023 + decoder_start = 1024)")
    p.add_argument("--short-cap-per-version", type=int, default=60000)
    p.add_argument("--enc-long-cap-per-version", type=int, default=30000)
    p.add_argument("--tgt-long-cap-per-version", type=int, default=30000)
    p.add_argument("--val-short-per-version", type=int, default=500)
    p.add_argument("--val-long-per-version", type=int, default=250)
    p.add_argument("--holdout-files-per-version", type=int, default=150)
    p.add_argument("--weight-short", type=float, default=0.70)
    p.add_argument("--weight-enc-long", type=float, default=0.20)
    p.add_argument("--weight-tgt-long", type=float, default=0.10)
    p.add_argument("--max-long-exposures", type=int, default=4)
    p.add_argument("--target-tokens-per-step", type=int, default=8192)
    p.add_argument("--max-attention-cost", type=int, default=5_200_000)
    p.add_argument("--max-microbatch-size", type=int, default=64)
    p.add_argument("--steps", type=int, default=2500)
    p.add_argument("--stop-after-step", type=int, default=0, help="Optional early stop step within --steps schedule (for smoke/resume testing)")
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--min-lr", type=float, default=1e-6)
    p.add_argument("--warmup-frac", type=float, default=0.03)
    p.add_argument("--weight-decay", type=float, default=0.01)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--eval-every", type=int, default=250)
    p.add_argument("--eval-gen-samples", type=int, default=120, help="Stratified val statements for constrained generation eval")
    p.add_argument("--log-every", type=int, default=25)
    p.add_argument("--seed", type=int, default=20261123)
    p.add_argument("--min-free-gib", type=float, default=8.0, help="Minimum free disk GiB on work_dir before launch")
    p.add_argument("--min-free-ram-gib", type=float, default=4.0, help="Minimum available host RAM GiB before launch (0 disables)")
    p.add_argument("--min-free-vram-gib", type=float, default=16.0, help="Minimum free CUDA VRAM GiB before launch (0 disables)")
    p.add_argument("--resume", action="store_true", help="Resume from latest_model and trainer_state.pt in work_dir")
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
