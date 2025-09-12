# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../" }
# ///

import itertools
import logging
import multiprocessing
import pathlib
import random
from typing import List, Optional, Set, Tuple

import tqdm

from .DatasetDescription import DataRequest
from pylingual.utils.generate_bytecode import compile_version
from .normalize_source import normalize_source
from pylingual.masking.ast_masker import add_dummy_decorators


def transfer_and_compile_file(
    original_file: pathlib.Path,
    destination_file: pathlib.Path,
    version: Tuple[int, int],
) -> Optional[Exception]:
    # copy over normalized source file
    try:
        normalized_source = normalize_source(original_file.read_text(), version=version, replace_docstrings=True)

        if version[:2] <= (3, 7):
            normalized_source = add_dummy_decorators(normalized_source)
    except Exception as err:
        return err

    destination_file.parent.mkdir(parents=True, exist_ok=True)
    destination_file.write_text(normalized_source)

    # compile the copied file with the given version
    try:
        compile_version(
            destination_file.resolve(),
            destination_file.with_suffix(".pyc").resolve(),
            version,
        )
    except Exception as err:
        return err

    return None


def star_transfer_and_compile_file(args) -> Optional[Exception]:
    return transfer_and_compile_file(*args)


# samples num_files files from the given directory
# expects the directory to have the structure
# source_dir -> identifier -> file.py
def sample_directory_splits(
    data_request: DataRequest,
) -> Tuple[List[pathlib.Path], List[pathlib.Path], List[pathlib.Path]]:
    all_files: Set[pathlib.Path] = set()
    for identifier in data_request.source_path.iterdir():
        source_file = next(identifier.glob("*.py"), None)  # get the first python file from the identifier
        if source_file is not None:
            all_files.add(source_file)

    # sample batches until we have enough files to satisfy the data requests
    # this avoids running expensive tests on unsampled files
    clean_sample: Set[pathlib.Path] = set()
    while len(clean_sample) < data_request.total_files:
        remaining_files = data_request.total_files - len(clean_sample)
        sample_batch = random.sample(list(all_files), k=remaining_files)
        # add the acceptable files to the sample and remove them from the population
        to_add = set(candidate for candidate in sample_batch if candidate is not None)
        clean_sample.update(to_add)
        all_files -= to_add

    full_sample = iter(clean_sample)

    train = list(itertools.islice(full_sample, data_request.num_train))
    test = list(itertools.islice(full_sample, data_request.num_test))
    valid = list(itertools.islice(full_sample, data_request.num_valid))

    return train, test, valid


def prepare_single_directory_transfer_args(data_request: DataRequest, target_dir: pathlib.Path) -> List[Tuple[pathlib.Path, pathlib.Path]]:
    train, test, valid = sample_directory_splits(data_request)

    transfer_args = []
    for split_name, split_files in zip(("train", "test", "valid"), (train, test, valid)):
        for source_file in split_files:
            target_file = target_dir / split_name / f"{data_request.name}-{source_file.parent.name}" / source_file.name
            transfer_args.append((source_file, target_file))

    return transfer_args


# takes a dict of {<source directory>: (num_train, num_test, num_valid)} and a target directory
# makes train, test, and split directories in the target directory with the normalized source files
def create_code_dataset(
    data_requests: List[DataRequest],
    target_dir: pathlib.Path,
    version: Tuple[int, int],
    logger: logging.Logger,
):
    with multiprocessing.Pool() as pool:
        # prepare a list of file transfers to execute
        logger.info(f"Sampling {', '.join(str(req.source_path.resolve()) for req in data_requests)}...")
        transfer_arg_lists = pool.starmap(
            prepare_single_directory_transfer_args,
            zip(data_requests, itertools.repeat(target_dir)),
        )
        # execute the file transfers
        versioned_transfer_arg_lists = [(source_file, target_file, version) for (source_file, target_file) in itertools.chain(*transfer_arg_lists)]
        logger.info(f"Normalizing and Compiling {len(versioned_transfer_arg_lists)} files...")
        for error in tqdm.tqdm(pool.imap_unordered(star_transfer_and_compile_file, versioned_transfer_arg_lists), total=len(versioned_transfer_arg_lists)):
            if error is not None:
                logger.debug(error)
