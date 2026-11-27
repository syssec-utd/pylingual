# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../", editable = true }
# ///
"""
Benchmark a control flow model on a split of a compiled code dataset (one directory per file, see README.md). Every
model sees the same files with the gold segmentation and lines, so the numbers measure control flow alone.

For each code object whose gold skeleton recompiles to equivalent bytecode:
    predicted   the model gives a skeleton (ControlFlowPredictor keeps only skeletons the block grammar accepts)
    exact       its best skeleton is the gold skeleton
    compiles    the file compiles with the best skeleton for this code object and the gold ones elsewhere
    equivalent  ... and this code object's bytecode is equivalent
    any_k       one of the model's k best skeletons (beam search) is equivalent
and the model's greedy time per code object, with the requests of a file in one call.
"""

from __future__ import annotations

import json
import math
import multiprocessing
import signal
import tempfile
import time
from collections import Counter
from pathlib import Path

import click
import torch
import tqdm

from dataset_generation.bytecode2cflow import equivalent_names, load_pair, make_examples
from pylingual.control_flow_reconstruction.model_view import CflowRequest
from pylingual.models import ControlFlowPredictor, TransitionPredictor

FILE_TIMEOUT = 300  # seconds; a file with many code objects and beams recompiles once per candidate


class InOrder(ControlFlowPredictor):
    """No model: the statements in order, with the blocks BlockGrammar.complete gives them."""

    def __init__(self):
        super().__init__(max_stmts=1 << 30, max_input_tokens=1 << 30)

    def _generate(self, batch: list[CflowRequest], num_beams: int) -> list[list[list[str]]]:
        return [[r.grammar().complete(r.grammar().start())] for r in batch]


def _timeout(*_):
    raise TimeoutError(f"file took over {FILE_TIMEOUT}s")


def with_timeout(fn, *args):
    signal.signal(signal.SIGALRM, _timeout)
    signal.alarm(FILE_TIMEOUT)
    try:
        return fn(*args)
    except Exception as error:
        return Exception(f"{type(error).__name__}: {error} in {args[0]}")
    finally:
        signal.alarm(0)


def gold_rows(py: Path) -> list[dict]:
    """Examples of a file whose gold skeleton is equivalent and whose name is unique."""
    with tempfile.TemporaryDirectory() as tmp:
        src, pyc, pyc_path = load_pair(py, py.with_suffix(".pyc"), Path(tmp))
        examples = make_examples(pyc, src)
        ok = equivalent_names(pyc, pyc_path, src, examples, Path(tmp) / "gold.py") if examples else None
    names = Counter(e["name"] for e in examples)
    return [{k: v for k, v in e.items() if not k.startswith("_")} for e in examples if ok and e["name"] in ok and names[e["name"]] == 1]


def gold_rows_or_error(py: Path) -> list[dict] | Exception:
    return with_timeout(gold_rows, py)


def check(py: Path, candidates: dict[str, list[list[str]]]) -> dict[str, list[tuple[bool, bool]]]:
    """(compiles, equivalent) of each candidate skeleton of each code object, with the gold skeletons elsewhere."""
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for name, skeletons in candidates.items():
            out[name] = []
            for tokens in skeletons:
                # labeling lines changes the bytecode it reads, so each render starts from the file again
                src, pyc, pyc_path = load_pair(py, py.with_suffix(".pyc"), Path(tmp))
                guess = [e | {"target": " ".join(tokens)} if e["name"] == name else e for e in make_examples(pyc, src)]
                names = equivalent_names(pyc, pyc_path, src, guess, Path(tmp) / "guess.py")
                out[name].append((names is not None, names is not None and name in names))
    return out


def bucket(n: int) -> str:
    return f"<={max(8, 2 ** math.ceil(math.log2(n)))}"


@click.command(help="Benchmark a control flow model on a compiled code dataset split.")
@click.argument("code_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--model", help="HuggingFace repo or local directory of the model")
@click.option("--baseline", is_flag=True, help="No model: statements in order (see InOrder)")
@click.option("--beams", default=4, help="k for any_k")
@click.option("--limit", default=1000, help="Files to use, the first in name order")
@click.option("--out", type=click.Path(path_type=Path), help="Write the report JSON here")
@click.option("--rows", type=click.Path(path_type=Path), help="Write the result of each code object here (JSONL)")
def main(code_dir: Path, model: str | None, baseline: bool, beams: int, limit: int, out: Path | None, rows: Path | None):
    if baseline == bool(model):
        raise click.UsageError("give --model or --baseline")
    files = [py for d in sorted(code_dir.iterdir()) if (py := next(d.glob("*.py"), None)) and py.with_suffix(".pyc").exists()][:limit]

    failed = []
    # the pool forks before the model loads, so the workers hold no GPU state
    with multiprocessing.Pool(maxtasksperchild=50) as pool:
        examples = {}
        for py, result in zip(files, tqdm.tqdm(pool.imap(gold_rows_or_error, files), total=len(files), desc="gold")):
            if isinstance(result, Exception):
                failed.append(str(result))
            elif result:
                examples[py] = result

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        predictor = InOrder() if baseline else TransitionPredictor.from_pretrained(model, device=device)
        candidates, seconds = {}, 0.0
        for py, file_examples in tqdm.tqdm(examples.items(), desc="predict"):
            requests = [CflowRequest.from_row(e) for e in file_examples]
            start = time.perf_counter()
            greedy = predictor(requests, fallback=False)
            seconds += time.perf_counter() - start
            beam = predictor(requests, num_beams=beams, fallback=False) if beams > 1 else greedy
            candidates[py] = {}
            for e, g, k in zip(file_examples, greedy, beam):
                e["greedy"] = g[0] if g else None
                candidates[py][e["name"]] = ([e["greedy"]] if g else []) + [b for b in k or [] if b != e["greedy"]]

        checked = pool.starmap(with_timeout, [(check, py, candidates[py]) for py in examples])

    records = []
    for (py, file_examples), results in zip(examples.items(), checked):
        if isinstance(results, Exception):
            failed.append(str(results))
            continue
        for e in file_examples:
            outcomes = results[e["name"]]
            greedy_ok = e["greedy"] is not None and bool(outcomes)
            records.append({
                "file": str(py), "name": e["name"], "n_stmts": e["n_stmts"],
                "predicted": e["greedy"] is not None,
                "exact": e["greedy"] == e["target"].split(),
                "compiles": greedy_ok and outcomes[0][0],
                "equivalent": greedy_ok and outcomes[0][1],
                "any_k": any(eq for _, eq in outcomes),
            })  # fmt: skip

    n = max(len(records), 1)
    by_size = {}
    for r in records:
        by_size.setdefault(bucket(r["n_stmts"]), []).append(r["equivalent"])
    report = {
        "model": "baseline" if baseline else model,
        "files": len(files),
        "failed_files": len(failed),
        "code_objects": len(records),
        **{key: sum(r[key] for r in records) / n for key in ("predicted", "exact", "compiles", "equivalent", "any_k")},
        "k": beams,
        "ms_per_code_object": 1000 * seconds / n,
        "equivalent_by_n_stmts": {b: sum(v) / len(v) for b, v in sorted(by_size.items(), key=lambda x: int(x[0][2:]))},
    }
    print(json.dumps(report, indent=2))
    if out:
        out.write_text(json.dumps(report, indent=2))
    if rows:
        rows.write_text("".join(json.dumps(r) + "\n" for r in records))


if __name__ == "__main__":
    main()
