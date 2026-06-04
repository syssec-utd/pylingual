# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../", editable = true }
# ///

import click

from dataset_generation.generate_dataset import main as generate_dataset
from dataset_generation.compile_dataset import main as compile_dataset
from dataset_generation.generate_csv import main as generate_csv
from dataset_generation.validate_dataset import main as validate_dataset
from dataset_generation.upload_dataset import main as upload_dataset
from pylingual.utils.get_logger import get_logger

STAGES = ["generate", "compile", "csv", "validate", "upload"]


@click.command(
    help="Run the dataset preparation pipeline. By default all stages run in order. "
    "Use --stage to run specific stages (e.g. --stage csv --stage upload)."
)
@click.argument("json_path", type=str)
@click.option(
    "--stage",
    multiple=True,
    type=click.Choice(STAGES),
    help="Stage(s) to run. May be specified multiple times. Defaults to all stages.",
)
@click.option("--public", is_flag=True, default=False, help="Upload as a public dataset instead of private.")
def main(json_path: str, stage: tuple[str, ...], public: bool):
    logger = get_logger("prepare-dataset")

    stages_to_run = list(stage) if stage else STAGES

    for s in stages_to_run:
        logger.info(f"Running stage: {s}")
        if s == "generate":
            generate_dataset([json_path], standalone_mode=False)
        elif s == "compile":
            compile_dataset([json_path], standalone_mode=False)
        elif s == "csv":
            generate_csv([json_path], standalone_mode=False)
        elif s == "validate":
            validate_dataset([json_path], standalone_mode=False)
        elif s == "upload":
            upload_dataset(["--public" if public else "", json_path], standalone_mode=False)


if __name__ == "__main__":
    main()