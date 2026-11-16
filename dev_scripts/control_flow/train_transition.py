import json
import math
import os
import pathlib
import time
from datetime import timedelta

import click
import numpy as np
import torch
import transformers
from ControlFlowConfiguration import ControlFlowConfiguration, parse_control_flow_config_json
from datasets import load_dataset
from transformers import Trainer, TrainingArguments

from pylingual.control_flow_reconstruction.block_grammar import BlockGrammar, Shape
from pylingual.control_flow_reconstruction.model_view import INPUT_TOKENS, CflowRequest
from pylingual.control_flow_reconstruction.skeleton import parse_ref
from pylingual.control_flow_reconstruction.transition import ALIGN, SPECIAL, STMT, TOKENS, Parse, TransitionConfig, TransitionModel, advance, allowed_row, encode_input, features, gold_actions
from pylingual.models import TransitionPredictor


def load_cflow_dataset(config: ControlFlowConfiguration):
    """The train/valid/test JSONL splits of every dataset dir, without the code objects too large for the model."""
    splits = {"train": "train", "validation": "valid", "test": "test"}
    dataset = load_dataset("json", data_files={split: [str(d / f"{name}.jsonl") for d in config.dataset_dirs] for split, name in splits.items()})
    return dataset.filter(lambda row: row["n_stmts"] <= config.max_stmts and len(row["input"].split()) < config.max_input_tokens)


def build_vocab(texts) -> list[str]:
    """Special and input structure tokens first, then every other token in `texts` but statement references."""
    fixed = [*SPECIAL, *INPUT_TOKENS]
    return fixed + sorted({t for text in texts for t in text.split() if parse_ref(t) is None} - set(fixed))


