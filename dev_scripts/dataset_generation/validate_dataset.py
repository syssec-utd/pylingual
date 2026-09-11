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
from pylingual.utils.get_logger import get_logger


@click.command(help="Validate that a dataset's CSV files are complete.")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("validate-dataset")
    dataset_description = get_dataset_description_from_arg_json(json_path, logger)

    missing = []
    for split in ("train", "test", "valid"):
        for kind in ("segmentation", "statement"):
            csv_dir = dataset_description.csv_dir / split / kind
            csv_files = list(csv_dir.glob("*.csv")) if csv_dir.exists() else []
            if not csv_files:
                missing.append(f"{split}/{kind}")

    if missing:
        logger.error("Missing CSV files for the following split/type combinations:")
        for entry in missing:
            logger.error(f"  {entry}")
        exit(1)

    logger.info("All splits validated successfully.")


if __name__ == "__main__":
    main()