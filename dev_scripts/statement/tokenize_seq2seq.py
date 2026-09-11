import os
from typing import Any

import click
import pathlib

from datasets import load_dataset
from transformers import RobertaTokenizer

from StatementConfiguration import StatementConfiguration, parse_statement_config_json

import functools


def preprocess_function(tokenizer: RobertaTokenizer, max_token_length: int, input_key: str, examples: dict[str, Any]) -> dict[str, Any]:
    """Set up Huggingface tokenizers for both inputs and targets"""
    inputs = [ex if ex else "" for ex in examples[input_key]]
    targets = [ex if ex else "" for ex in examples["source"]]

    return tokenizer(text=inputs, text_target=targets, max_length=max_token_length, truncation=True)


def tokenize_seq2seq_dataset(config: StatementConfiguration, public: bool = False):
    # ref: https://huggingface.co/Salesforce/codet5-base
    tokenizer = RobertaTokenizer.from_pretrained(config.tokenizer_repo_name)
    raw_datasets = load_dataset(config.dataset_repo_name, token=True)

    column_names = raw_datasets["train"].column_names
    input_key = "bytecode"
    prepped_preprocess_function = functools.partial(preprocess_function, tokenizer, config.max_token_length, input_key)
    tokenized_datasets = raw_datasets.map(
        prepped_preprocess_function,
        batched=True,
        remove_columns=column_names,
        num_proc=os.cpu_count(),
        desc="Tokenizing datasets",
    )

    tokenized_datasets.push_to_hub(config.tokenized_dataset_repo_name, private=not public)


@click.command(help="Tokenization script for Statement Translation model given a statement json.")
@click.argument("json_path", type=str)
@click.option("--public", is_flag=True, default=False, help="Make uploaded HuggingFace repos public (default: private)")
def main(json_path: str, public: bool):
    json_file_path = pathlib.Path(json_path)
    statement_config = parse_statement_config_json(json_file_path)
    tokenize_seq2seq_dataset(statement_config, public)


if __name__ == "__main__":
    main()
