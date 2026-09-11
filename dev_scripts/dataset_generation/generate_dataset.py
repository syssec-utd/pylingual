# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../", editable = true }
# ///

import click

from .DatasetDescription import get_dataset_description_from_arg_json
from .create_code_dataset import create_code_dataset
from pylingual.utils.get_logger import get_logger


@click.command(help="Generate the code dataset from a dataset description JSON.")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("generate-dataset")
    dataset_description = get_dataset_description_from_arg_json(json_path, logger)

    if dataset_description.code_dir.exists():
        raise FileExistsError(f"{dataset_description.code_dir} already exists! The dataset name is probably already taken.")

    logger.info("Creating code dataset...")
    if not (dataset_description.data_requests and dataset_description.code_dir and dataset_description.version):
        logger.error("Dataset description is missing required fields")
        exit(1)

    create_code_dataset(
        dataset_description.data_requests,
        dataset_description.code_dir,
        dataset_description.version,
        logger,
    )


if __name__ == "__main__":
    main()