import logging
import pathlib
import click

from datasets import ReadInstruction, load_dataset
from huggingface_hub import HfApi, create_repo, repo_exists
from SegmentationConfiguration import SegmentationConfiguration, parse_segmentation_config_json
from tokenizers import Tokenizer, decoders, models, normalizers, pre_tokenizers, processors, trainers

special_tokens = ["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"]


def get_untrained_tokenizer() -> Tokenizer:
    # WordPiece tokenization for BERT.
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))

    # The normalizer recognizes the accented characters and strip them out.
    tokenizer.normalizer = normalizers.Sequence([normalizers.NFD(), normalizers.StripAccents()])

    # The pre-tokenizer splits on <SEP> tokens.
    tokenizer.pre_tokenizer = pre_tokenizers.Split("<SEP>", "removed")

    return tokenizer


def post_training_configuration(tokenizer: Tokenizer):
    cls_token_id = tokenizer.token_to_id("[CLS]")
    sep_token_id = tokenizer.token_to_id("[SEP]")

    # Set decoder for the tokenizer
    tokenizer.decoder = decoders.WordPiece(prefix="##")

    # For the TemplateProcessor, we have to specify how to treat a single sentence and a pair of sentences.
    tokenizer.post_processor = processors.TemplateProcessing(
        single="[CLS]:0 $A:0 [SEP]:0",
        pair="[CLS]:0 $A:0 [SEP]:0 $B:1 [SEP]:1",
        special_tokens=[("[CLS]", cls_token_id), ("[SEP]", sep_token_id)],
    )


def save_and_upload_tokenizer(
    tokenizer: Tokenizer,
    tokenizer_json_path: pathlib.Path,
    tokenizer_repo_name: str,
    dataset_name: str,
    public: bool = False,
):
    tokenizer_json_path.parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(tokenizer_json_path.resolve()))

    api = HfApi()
    create_repo(tokenizer_repo_name, exist_ok=True, private=not public)
    api.upload_file(
        path_in_repo="tokenizer.json",
        path_or_fileobj=str(tokenizer_json_path.resolve()),
        repo_id=tokenizer_repo_name,
        commit_message=f"Trained tokenizer using {dataset_name}",
    )


def train_tokenizer(config: SegmentationConfiguration, public: bool = False):
    if repo_exists(config.base_repo_name):
        logging.error(f"{config.base_repo_name} has already exists")
        exit(1)

    tokenizer = get_untrained_tokenizer()

    train_dataset = load_dataset(
        config.dataset_repo_name,
        token=True,
        split=ReadInstruction("train", to=config.dataset_percentage, unit="%"),
    )["bytecode"]
    trainer = trainers.WordPieceTrainer(vocab_size=30000, special_tokens=special_tokens)
    tokenizer.train_from_iterator(train_dataset, trainer=trainer)

    post_training_configuration(tokenizer)

    save_and_upload_tokenizer(
        tokenizer,
        config.tokenizer_json_path,
        config.tokenizer_repo_name,
        config.dataset_repo_name,
        public,
    )


@click.command(help="Training script for the bytecode tokenizer for the segmentation model given a segmentation json.")
@click.argument("json_path", type=str)
@click.option("--public", is_flag=True, default=False, help="Make uploaded HuggingFace repos public (default: private)")
def main(json_path: str, public: bool):
    json_file_path = pathlib.Path(json_path)
    segmentation_config = parse_segmentation_config_json(json_file_path)
    train_tokenizer(segmentation_config, public)


if __name__ == "__main__":
    main()