def collate(rows: list[dict]) -> dict[str, torch.Tensor]:
    """Encoder inputs, and the decoder features, allowed actions and action of each step of the gold skeletons."""
    # at least 2 statement slots: with 1, the pointer's backward is an outer product bmm, which torch 2.14 runs as a
    # triton kernel that needs a C compiler
    n, length = max(2, *(row["n_stmts"] for row in rows)), -(-max(row["length"] for row in rows) // ALIGN) * ALIGN
    steps = []
    for row in rows:
        grammar = BlockGrammar([Shape.parse(s) for s in row["shapes"].split()], row["version"])
        parse, walk = Parse(grammar.start()), []
        for action in gold_actions(row["target"].split()):
            walk.append((features(grammar, parse), allowed_row(grammar, parse.state, n), action.stmt if action.token == STMT else n + action.token))
            parse = advance(grammar, parse, action)
        steps.append(walk)
    t = max(map(len, steps))
    batch = {
        "input_ids": np.zeros((len(rows), length), dtype=np.int64),
        "refs": np.full((len(rows), length), -1, dtype=np.int64),
        "attention_mask": np.zeros((len(rows), length), dtype=bool),
        "stmt_pos": np.zeros((len(rows), n), dtype=np.int64),
        "features": np.zeros((len(rows), t, 9), dtype=np.int64),
        "allowed": np.zeros((len(rows), t, n + len(TOKENS)), dtype=bool),
        "labels": np.full((len(rows), t), -100, dtype=np.int64),
    }
    for b, (row, walk) in enumerate(zip(rows, steps)):
        batch["input_ids"][b, : row["length"]] = row["input_ids"]
        batch["refs"][b, : row["length"]] = row["refs"]
        batch["attention_mask"][b, : row["length"]] = True
        batch["stmt_pos"][b, : len(row["stmt_pos"])] = row["stmt_pos"]
        for s, (feats, allowed, label) in enumerate(walk):
            batch["features"][b, s], batch["allowed"][b, s], batch["labels"][b, s] = feats, allowed, label
    return {k: torch.from_numpy(v) for k, v in batch.items()}


class BudgetBatches(torch.utils.data.Sampler):
    """
    Batches of rows of similar size, of at most `rows` rows, `rows * TOKENS_PER_ROW` padded input tokens and
    `rows * CELLS_PER_ROW` padded decoder step x statement cells (the size of the pointer logits), so the few very large
    code objects train in small batches instead of running out of memory.

    When `shuffle`, each epoch (seeded by `seed` and the epoch) splits the shuffled rows into megabatches of MEGABATCH
    batches, sorts each by size and cuts it into batches, like group_by_length; batches of mixed sizes train better than
    batches cut from all rows sorted by size. The batch count varies a little between epochs; the trainer runs
    `len(self)` steps each epoch. Otherwise the batches are cut from all rows sorted by size.
    """

    TOKENS_PER_ROW = 512
    CELLS_PER_ROW = 1 << 16
    MEGABATCH = 50

    def __init__(self, dataset, rows: int, shuffle: bool, seed: int):
        self.sizes = np.stack([np.array(dataset[c]) for c in ("length", "n_stmts", "steps")], 1)
        self.rows, self.shuffle, self.seed, self.epoch = rows, shuffle, seed, 0
        self.count = len(self.batches(0))

    def cut(self, order: np.ndarray) -> list[list[int]]:
        """Batches of `order`, largest rows first."""
        order = order[np.lexsort(self.sizes[order].T[[2, 1, 0]])[::-1]]
        batches, batch, size = [], [], np.zeros(3, dtype=np.int64)
        for i in order.tolist():
            grown = np.maximum(size, self.sizes[i])
            k = len(batch) + 1
            if batch and (k > self.rows or k * grown[0] > self.rows * self.TOKENS_PER_ROW or k * grown[1] * grown[2] > self.rows * self.CELLS_PER_ROW):
                batches.append(batch)
                batch, grown = [], self.sizes[i]
            batch.append(i)
            size = grown
        return batches + [batch]

    def batches(self, epoch: int) -> list[list[int]]:
        if not self.shuffle:
            return self.cut(np.arange(len(self.sizes)))
        rng = np.random.default_rng((self.seed, epoch))
        order, mega = rng.permutation(len(self.sizes)), self.rows * self.MEGABATCH
        batches = [b for start in range(0, len(order), mega) for b in self.cut(order[start : start + mega])]
        return [batches[i] for i in rng.permutation(len(batches))]

    def set_epoch(self, epoch: int):
        self.epoch = epoch

    def __len__(self):
        return self.count

    def __iter__(self):
        batches = self.batches(self.epoch)
        self.epoch += 1  # in case the trainer does not set it
        yield from batches


class BudgetTrainer(Trainer):
    def _budget_loader(self, dataset, shuffle: bool):
        sampler = BudgetBatches(dataset, self.args.per_device_train_batch_size, shuffle, self.args.seed)
        loader = torch.utils.data.DataLoader(dataset, batch_sampler=sampler, collate_fn=self.data_collator, num_workers=self.args.dataloader_num_workers, pin_memory=self.args.dataloader_pin_memory)
        return self.accelerator.prepare(loader)

    def get_train_dataloader(self):
        return self._budget_loader(self.train_dataset, shuffle=True)

    def get_eval_dataloader(self, eval_dataset=None):
        return self._budget_loader(eval_dataset if eval_dataset is not None else self.eval_dataset, shuffle=False)


def exact_match(predictor: TransitionPredictor, test) -> dict:
    """Share of greedy skeletons equal to the gold skeleton, by statement count."""
    predictions = predictor([CflowRequest.from_row(row) for row in test])
    buckets = {}
    for prediction, row in zip(predictions, test):
        bucket = buckets.setdefault(max(8, 2 ** math.ceil(math.log2(row["n_stmts"]))), [0, 0])
        bucket[0] += 1
        bucket[1] += bool(prediction) and prediction[0] == row["target"].split()
    return {
        "exact_match": sum(c for _, c in buckets.values()) / max(len(test), 1),
        "predicted": sum(map(bool, predictions)) / max(len(test), 1),
        "by_n_stmts": {f"<={b}": c / n for b, (n, c) in sorted(buckets.items())},
    }


def train_transition_model(config: ControlFlowConfiguration, public: bool = False, seed: int = 42):
    dataset = load_cflow_dataset(config)
    vocab = build_vocab(dataset["train"]["input"])
    index = {t: i for i, t in enumerate(vocab)}

    def tokenize(row):
        ids, refs, stmt_pos = encode_input(row["input"].split(), index)
        return {"input_ids": ids, "refs": refs, "stmt_pos": stmt_pos, "length": len(ids), "steps": len(row["target"].split()) + 1}

    tokenized = dataset.map(tokenize, remove_columns=["input", "file"], keep_in_memory=True)  # no 190 MB cache file per run

    transformers.set_seed(seed)  # the model is built before the trainer seeds
    params = config.model_parameters
    model = TransitionModel(TransitionConfig(
        vocab=vocab, d_model=params.d_model, layers=params.layers, heads=params.heads, d_ff=params.d_ff,
        max_stmts=config.max_stmts, max_input_tokens=config.max_input_tokens, products=True, decoder_layers=2,
    ))  # fmt: skip

    print(f"trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}")
    model_dir = config.model_dir
    train_args = TrainingArguments(
        output_dir=str(model_dir),
        per_device_train_batch_size=config.training_parameters.batch_size,
        per_device_eval_batch_size=config.training_parameters.batch_size,
        learning_rate=config.training_parameters.learning_rate,
        num_train_epochs=config.training_parameters.epochs,
        lr_scheduler_type="cosine",
        warmup_steps=0.05,
        weight_decay=0.01,
        max_grad_norm=1.0,
        seed=seed,
        # emulated bf16 has no memory efficient attention kernel
        bf16=torch.cuda.is_available() and torch.cuda.is_bf16_supported(including_emulation=False),
        fp16=torch.cuda.is_available() and not torch.cuda.is_bf16_supported(including_emulation=False),
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        prediction_loss_only=True,
        save_total_limit=2,
        save_only_model=True,  # the checkpoints only pick the best epoch; optimizer states would double their size
        remove_unused_columns=False,  # the collator walks the grammar over the gold skeleton
        dataloader_num_workers=min(4, os.cpu_count() or 1),
        report_to="tensorboard",
        logging_steps=100,
        ddp_find_unused_parameters=False,
        push_to_hub=config.push_to_hub,
        hub_model_id=config.model_repo_name,
        hub_private_repo=not public,
    )
    trainer = BudgetTrainer(model=model, args=train_args, data_collator=collate, train_dataset=tokenized["train"], eval_dataset=tokenized["validation"])

    start = time.time()
    trainer.train()  # the checkpoints hold no optimizer state, so a run cannot resume from them
    duration = str(timedelta(seconds=time.time() - start))
    if torch.cuda.is_available():
        print(f"peak GPU memory allocated: {torch.cuda.max_memory_allocated() / 2**30:.2f} GiB")

    if int(os.environ.get("LOCAL_RANK", "0")) == 0:
        trainer.save_model(str(model_dir))
        report = exact_match(TransitionPredictor(trainer.model, trainer.model.device), dataset["test"])
        (model_dir / "eval.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        if config.push_to_hub:
            trainer.push_to_hub(commit_message=duration)


@click.command(help="Training script for the transition control flow model given a control flow json.")
@click.argument("json_path", type=str)
@click.option("--seed", default=42, help="Seed of the initialization, dropout and batch order")
@click.option("--public", is_flag=True, default=False, help="Make uploaded HuggingFace repos public (default: private)")
def main(json_path: str, seed: int, public: bool):
    train_transition_model(parse_control_flow_config_json(pathlib.Path(json_path)), public, seed)


if __name__ == "__main__":
    main()
