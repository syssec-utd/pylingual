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
from .bytecode2cflow import create_cflow_dataset
from pylingual.utils.get_logger import get_logger


@click.command(help="Convert a compiled code dataset to the control flow model dataset (JSONL).")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("generate-cflow")
    dataset_description = get_dataset_description_from_arg_json(json_path, logger)

    logger.info("Converting code dataset to control flow rows...")
    create_cflow_dataset(dataset_description.code_dir, dataset_description.cflow_dir, logger)


if __name__ == "__main__":
    main()
