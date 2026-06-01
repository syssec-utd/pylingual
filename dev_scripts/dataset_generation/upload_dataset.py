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
from .upload_raw_dataset import upload_dataset_to_huggingface
from pylingual.utils.get_logger import get_logger


@click.command(help="Upload a dataset to HuggingFace.")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("upload-dataset")
    dataset_description = get_dataset_description_from_arg_json(json_path, logger)

    logger.info(f"Uploading {dataset_description.name} to HuggingFace...")
    upload_dataset_to_huggingface(dataset_description)


if __name__ == "__main__":
    main()