# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../" }
# ///

import csv
import itertools
import logging
import multiprocessing
import pathlib
import re
import signal
from typing import Callable, Tuple

import tqdm
from pylingual.editable_bytecode import PYCFile

from pylingual.masking.ast_masker import DUMMY_DECORATOR
from pylingual.masking.model_disasm import fix_jump_targets
from .DatasetDescription import DataRequest
from pylingual.masking.model_disasm import create_global_masker, mask_source

bytecode_separator = " <SEP> "
source_seperator = " <SEP> "
CSV_SGMT_HEADER = ["source", "bytecode", "boundary", "file"]
CSV_STMT_HEADER = ["source", "bytecode", "file"]


def create_csv_dataset(code_dataset_path: pathlib.Path, csv_dataset_path: pathlib.Path, data_requests: list[DataRequest], logger: logging.Logger = None):
    progress_bar = tqdm.tqdm(total=sum([request.total_files for request in data_requests]))
    for split in ("train", "test", "valid"):
        if logger:
            logger.info(f"Converting the {split} split to CSV...")
        write_csvs(code_dataset_path / split, csv_dataset_path / split, logger, progress_bar=progress_bar)


def write_csvs(source_path: pathlib.Path, csv_output_path: pathlib.Path, logger: logging.Logger = None, max_csv_rows: int = 30000, progress_bar: tqdm.tqdm = None):
    # validate output directory
    if csv_output_path.exists():
        if not csv_output_path.is_dir():
            raise OSError("CSV output path is not a directory")
    else:
        csv_output_path.mkdir(parents=True)

    ##### csv write wrappers to preserve csv row limit

    def csv_writer(file_prefix: str, csv_header: list) -> Callable:
        out_dir = csv_output_path.joinpath(file_prefix)
        out_dir.mkdir(exist_ok=True)

        for csv_idx in itertools.count():
            new_path = out_dir.joinpath(f"{file_prefix}_{csv_idx}.csv")
            new_path.touch()
            if logger:
                logger.info(f"Creating new csv {new_path.resolve()}...")
            with new_path.open(mode="w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(csv_header)
                for writer in itertools.repeat(writer, max_csv_rows):
                    yield writer.writerow

    segmentation_writer = csv_writer("segmentation", CSV_SGMT_HEADER)
    statement_writer = csv_writer("statement", CSV_STMT_HEADER)

    # create dirs
    code_dirs = (child for child in source_path.iterdir() if child.is_dir())

    def bytecode2csv_args():
        for dir in code_dirs:
            py_path = next(dir.glob("*.py"), None)
            pyc_path = next(dir.glob("*.pyc"), None)
            if None in (py_path, pyc_path):
                logging.debug(f"PY or PYC file not found in {dir}")
                continue
            else:
                yield (py_path, pyc_path)

    num_fails = 0
    with multiprocessing.Pool() as pool:
        for result in pool.imap_unordered(bytecode2csv_exception_wrapper, bytecode2csv_args()):
            if isinstance(result, Exception):
                num_fails += 1
                logger.debug(f"DIR: {dir}\nERR: {result}\nTYPE ERR: {type(result)}\n")
                continue

            (segmentation_rows, statement_rows) = result
            for row, writerow in zip(segmentation_rows, segmentation_writer):
                writerow(row)
            for row, writerow in zip(statement_rows, statement_writer):
                writerow(row)

            if progress_bar:
                progress_bar.update()
                progress_bar.set_postfix({"num_fails": num_fails})

    logger.info(f"NUMBER OF FAILS !!! {num_fails}")


def timeout_handler(signum, frame):
    raise TimeoutError()


def bytecode2csv_exception_wrapper(paths=Tuple[pathlib.Path, pathlib.Path]) -> Tuple[list, list] | Exception:
    signal.signal(signal.SIGALRM, timeout_handler)
    try:
        signal.alarm(30)  # set 30 second timeout
        results = bytecode2csv(*paths)
        signal.alarm(0)  # success; disable timer
        return results
    except Exception as error:
        signal.alarm(0)  # disable timer in case another exception triggered the fail
        return Exception(f"{type(error)}: {error} in file {paths}")


def bytecode2csv(py_path: pathlib.Path, pyc_path: pathlib.Path) -> tuple[list, list]:
    """Creates segmentation and statement csv rows for given bytecode and source file"""
    segmentation_rows = []
    statement_rows = []

    pyc = PYCFile(str(pyc_path.resolve()))
    if pyc.version == (3, 10):
        pyc.replace_duplicated_returns10(py_path.read_text().split("\n"))
    elif pyc.version >= (3, 12):
        pyc.replace_duplicated_returns12(py_path.read_text().split("\n"))
    global_masker = create_global_masker(pyc)

    masked_source_text = mask_source(py_path, global_masker, pyc.version)
    masked_source_lines = masked_source_text.split("\n")

    # filter out dummy decorators added in <= 3.7
    dummy_lnos = []
    if pyc.version <= (3, 7):
        # remove dummy decorators from bytecode'
        pyc._patch_dummy_decorator(dummy_decorator_name=DUMMY_DECORATOR)
        try:  # if no functions are in source, then dummy will not exist
            dummy_decorator_line = f"@{global_masker.mask(DUMMY_DECORATOR)}"
        except KeyError:
            dummy_decorator_line = None
        dummy_lnos = [lno + 1 for lno, source in enumerate(masked_source_lines) if source.strip() == dummy_decorator_line]

    seen_lines = set()

    # create rows for each bytecode
    for bc in pyc.iter_bytecodes():
        # we ignore comprehensions, hoisted later
        if bc.is_comprehension:
            continue

        # attempt to filter lines
        lno_insts = bc.get_lno_insts(previously_seen_lines=seen_lines)

        # create line num : model disasm view of insts
        lno_model_view_insts = {lno: [global_masker.get_model_view(inst) for inst in line_insts] for lno, line_insts in lno_insts.items()}
        seen_lines.update(lno_model_view_insts.keys())

        # segment source
        if pyc.version <= (3, 7):
            segmented_source_lines = []
            for line_num in lno_model_view_insts:
                if not line_num:
                    segmented_source_lines.append("")
                elif line_num in dummy_lnos:
                    segmented_source_lines.append(masked_source_lines[line_num].strip())
                else:
                    segmented_source_lines.append(masked_source_lines[line_num - 1].strip())
        else:
            segmented_source_lines = [masked_source_lines[line_num - 1].strip() if line_num else "" for line_num in lno_model_view_insts.keys()]  # -1 to convert from line num to index in array

        model_disasm_text = bytecode_separator.join(val for val in itertools.chain(*lno_model_view_insts.values()))

        if len(segmented_source_lines) != len(lno_model_view_insts):
            raise ValueError("Length mismatch between segmented source and segmented bytecodes")

        # create bytecode segmentation
        boundaries = []
        for bc_line in lno_model_view_insts.values():
            if len(bc_line) == 1:
                bounds = "B"
            elif len(bc_line) >= 2:
                bounds = "B" + "I" * (len(bc_line) - 2) + "E"
            else:
                raise ValueError("Unexpected amount of bytecodes segmented into a line")
            boundaries.extend(list(bounds))

        # append rows
        segmentation_rows.append([source_seperator.join(segmented_source_lines), model_disasm_text, boundaries, str(py_path)])
        for segmented_source, bytecodes in zip(segmented_source_lines, lno_model_view_insts.values()):
            # skip empty lines
            if not segmented_source or segmented_source == "None":
                continue
            # skip fillers
            if segmented_source in ("pass", "...") and ("RETURN_VALUE" in bytecodes or "RETURN_CONST , None" in bytecodes):
                continue
            # skip string-only lines that aren't docstrings
            if (segmented_source.startswith("'") or segmented_source.startswith('"')) and not any("__doc__" in b for b in bytecodes):
                continue
            if segmented_source.startswith("elif "):
                segmented_source = segmented_source[2:]

            joined_bytecode = bytecode_separator.join(bytecodes)

            # DUCT-TAPE; skip samples where model has to guess masks
            source_masks = set(re.findall(r"<mask_\d+>", segmented_source))
            bytecode_masks = set(re.findall(r"<mask_\d+>", joined_bytecode))
            if not source_masks <= bytecode_masks:
                continue

            # normalize source mask order for statements
            # replace mask values to start at 0 and count up
            mask_regex = re.compile(r"(?<=<mask_)\d+(?=>)")
            masks = mask_regex.findall(joined_bytecode)
            mask_order = [x for i, x in enumerate(masks) if masks.index(x) == i]
            normalized_mask_bytecode = mask_regex.sub(lambda x: str(mask_order.index(x.group(0))), joined_bytecode)
            normalized_mask_source = mask_regex.sub(lambda x: str(mask_order.index(x.group(0))), segmented_source)

            # normalize jump targets
            normalized_mask_bytecode = fix_jump_targets(normalized_mask_bytecode)

            statement_rows.append([normalized_mask_source, normalized_mask_bytecode, str(py_path)])

    return (segmentation_rows, statement_rows)
