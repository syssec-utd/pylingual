# /// script
# requires-python = ">= 3.12"
# dependencies = [
#   "pylingual",
# ]
# [tool.uv.sources]
# pylingual = { path = "../../", editable = true }
# ///

import csv
import itertools
import logging
import multiprocessing
import pathlib
import re
import time
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


def retry_on_nas_error(max_retries=3, base_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except OSError as e:
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (2 ** attempt))
                    else:
                        raise
        return wrapper
    return decorator


def create_csv_dataset(code_dataset_path: pathlib.Path, csv_dataset_path: pathlib.Path, data_requests: list[DataRequest], logger: logging.Logger = None):
    progress_bar = tqdm.tqdm(total=sum([request.total_files for request in data_requests]))
    for split in ("train", "test", "valid"):
        if logger:
            logger.info(f"Converting the {split} split to CSV...")
        write_csvs(code_dataset_path / split, csv_dataset_path / split, logger, progress_bar=progress_bar)


def write_csvs(source_path: pathlib.Path, csv_output_path: pathlib.Path, logger: logging.Logger = None, max_csv_rows: int = 30000, progress_bar: tqdm.tqdm = None):
    # validate output directory
    @retry_on_nas_error()
    def ensure_csv_output_dir():
        if csv_output_path.exists():
            if not csv_output_path.is_dir():
                raise OSError("CSV output path is not a directory")
        else:
            csv_output_path.mkdir(parents=True)

    try:
        ensure_csv_output_dir()
    except OSError as error:
        if logger:
            logger.warning(f"Unable to access CSV output directory {csv_output_path}: {error}; skipping split")
        return

    # Resume: scan existing CSV files to find already-processed source paths
    def load_processed_paths() -> set[str]:
        """Read the file column from existing segmentation CSVs to determine which sources are done."""
        processed = set()
        seg_dir = csv_output_path.joinpath("segmentation")
        if not seg_dir.exists():
            return processed
        try:
            csv_files = sorted(seg_dir.glob("segmentation_*.csv"))
        except OSError:
            return processed
        for csv_path in csv_files:
            try:
                with open(csv_path, "r") as f:
                    reader = csv.reader(f)
                    next(reader, None)  # skip header
                    for row in reader:
                        if row:
                            processed.add(row[-1])
            except (OSError, csv.Error, StopIteration):
                continue
        return processed

    processed_paths = load_processed_paths()
    if logger and processed_paths:
        logger.info(f"Resuming: {len(processed_paths)} source files already in existing CSVs")

    def get_start_idx(prefix: str) -> int:
        """Return the next CSV file index after the highest existing one."""
        out_dir = csv_output_path.joinpath(prefix)
        try:
            files = list(out_dir.glob(f"{prefix}_*.csv"))
        except OSError:
            return 0
        if not files:
            return 0
        try:
            return max(int(f.stem.split("_")[-1]) for f in files) + 1
        except (ValueError, IndexError):
            return 0

    ##### csv write wrappers to preserve csv row limit

    def csv_writer(file_prefix: str, csv_header: list, start_idx: int = 0) -> Callable:
        out_dir = csv_output_path.joinpath(file_prefix)

        for csv_idx in itertools.count(start_idx):
            @retry_on_nas_error()
            def ensure_output_dir():
                out_dir.mkdir(exist_ok=True)

            @retry_on_nas_error()
            def open_csv(mode="w"):
                new_path = out_dir.joinpath(f"{file_prefix}_{csv_idx}.csv")
                if mode == "w":
                    new_path.touch()
                return new_path.open(mode=mode)

            def discard_row(_row):
                return None

            try:
                ensure_output_dir()
                csv_file = open_csv()
            except OSError as error:
                if logger:
                    logger.warning(f"Unable to open {file_prefix}_{csv_idx}.csv: {error}; dropping rows")
                for _ in itertools.repeat(None, max_csv_rows):
                    yield discard_row
                continue

            if logger:
                logger.info(f"Creating new csv {csv_file.name}...")
            writer = csv.writer(csv_file)

            def close_csv():
                try:
                    csv_file.close()
                except OSError as error:
                    if logger:
                        logger.warning(f"Unable to close {csv_file.name}: {error}")

            def write_row(row):
                nonlocal csv_file, writer
                for attempt in range(3):
                    try:
                        return writer.writerow(row)
                    except OSError as error:
                        close_csv()
                        if attempt == 2:
                            if logger:
                                logger.warning(f"Unable to write {file_prefix}_{csv_idx}.csv: {error}; dropping row")
                            return None
                        try:
                            time.sleep(2**attempt)
                            csv_file = open_csv(mode="a")
                            writer = csv.writer(csv_file)
                        except OSError:
                            continue

            try:
                write_row(csv_header)
                for _ in itertools.repeat(None, max_csv_rows):
                    yield write_row
            finally:
                close_csv()

    seg_start = get_start_idx("segmentation")
    stmt_start = get_start_idx("statement")
    segmentation_writer = csv_writer("segmentation", CSV_SGMT_HEADER, seg_start)
    statement_writer = csv_writer("statement", CSV_STMT_HEADER, stmt_start)

    # create dirs
    def safe_code_dirs():
        try:
            it = source_path.iterdir()
        except OSError:
            return
        while True:
            try:
                child = next(it)
            except OSError:
                continue
            except StopIteration:
                return
            try:
                if child.is_dir():
                    yield child
            except OSError:
                continue
    code_dirs = safe_code_dirs()

    def bytecode2csv_args():
        while True:
            try:
                try:
                    dir = next(code_dirs)
                except OSError:
                    continue
                except StopIteration:
                    return
                py_path = next(dir.glob("*.py"), None)
                pyc_path = next(dir.glob("*.pyc"), None)
            except OSError:
                continue
            if None in (py_path, pyc_path):
                continue
            if str(py_path) in processed_paths:
                if progress_bar:
                    progress_bar.update()
                continue
            yield (py_path, pyc_path)

    num_fails = 0
    with multiprocessing.Pool(maxtasksperchild=100) as pool:
        iterator = pool.imap_unordered(bytecode2csv_exception_wrapper, bytecode2csv_args())
        while True:
            try:
                result = iterator.next(timeout=300)
            except StopIteration:
                break
            except multiprocessing.TimeoutError:
                num_fails += 1
                if logger:
                    logger.warning(f"Task timed out after 300s (num_fails={num_fails})")
                continue
            if isinstance(result, Exception):
                num_fails += 1
                logger.debug(f"ERR: {result}\nTYPE ERR: {type(result)}\n")
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


def bytecode2csv_exception_wrapper(paths=Tuple[pathlib.Path, pathlib.Path]) -> Tuple[list, list] | Exception:
    try:
        return bytecode2csv(*paths)
    except Exception as error:
        return Exception(f"{type(error)}: {error} in file {paths}")


@retry_on_nas_error()
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
