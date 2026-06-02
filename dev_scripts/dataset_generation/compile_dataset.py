# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../", editable = true }
# ///

import logging
import multiprocessing
import pathlib
from typing import Optional, Tuple

import click
import tqdm

from .DatasetDescription import get_dataset_description_from_arg_json
from pylingual.utils.generate_bytecode import compile_version
from pylingual.utils.get_logger import get_logger


def compile_file(py_path: pathlib.Path, pyc_path: pathlib.Path, version: Tuple[int, int]) -> Optional[Exception]:
    try:
        compile_version(py_path, pyc_path, version)
    except Exception as err:
        return err
    return None


def star_compile_file(args):
    return compile_file(*args)


@click.command(help="Compile .py files to .pyc bytecode. Only compiles files missing their .pyc counterpart.")
@click.argument("json_path", type=str)
def main(json_path: str):
    logger = get_logger("compile-dataset")
    dataset_description = get_dataset_description_from_arg_json(json_path, logger)

    if not dataset_description.code_dir.exists():
        raise FileNotFoundError(f"{dataset_description.code_dir} does not exist. Run the generate stage first.")

    compile_args = []
    for py_path in dataset_description.code_dir.rglob("*.py"):
        pyc_path = py_path.with_suffix(".pyc")
        if not pyc_path.exists():
            compile_args.append((py_path, pyc_path, dataset_description.version))

    if not compile_args:
        logger.info("All .py files already have corresponding .pyc files. Nothing to compile.")
        return

    logger.info(f"Compiling {len(compile_args)} files...")
    num_fails = 0
    with multiprocessing.Pool() as pool:
        for error in tqdm.tqdm(pool.imap_unordered(star_compile_file, compile_args), total=len(compile_args)):
            if error is not None:
                num_fails += 1
                logger.debug(error)

    logger.info(f"Compilation complete. {num_fails} files failed to compile.")


if __name__ == "__main__":
    main()