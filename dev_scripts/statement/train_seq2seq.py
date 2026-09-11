import os
import pathlib
import time
from datetime import timedelta
import click

from datasets import ReadInstruction, load_dataset
from StatementConfiguration import StatementConfiguration, parse_statement_config_json
from transformers import (
    DataCollatorForSeq2Seq,
    RobertaTokenizer,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    T5ForConditionalGeneration,
)


def load_tokenized_train_dataset(dataset_repo_name: str, dataset_percentage: int):
    # Load the tokenized dataset
    tokenized_train_dataset = load_dataset(
        dataset_repo_name,
        token=True,
        split=ReadInstruction("train", to=dataset_percentage, unit="%"),
    )
    return tokenized_train_dataset


def train_statement_model(config: StatementConfiguration, public: bool = False):
    # load model, Salesforce/codet5-base is a pretrained model solving the code generation task.
    tokenizer = RobertaTokenizer.from_pretrained(config.tokenizer_repo_name)
    model = T5ForConditionalGeneration.from_pretrained(config.pretrained_seq2seq_repo_name)
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    model_dir = str(config.statement_model_dir)
    model_repo_name = config.statement_model_repo_name

    train_args = Seq2SeqTrainingArguments(
        output_dir=model_dir,
        learning_rate=config.statement_training_parameters.learning_rate,
        per_device_train_batch_size=config.statement_training_parameters.batch_size,
        per_device_eval_batch_size=config.statement_training_parameters.batch_size,
        weight_decay=0.01,
        fp16=config.fp16,
        logging_dir=str(config.log_dir),
        report_to="tensorboard",
        logging_strategy="steps",
        logging_steps=1000,
        save_strategy="steps",
        save_steps=10000,
        save_total_limit=2,
        num_train_epochs=config.statement_training_parameters.epochs,
        predict_with_generate=True,
        push_to_hub=True,
        hub_model_id=model_repo_name,
        hub_private_repo=not public,
        ddp_backend="nccl",
        ddp_find_unused_parameters=False,
    )

    tokenized_train_dataset = load_tokenized_train_dataset(config.tokenized_dataset_repo_name, config.dataset_percentage)
    trainer = Seq2SeqTrainer(
        model=model,
        args=train_args,
        data_collator=data_collator,
        train_dataset=tokenized_train_dataset,
        processing_class=tokenizer,
    )

    start = time.time()
    trainer.train()
    duration = str(timedelta(seconds=time.time() - start))

    if int(os.environ.get("LOCAL_RANK", "0")) == 0:
        # upload the latest version of the model to the Model Hub on Huggingface
        trainer.save_model(str(config.statement_model_dir))
        # this command returns the URL of the commit it just did
        trainer.push_to_hub(
            commit_message=duration,
            finetuned_from=config.pretrained_seq2seq_repo_name,
            dataset=config.tokenized_dataset_repo_name,
        )


@click.command(help="Training script for the statement translation model given a statement json.")
@click.argument("json_path", type=str)
@click.option("--public", is_flag=True, default=False, help="Make uploaded HuggingFace repos public (default: private)")
def main(json_path: str, public: bool):
    json_file_path = pathlib.Path(json_path)
    statement_config = parse_statement_config_json(json_file_path)
    train_statement_model(statement_config, public)


if __name__ == "__main__":
    main()
