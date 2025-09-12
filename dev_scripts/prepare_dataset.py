# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../" }
# ///

import json
import logging
import pathlib
from typing import Union
import click

from dataset_generation.bytecode2csv import create_csv_dataset
from dataset_generation.create_code_dataset import create_code_dataset
from dataset_generation.DatasetDescription import DataRequest, DatasetDescription
from dataset_generation.upload_raw_dataset import upload_dataset_to_huggingface
from pylingual.utils.get_logger import get_logger


def get_dataset_description_from_arg_json(json_path: str, logger: Union[logging.Logger, None] = None) -> DatasetDescription:
    json_file_path = pathlib.Path(json_path)

    if not json_file_path.exists():
        raise FileNotFoundError(f"{json_file_path} does not exist")

    if logger:
        logger.info(f"Loading dataset description from {json_file_path}...")

    with json_file_path.open() as json_file:
        dataset_description_dict = json.load(json_file)

    dataset_description_dict["data_requests"] = [DataRequest(**d) for d in dataset_description_dict["data_requests"]]
    return DatasetDescription(**dataset_description_dict)


@click.command(help="Samples, splits, processes, and uploads a given dataset described by JSON.")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("prepare-dataset")

    dataset_description = get_dataset_description_from_arg_json(json_path, logger)
    logger.debug(dataset_description)

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

    # create csv dataset
    logger.info("Converting code dataset to csv...")
    create_csv_dataset(
        dataset_description.code_dir,
        dataset_description.csv_dir,
        dataset_description.data_requests,
        logger,
    )

    logger.info(f"Uploading {dataset_description.name} to HuggingFace...")
    upload_dataset_to_huggingface(dataset_description)


if __name__ == "__main__":
    main()
