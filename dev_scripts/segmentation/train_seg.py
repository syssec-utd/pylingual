import logging
import os
import pathlib
import click

import evaluate
import numpy as np
from datasets import ReadInstruction, load_dataset, load_from_disk
from huggingface_hub import hf_hub_download, repo_exists
from SegmentationConfiguration import SegmentationConfiguration, parse_segmentation_config_json
from transformers import AutoModelForTokenClassification, DataCollatorForTokenClassification, PreTrainedTokenizerFast, Trainer, TrainingArguments

# two dictionaries, id2label and label2id, which contain the mappings from ID to label and vice versa.
label_names = ["B", "I", "E"]
id2label = {str(i): label for i, label in enumerate(label_names)}
label2id = {v: k for k, v in id2label.items()}


# compute_metrics: evaluate metric for training and evaluation.
def compute_metrics(eval_preds):
    metric = evaluate.load("seqeval")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)

    # Remove ignored index (special tokens) and convert to labels
    # noqa: E741
    true_labels = [[label_names[l] for l in label if l != -100] for label in labels]
    true_predictions = [[label_names[p] for (p, l) in zip(prediction, label) if l != -100] for prediction, label in zip(predictions, labels)]
    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
    }


def load_tokenizer(tokenizer_json_path: pathlib.Path, tokenizer_repo_name: str, cache_dir: pathlib.Path) -> PreTrainedTokenizerFast:
    if tokenizer_json_path.exists():
        tokenizer_file = str(tokenizer_json_path)
    else:
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


def load_tokenized_train_and_valid_dataset(dataset_repo_name: str, cache_dir: pathlib.Path, dataset_percentage: int = 100, dataset_dir: pathlib.Path | None = None):
    if dataset_dir is not None and dataset_dir.exists():
        tokenized_dataset = load_from_disk(dataset_dir)
        tokenized_train_dataset = tokenized_dataset["train"]
        if dataset_percentage < 100:
            tokenized_train_dataset = tokenized_train_dataset.select(range(len(tokenized_train_dataset) * dataset_percentage // 100))
        return tokenized_train_dataset, tokenized_dataset["valid"]

    dataset_dir = cache_dir / "datasets" / dataset_repo_name
    # Load the tokenized dataset
    tokenized_train_dataset = load_dataset(
        dataset_repo_name,
        token=True,
        cache_dir=str(dataset_dir),
        split=ReadInstruction("train", to=dataset_percentage, unit="%"),
    )

    tokenized_validation_dataset = load_dataset(
        dataset_repo_name,
        token=True,
        cache_dir=str(dataset_dir),
        split="valid",
    )

    return tokenized_train_dataset, tokenized_validation_dataset


def train_segmentation_model(config: SegmentationConfiguration, public: bool = False):
    if repo_exists(config.base_repo_name):
        logging.error(f"{config.base_repo_name} has already exists")
        exit(1)
    # training arguments.
    training_args = TrainingArguments(
        output_dir=str(config.segmenter_dir),
        eval_strategy="epoch",
        logging_strategy="epoch",
        save_strategy="epoch",
        learning_rate=config.segmentation_training_parameters.learning_rate,
        num_train_epochs=config.segmentation_training_parameters.epochs,
        per_device_train_batch_size=config.segmentation_training_parameters.batch_size,
        save_steps=1000,
        weight_decay=0.01,
        fp16=True,
        push_to_hub=False,
        hub_model_id=config.segmenter_repo_name,
        hub_private_repo=not public,
        ddp_backend="nccl",
        ddp_find_unused_parameters=True,
        save_total_limit=5,
    )

    # load a basic pretrained BERT model
    mlm_source = str(config.mlm_dir) if config.mlm_dir.exists() else config.mlm_repo_name
    model = AutoModelForTokenClassification.from_pretrained(
        pretrained_model_name_or_path=mlm_source,
        id2label=id2label,
        label2id=label2id,
        token=True,
    )

    # Set DataCollator for DataCollatorForTokenClassification
    tokenizer = load_tokenizer(config.tokenizer_json_path, config.tokenizer_repo_name, config.cache_dir)
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer, max_length=config.max_token_length)

    (
        tokenized_train_dataset,
        tokenized_validation_dataset,
    ) = load_tokenized_train_and_valid_dataset(
        config.tokenized_dataset_repo_name,
        config.cache_dir,
        config.dataset_percentage,
        config.tokenized_dataset_dir,
    )

    # Hugging face trainer: a Trainer class to fine-tune pretrained models
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_validation_dataset,
        compute_metrics=compute_metrics,
        processing_class=tokenizer,
    )
    
    # Training
    trainer.train()

    if int(os.environ.get("LOCAL_RANK", "0")) == 0:
        # Save the model
        trainer.save_model(str(config.segmenter_dir))

        try:
            trainer.push_to_hub(
                finetuned_from=config.mlm_repo_name,
                dataset=config.tokenized_dataset_repo_name,
                commit_message=f"Trained on {config.tokenized_dataset_repo_name} using {config.mlm_repo_name}",
            )
        except Exception as error:
            logging.warning(
                f"Segmenter saved locally but could not be uploaded to {config.segmenter_repo_name}: {error}"
            )


@click.command(help="Training script for the segmentation model given a segmentation json.")
@click.argument("json_path", type=str)
@click.option("--public", is_flag=True, default=False, help="Make uploaded HuggingFace repos public (default: private)")
def main(json_path: str, public: bool):
    json_file_path = pathlib.Path(json_path)
    segmentation_config = parse_segmentation_config_json(json_file_path)
    train_segmentation_model(segmentation_config, public)


if __name__ == "__main__":
    main()
