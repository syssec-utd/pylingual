# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../" }
# ///

import ast
import functools
import os
import pathlib
import click

from datasets import load_dataset
from huggingface_hub import hf_hub_download
from SegmentationConfiguration import SegmentationConfiguration, parse_segmentation_config_json
from pylingual.segmentation.sliding_window import sliding_window
from transformers import PreTrainedTokenizerFast

bytecode_separator = " <SEP> "


def load_tokenizer(tokenizer_repo_name: str, cache_dir: pathlib.Path) -> PreTrainedTokenizerFast:
    tokenizer_dir = cache_dir / "tokenizers" / tokenizer_repo_name

    tokenizer_file = hf_hub_download(repo_id=tokenizer_repo_name, filename="tokenizer.json", token=True, cache_dir=str(tokenizer_dir))
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=tokenizer_file,
        unk_token="[UNK]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        sep_token="[SEP]",
        mask_token="[MASK]",
    )

    return tokenizer


# we need to make sure we align all the labels with the proper words.
def align_labels_with_tokens(labels, word_ids):
    label_names = ["B", "I", "E"]
    id2label = {str(i): label for i, label in enumerate(label_names)}
    label2id = {v: k for k, v in id2label.items()}

    new_labels = []
    current_word = None
    for word_id in word_ids:
        if word_id != current_word:
            # Start of a new word!
            current_word = word_id
            label = -100 if word_id is None else int(label2id[labels[word_id]])
            new_labels.append(label)
        elif word_id is None:
            # Special token
            new_labels.append(-100)
        else:
            # Same word as previous token
            label = int(label2id[labels[word_id]])
            new_labels.append(label)
    return new_labels


# the process function used for tokenize the dataset
def tokenize_and_align_labels(tokenizer: PreTrainedTokenizerFast, max_length: int, examples):
    MAX_WINDOW_LENGTH = 512
    STEP_SIZE = 128

    # parse the strings into lists to better work with the bytecode and boundaries
    parsed_bc = [(codeobj.split(" <SEP> "), ast.literal_eval(bounds)) for codeobj, bounds in zip(examples["bytecode"], examples["boundary"])]

    codeobj_tokens = []

    # count the tokens for each bytecode instruction in a codeobj
    for codeobj, bounds in parsed_bc:
        token_list = []

        for bc, bounds in zip(codeobj, bounds):
            token_list.append(((bc, bounds), len(tokenizer(bc)[0])))

        codeobj_tokens.append(token_list)

    windows = [sliding_window(codeobj, MAX_WINDOW_LENGTH, STEP_SIZE) for codeobj in codeobj_tokens]

    # remake examples using our windows
    examples["boundary"] = []
    examples["bytecode"] = []

    # go through each window
    for window in windows:
        for item in window:
            # where we will temporarily store our bytecode and bounds
            bytecode = []
            bounds = []

            for bc in item[0]:
                bytecode.append(bc[0])
                bounds.append(bc[1])

            # append it into examples
            examples["bytecode"].append(bytecode_separator.join(bytecode))
            examples["boundary"].append(str(bounds))

    tokenized_inputs = tokenizer(
        examples["bytecode"],
        truncation=True,
        max_length=max_length,
    )

    all_labels = examples["boundary"]
    new_labels = []
    for i, labels in enumerate(all_labels):
        labels = labels.replace("'", "").strip("][").split(", ")
        word_ids = tokenized_inputs.word_ids(i)
        labels_len = len(labels)
        max_word_id = word_ids[-2]
        # for those data might cause error due to the incorrect tokenization, we fix the data exceed-length issue and
        # leave them here as some noisy data.
        if max_word_id >= labels_len:
            new_labels.append([-100] * max_word_id)
        else:
            new_labels.append(align_labels_with_tokens(labels, word_ids))

    tokenized_inputs["labels"] = new_labels

    return tokenized_inputs


def tokenize_segmentation_dataset(config: SegmentationConfiguration):
    raw_dataset = load_dataset(config.dataset_repo_name, token=True, cache_dir=str(config.dataset_dir))

    tokenizer = load_tokenizer(config.tokenizer_repo_name, config.cache_dir)
    prepped_tokenize_and_align_labels = functools.partial(tokenize_and_align_labels, tokenizer, config.max_token_length)

    # tokenize input dataset
    column_names = raw_dataset["train"].column_names
    tokenized_datasets = raw_dataset.map(
        prepped_tokenize_and_align_labels,
        batched=True,
        remove_columns=column_names,
        num_proc=os.cpu_count(),
        desc="Tokenizing datasets",
    )

    tokenized_datasets.push_to_hub(
        config.tokenized_dataset_repo_name,
        private=True,
    )


@click.command(help="Script to tokenize the segmentation dataset given a segmentation json.")
@click.argument("json_path", type=str)
def main(json_path: str):
    json_file_path = pathlib.Path(json_path)
    segmentation_config = parse_segmentation_config_json(json_file_path)
    tokenize_segmentation_dataset(segmentation_config)


if __name__ == "__main__":
    main()
