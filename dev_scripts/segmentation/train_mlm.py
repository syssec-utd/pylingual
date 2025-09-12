# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../" }
# ///

import logging
import os
import pathlib
import click

from datasets import load_dataset
from huggingface_hub import hf_hub_download, repo_exists
from SegmentationConfiguration import SegmentationConfiguration, parse_segmentation_config_json
from transformers import AutoModelForMaskedLM, DataCollatorForLanguageModeling, PreTrainedTokenizerFast, RobertaConfig, RobertaForMaskedLM, Trainer, TrainingArguments

from pylingual.segmentation.sliding_window import sliding_window

bytecode_separator = " <SEP> "


def load_tokenizer(tokenizer_repo_name: str, cache_dir: pathlib.Path) -> PreTrainedTokenizerFast:
    tokenizer_dir = cache_dir / "tokenizers" / tokenizer_repo_name

    tokenizer_file = hf_hub_download(
        repo_id=tokenizer_repo_name,
        filename="tokenizer.json",
        token=True,
        cache_dir=str(tokenizer_dir),
    )
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=tokenizer_file,
        unk_token="[UNK]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        sep_token="[SEP]",
        mask_token="[MASK]",
    )

    return tokenizer


def load_tokenized_train_dataset(
    dataset_repo_name: str,
    tokenizer: PreTrainedTokenizerFast,
    max_length: int,
    cache_dir: pathlib.Path,
):
    dataset_dir = cache_dir / "datasets" / dataset_repo_name
    raw_dataset = load_dataset(dataset_repo_name, token=True, cache_dir=dataset_dir, split="train")

    # tokenize the input data
    column_names = raw_dataset.column_names

    def tokenize(examples):
        # sliding window compatibility
        MAX_WINDOW_LENGTH = 512
        STEP_SIZE = 128

        # parse the strings into lists to better work with the bytecode and boundaries
        parsed_bc = [codeobj.split(" <SEP> ") for codeobj in examples["bytecode"]]

        codeobj_tokens = []

        # count the tokens for each bytecode instruction in a codeobj
        for codeobj in parsed_bc:
            token_list = []

            for bytecode in codeobj:
                token_list.append((bytecode, len(tokenizer(bytecode)[0])))

            codeobj_tokens.append(token_list)

        windows = [sliding_window(codeobj, MAX_WINDOW_LENGTH, STEP_SIZE) for codeobj in codeobj_tokens]

        # remake examples using our windows
        examples["bytecode"] = []

        # go through each window
        for window in windows:
            for item in window:
                # where we will temporarily store our bytecode and bounds
                bytecode = []

                for bc in item[0]:
                    bytecode.append(bc)

                # append to examples
                examples["bytecode"].append(bytecode_separator.join(bytecode))

        return tokenizer(examples["bytecode"], max_length=max_length, truncation=True)

    tokenized_dataset = raw_dataset.map(
        tokenize,
        batched=True,
        remove_columns=column_names,
        num_proc=os.cpu_count(),
        desc="Tokenizing datasets",
    )

    return tokenized_dataset


def load_pretrained_mlm(
    pretrained_mlm_repo_name: str,
    tokenizer_embedding_length: int,
    cache_dir: pathlib.Path,
) -> AutoModelForMaskedLM:
    # load a basic pretrained BERT model
    pretrained_mlm_dir = cache_dir / "models" / pretrained_mlm_repo_name
    model = AutoModelForMaskedLM.from_pretrained(pretrained_mlm_repo_name, cache_dir=str(pretrained_mlm_dir))

    # resize token embeddings to fit the model
    model.resize_token_embeddings(tokenizer_embedding_length)

    return model


def initialize_untrained_mlm(
    tokenizer_embedding_length: int,
    max_token_length: int,
) -> RobertaForMaskedLM:
    # initialize untrained RoBERTa model
    # most configuration options set to match https://huggingface.co/microsoft/codebert-base/blob/main/config.json for direct comparison
    model_config = RobertaConfig(
        max_position_embeddings=max_token_length,  # INPUT LENGTH LIMIT
        vocab_size=tokenizer_embedding_length,
        layer_norm_eps=1e-05,
        type_vocab_size=1,
    )
    model = RobertaForMaskedLM(model_config)

    return model


def train_mlm(config: SegmentationConfiguration):
    if repo_exists(config.base_repo_name):
        logging.error(f"{config.base_repo_name} has already exists")
        exit(1)

    using_pretrained_model = bool(config.pretrained_mlm_repo_name)
    # train model, for now the configuration comes from a regular T5 translation model.
    training_args = TrainingArguments(
        output_dir=str(config.mlm_dir),
        num_train_epochs=config.mlm_training_parameters.epochs,
        per_device_train_batch_size=config.mlm_training_parameters.batch_size,
        save_steps=1000,
        save_total_limit=5,
        prediction_loss_only=True,
        push_to_hub=True,
        hub_model_id=config.mlm_repo_name,
        hub_private_repo=True,
        ddp_backend="nccl",
        ddp_find_unused_parameters=using_pretrained_model,  # only look for unused parameters in pretrained models
        remove_unused_columns=False,
    )

    tokenizer = load_tokenizer(config.tokenizer_repo_name, config.cache_dir)

    # Set DataCollator for MLM task, set the probability of masking.
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

    if using_pretrained_model:
        pretrained_mlm = load_pretrained_mlm(config.pretrained_mlm_repo_name, len(tokenizer), config.cache_dir)
    else:
        pretrained_mlm = initialize_untrained_mlm(len(tokenizer), config.max_token_length + 2)

    tokenized_training_data = load_tokenized_train_dataset(config.dataset_repo_name, tokenizer, config.max_token_length, config.cache_dir)

    # Hugging face trainer: a Trainer class to fine-tune pretrained models
    trainer = Trainer(
        model=pretrained_mlm,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_training_data,
    )

    # Training
    trainer.train()

    if int(os.environ["LOCAL_RANK"]) == 0:
        # Save the model
        trainer.save_model(config.mlm_dir)

        trainer.push_to_hub(
            finetuned_from=config.pretrained_mlm_repo_name,
            dataset=config.dataset_repo_name,
            commit_message=f"Trained on {config.dataset_repo_name} using {config.tokenizer_repo_name}",
        )


@click.command(help="Training script for the masked language model pretraining for the segmentation model given a segmentation json.")
@click.argument("json_path", type=str)
def main(json_path: str):
    json_file_path = pathlib.Path(json_path)
    segmentation_config = parse_segmentation_config_json(json_file_path)
    train_mlm(segmentation_config)


if __name__ == "__main__":
    main()
