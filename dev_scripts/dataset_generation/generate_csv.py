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
from .bytecode2csv import create_csv_dataset
from pylingual.utils.get_logger import get_logger


@click.command(help="Convert a code dataset to CSV format.")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("generate-csv")
    dataset_description = get_dataset_description_from_arg_json(json_path, logger)

    logger.info("Converting code dataset to csv...")
    create_csv_dataset(
        dataset_description.code_dir,
        dataset_description.csv_dir,
        dataset_description.data_requests,
        logger,
    )


if __name__ == "__main__":
    main()