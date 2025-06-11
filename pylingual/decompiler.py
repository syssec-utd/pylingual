from __future__ import annotations

import datetime
import functools
import importlib.resources
import itertools
import keyword
import logging
import re
import tempfile
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from xdis.magics import magicint2version

from pylingual.control_flow_reconstruction.cflow import bytecode_to_indented_source
from pylingual.control_flow_reconstruction.reconstruct_control_indentation import reconstruct_source
from pylingual.equivalence_check import TestResult, compare_pyc
from pylingual.models import CacheTranslator, load_models
from pylingual.utils.generate_bytecode import CompileError, compile_version
from pylingual.masking.model_disasm import create_global_masker, restore_masked_source_text
from pylingual.editable_bytecode import PYCFile
from pylingual.segmentation.segmentation_search_strategies import get_top_k_predictions, m_deep_top_k, naive_confidence_priority, filter_subwords
from pylingual.segmentation.sliding_window import merge, sliding_window
from pylingual.utils.lists import unflatten
from pylingual.utils.version import PythonVersion
from pylingual.utils.tracked_list import CFLOW_STEP, CORRECTION_STEP, SEGMENTATION_STEP, TrackedList, TrackedDataset

if TYPE_CHECKING:
    import transformers
    from pylingual.editable_bytecode.Instruction import Inst

logger = logging.getLogger(__name__)

bytecode_separator = " <SEP> "
lno_regex = re.compile(r"(?<=line )\d+")
def_regex = re.compile(r"(?<=def ).+?(?=\()")
class_regex = re.compile(r"(?<=class ).+?(?=:|\()")


def has_comp_error(results: list[TestResult]) -> bool:
    return bool(results) and isinstance(results[0], Exception)


@dataclass
class DecompilerResult:
    """
    Dataclass containing relevant results from decompiling a pyc

    :param equivalence_results: list of internal bytecode comparison results
    :param original_pyc: path to original pyc
    :param decompiled_source: path to decompiled source
    :param out_dir: directory where decompiler output and internal steps are written
    :param version: python version of pyc
    """

    equivalence_results: list[TestResult]
    original_pyc: Path
    decompiled_source: Path
    out_dir: Path
    version: PythonVersion

    def calculate_success_rate(self) -> float:
        if not self.equivalence_results:
            return 0
        return sum(1 for x in self.equivalence_results if x.success) / len(self.equivalence_results) * 100


class Decompiler:
    """
    You probably want to use decompile() instead.

    Decompiles a PYC file after masking bytecode, segmenting bytecode, and translating bytecode back into source statements, then reconstructs the control flow.
    Additionally saves the decompiled file into the specified output directory.

    :param pyc: The PYCFile loaded into memory
    :param out_dir: The output directory where decompilation results will be stored
    :param segmenter: The loaded segmentation model
    :param translator: The loaded translation model
    :param version: The python version
    :param top_k: Value of k to use for top k segmentation
    :param trust_lnotab: Decides whether or not to use line number information
    """

    def __init__(self, pyc: PYCFile, out_dir: Path, segmenter: transformers.Pipeline, translator: CacheTranslator, version: PythonVersion, top_k=10, trust_lnotab=False):
        self.pyc = pyc
        self.file = pyc.pyc_path
        self.out_dir = out_dir
        self.segmenter = segmenter
        self.translator = translator
        self.version = version
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.top_k = top_k
        self.highest_k_used = 0

        self.trust_lnotab = trust_lnotab

        self.header = "# Decompiled with PyLingual (https://pylingual.io)\n"
        try:
            self.header += (
                f"# Internal filename: {self.pyc.codeobj.co_filename}\n"
                f"# Bytecode version: {magicint2version[self.pyc.magic]} ({self.pyc.magic})\n"
                f"# Source timestamp: {datetime.datetime.fromtimestamp(self.pyc.timestamp, datetime.UTC).strftime('%Y-%m-%d %H:%M:%S UTC')} ({self.pyc.timestamp})\n\n"
            )
        except:
            pass

        self.decompile()
        self.log_results()

        logger.info(f"Checking decompilation for {self.file.name}...")
        if shutil.which("pyenv") is None and self.version != sys.version_info:
            logger.warning(f"pyenv is not installed so equivalence check cannot be performed. Please install pyenv manually along with the required Python version ({self.version}) or run PyLingual again with the --init-pyenv flag")
            self.result = DecompilerResult([TestResult(False, "Cannot compare equivalence without pyenv installed", bc.name, bc.name) for bc in self.pyc.iter_bytecodes()], self.file, self.candidate_source_path, self.out_dir, self.version)
            return

        self.equivalence_results = self.check_reconstruction()
        self.correct_failures()

        if has_comp_error(self.equivalence_results):
            self.equivalence_results += self.purge_comp_errors()

        equivalence_report = self.out_dir / "equivalence_report.txt"
        equivalence_report.write_text("\n".join(str(r) for r in self.equivalence_results))

        self.result = DecompilerResult(self.equivalence_results, self.file, self.candidate_source_path, self.out_dir, self.version)

    def decompile(self):
        self.mask_bytecode()
        if self.trust_lnotab:
            self.update_segmentation_from_lnotab()
        else:
            self.run_segmentation()
        self.run_translation()
        self.run_cflow_reconstruction()
        self.reconstruct_source()

    def find_comp_error_cause(self, results: list[TestResult]):
        # parse lno from exception
        lno = int(lno_regex.search(str(results[0])).group(0)) - 1
        # adjust for lines added in postprocessing
        lno -= sum(1 for x in (self.header + self.indented_source).split("\n")[: lno + 1] if x.endswith("# postinserted") or not x.strip() or x.strip().startswith("#"))

        # get offending codeobj

        bad_codeobj = self.blame[lno]

        bad_idx = next(i for i, e in enumerate(self.ordered_bytecodes) if e.codeobj == bad_codeobj)
        return bad_idx

    def correct_failures(self):
        changed = False

        try:
            # fix compile errors
            corrected_comp_errors = set()
            while has_comp_error(self.equivalence_results):
                bad_idx = self.find_comp_error_cause(self.equivalence_results)
                # i don't think this will ever happen but better safe than sorry
                if bad_idx in corrected_comp_errors:
                    return
                if not self.correct_segmentation(bad_idx, from_comp_error=True):
                    return
                changed = True
                corrected_comp_errors.add(bad_idx)
            failed = TrackedList(CORRECTION_STEP, [i for i, result in enumerate(self.equivalence_results) if not result.success])
            for i in failed:
                if self.correct_segmentation(i):
                    changed = True
                    continue
                # other fixes...
        except Exception as e:
            e.add_note("From error correction")
            raise
        finally:
            if changed:
                self.log_results()

    # get eq results after replacing all codeobjs with comp errors with pass, preserving nested codeobjs
    def purge_comp_errors(self):
        try:
            equivalence_results = self.equivalence_results

            def replace_line(line):
                line = line.strip()
                x = def_regex.search(line)
                if x is not None:
                    try:
                        x = x.group(0)
                        x = self.global_masker.unmask(x) if x.startswith("<mask_") else x
                        if not x.isidentifier() or keyword.iskeyword(x):
                            x = "_"
                    except:
                        x = "_"
                    return f"def {x}():"
                x = class_regex.search(line)
                if x is not None:
                    try:
                        x = x.group(0)
                        x = self.global_masker.unmask(x) if x.startswith("<mask_") else x
                        if not x.isidentifier() or keyword.iskeyword(x):
                            x = "_"
                    except:
                        x = "_"
                    return f"class {x}:"
                if line.endswith("# inserted"):
                    return "pass  # inserted"
                return "pass"

            purged = []
            while has_comp_error(equivalence_results):
                bad_idx = self.find_comp_error_cause(equivalence_results)
                bad_co = self.ordered_bytecodes[bad_idx].codeobj
                if bad_idx in purged:
                    return []
                purged.append(bad_idx)
                self.cflow_results[bad_co] = [replace_line(x) for x in "\n".join(self.cflow_results[bad_co]).split("\n")]
                self.reconstruct_source()
                equivalence_results = self.check_reconstruction(write_source=True)
            for i in purged:
                r = equivalence_results[i]
                equivalence_results[i] = TestResult(False, "Compilation Error", r.name_a, r.name_b)
            return equivalence_results
        except:
            return []

    def mask_bytecode(self):
        logger.info(f"Masking bytecode for {self.file.name}...")
        try:
            self.global_masker = create_global_masker(self.pyc)
            # create a dict of line num : [bytecodes composing line]
            self.ordered_instructions = [list(itertools.chain.from_iterable(bc.get_lno_insts().values())) for bc in self.pyc.iter_bytecodes()]
            self.ordered_bytecodes = [bc for bc in self.pyc.iter_bytecodes()]
            self.codeobj_instruction_lists = [[self.global_masker.get_model_view(inst) for inst in insts] for insts in self.ordered_instructions]
            self.segmentation_requests = [bytecode_separator.join(self.global_masker.get_model_view(inst) for inst in insts) for insts in self.ordered_instructions]
        except Exception as e:
            e.add_note("From masking bytecode")
            raise

    def run_segmentation(self):
        logger.info(f"Segmenting bytecode for {self.file.name}...")
        try:
            MAX_WINDOW_LENGTH = 512
            STEP_SIZE = 128

            codeobj_list_instructions = (segmentation_request.split(bytecode_separator) for segmentation_request in self.segmentation_requests)
            codeobj_token_list = []

            # make a list of instructions with their token lengths, can be turned into a list comp but readability suffers and complexity is increased
            for codeobj_instructions in codeobj_list_instructions:
                token_list = []
                tokenized_insts = self.segmenter.tokenizer(codeobj_instructions)

                # map token length to instruction
                for i, inst in enumerate(codeobj_instructions):
                    token_list.append([inst, len(tokenized_insts[i])])

                # map to codeobject
                codeobj_token_list.append(token_list)

            window_segmentation_request_iterators = [(codeobj_index, sliding_window(codeobj, MAX_WINDOW_LENGTH, STEP_SIZE)) for codeobj_index, codeobj in enumerate(codeobj_token_list)]
            window_segmentation_requests = (
                ((codeobj_index, window_index), bytecode_separator.join(window[0]), window[1]) for codeobj_index, window_iterator in window_segmentation_request_iterators for window_index, window in enumerate(window_iterator)
            )

            window_coordinates, flat_window_requests, inst_index = zip(*window_segmentation_requests)

            window_segmentation_results = [filter_subwords(segmentation_result) for segmentation_result in self.segmenter(TrackedDataset(SEGMENTATION_STEP, list(flat_window_requests)), batch_size=8)]

            self.segmentation_results = merge(list(window_coordinates), window_segmentation_results, list(inst_index), MAX_WINDOW_LENGTH, STEP_SIZE)  # merge everything

            # force each code object to start with a 'B'

            for codeobj in self.segmentation_results:
                codeobj[0]["entity"] = "B"

            self.update_starts_line()
        except Exception as e:
            e.add_note("From segmentation")
            raise

    def update_segmentation_from_lnotab(self):
        self.segmentation_results = []
        seen_lines = set()
        # create rows for each bytecode
        for bc in self.pyc.iter_bytecodes():
            # attempt to filter lines
            lno_insts = bc.get_lno_insts(previously_seen_lines=seen_lines)
            seen_lines.update(lno_insts.keys())

            # create bytecode segmentation
            boundaries = []
            for bc_line in lno_insts.values():
                if len(bc_line) == 1:
                    bounds = "B"
                elif len(bc_line) >= 2:
                    bounds = "B" + "I" * (len(bc_line) - 2) + "E"
                else:
                    raise ValueError("Unexpected amount of bytecodes segmented into a line")
                boundaries.extend(list(bounds))

            self.segmentation_results.append([{"entity": entity, "score": 1} for entity in boundaries])

        self.update_starts_line()

    def run_translation(self):
        logger.info(f"Translating statements for {self.file.name}...")
        try:
            translation_requests = []
            for instructions, boundary_predictions in zip(self.ordered_instructions, self.segmentation_results):
                translation_requests.append(self.make_translation_request(instructions, boundary_predictions))
            flattened_translation_requests = list(itertools.chain.from_iterable(translation_requests))
            self.translation_results = self.translator(flattened_translation_requests)
            unflatten(self.translation_results, translation_requests)
            self.update_source_lines()
        except Exception as e:
            e.add_note("From translation")
            raise

    def run_cflow_reconstruction(self):
        logger.info(f"Reconstructing control flow for {self.file.name}...")
        try:
            self.cflow_results = {bc.codeobj: bytecode_to_indented_source(bc, self.source_lines) for bc in TrackedDataset(CFLOW_STEP, self.ordered_bytecodes)}
        except Exception as e:
            e.add_note("From control flow reconstruction")
            raise

    # merge sources and unmask source
    def reconstruct_source(self):
        logger.info(f"Reconstructing source for {self.file.name}...")
        # merge sources and postprocess results
        try:
            self.indented_masked_source, self.blame = reconstruct_source(self.pyc, {a: b for a, b in self.cflow_results.items()})
        except Exception as e:
            e.add_note("From control flow reconstruction")
            raise
        # undo the masking
        try:
            self.indented_source = restore_masked_source_text(self.indented_masked_source, self.global_masker, python_version=self.version)
        except Exception as e:
            e.add_note("From unmasking source")
            raise

    # write indented source and pyc
    def log_results(self):
        self.candidate_source_path = self.out_dir / self.file.with_suffix(".py").name
        self.candidate_pyc_path = self.candidate_source_path.with_suffix(".pyc")
        self.candidate_source_path.write_text(self.header + self.indented_source)
        try:
            compile_version(self.candidate_source_path, self.candidate_pyc_path, self.version)
        except Exception:
            pass  # it's ok if the python doesn't compile

    # make a translation request from a segmentation result
    def make_translation_request(self, instructions: list[Inst], boundary_predictions: list[dict]) -> list[str]:
        translation_requests = []
        for inst, boundary_prediction in zip(instructions, boundary_predictions):
            if boundary_prediction["entity"] == "B":
                translation_requests.append(self.global_masker.get_model_view(inst))
            else:
                translation_requests[-1] += bytecode_separator + self.global_masker.get_model_view(inst)
        return translation_requests

    def update_source_lines(self):
        self.source_lines = list(itertools.chain.from_iterable(self.translation_results))
        if self.version == (3, 12):
            self.pyc.fix_while12(self.source_lines)
        elif self.version >= (3, 10):
            self.pyc.fix_while(self.source_lines)

    # compiles and compares result to original pyc
    def check_reconstruction(self, write_source=False) -> list:
        candidate_source_path = self.candidate_source_path
        candidate_pyc_path = self.candidate_pyc_path
        if write_source:
            tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete_on_close=False)
            tmp.write(self.header + self.indented_source)
            candidate_source_path = Path(tmp.name)
            candidate_pyc_path = Path(tmp.name).with_suffix(".pyc")

        # compile source
        try:
            compile_version(candidate_source_path, candidate_pyc_path, self.version)
        except CompileError as e:
            return [e]
        else:
            return compare_pyc(self.file, candidate_pyc_path)

    # try to correct the segmentation of the ith code object
    def correct_segmentation(self, i: int, from_comp_error=False) -> bool:
        if not self.segmentation_results[i]:
            return False
        original_prediction = [r["entity"] for r in self.segmentation_results[i]]
        strategy = functools.partial(m_deep_top_k, priority_function=naive_confidence_priority, m=2, k=self.top_k + 1)
        # skip first prediction since it is the same as original
        for k, prediction in enumerate(get_top_k_predictions(strategy, self.segmentation_results[i])[1:], start=1):
            if prediction[0] != "B":
                continue
            # change segmentation to new prediction
            for r, p in zip(self.segmentation_results[i], prediction):
                r["entity"] = p
            self.update_starts_line()
            # retranslate affected bytecode
            translation_request = self.make_translation_request(self.ordered_instructions[i], self.segmentation_results[i])
            try:
                self.translation_results[i] = self.translator(translation_request)
                self.update_source_lines()
            except Exception as e:
                e.add_note("From translation")
                raise
            # redo cflow of affected bytecode
            try:
                bc = self.ordered_bytecodes[i]
                self.cflow_results[bc.codeobj] = bytecode_to_indented_source(bc, self.source_lines)
            except Exception as e:
                e.add_note("From control flow reconstruction")
                raise
            # check if new reconstruction is correct
            previous_indented_masked_source, previous_blame, previous_indented_source = self.indented_masked_source, self.blame, self.indented_source
            self.reconstruct_source()
            equivalence_results = self.check_reconstruction(write_source=True)
            if from_comp_error:
                if not has_comp_error(equivalence_results) or self.find_comp_error_cause(equivalence_results) != i:
                    self.equivalence_results = equivalence_results
                    self.highest_k_used = max(self.highest_k_used, k)
                    return True
            elif not has_comp_error(equivalence_results) and equivalence_results[i].success:
                self.equivalence_results[i] = equivalence_results[i]
                self.highest_k_used = max(self.highest_k_used, k)
                return True
            # correction failed, roll back changes to internal source code storage
            self.indented_masked_source, self.blame, self.indented_source = previous_indented_masked_source, previous_blame, previous_indented_source
        # revert to original segmentation
        for r, p in zip(self.segmentation_results[i], original_prediction):
            r["entity"] = p
        return False

    # update starts_line of all instructions based on segmentation results
    def update_starts_line(self):
        line = 0
        for instructions, boundary_predictions in zip(self.ordered_instructions, self.segmentation_results):
            for inst, boundary_prediction in zip(instructions, boundary_predictions):
                if boundary_prediction["entity"] == "B":
                    line += 1
                    inst.starts_line = line
                else:
                    inst.starts_line = None


def decompile(file: Path, out_dir: Path, config_file: Path | None = None, version: PythonVersion | tuple[int, int] | str | None = None, top_k: int = 10, trust_lnotab: bool = False) -> DecompilerResult:
    """
    Decompile a PYC file.

    :param file: path to pyc to decompile
    :param out_dir: Path to save decompilation results and steps to. Defaults to ./decompiled_<pyc_name>/
    :param config_file: Path to decompiler_config.yaml to load. recommended None, which loads the default pylingual config.
    :param version: Loads the models corresponding to this python version. if None, automatically detects version based on input PYC file.
    :param top_k: Max number of pyc segmentations to consider.
    :param trust_lnotab: Trust the lnotab in the input PYC for segmentation, recommended False.
    :return: DecompilerResult class including important information about decompilation
    """
    logger.info(f"Loading {file}...")
    pyc = PYCFile(file)

    # try to auto resolve version
    if version is None:
        try:
            pversion = PythonVersion(pyc.version)
            logger.info(f"Detected version as {pversion}")
        except ValueError:
            raise
        except Exception as err:
            raise TypeError("Error automatically parsing version from pyc") from err
    else:
        pversion = PythonVersion(version)

    # try auto load config file from package
    if config_file is None:
        pkg_path = importlib.resources.files("pylingual")
        with importlib.resources.as_file(pkg_path.joinpath("decompiler_config.yaml")) as pylingual_config:
            config_file = Path(pylingual_config)

    # check config exists
    if not config_file.exists():
        raise FileNotFoundError(f"Decompiler config {config_file} not found")

    segmenter, translator = load_models(config_file, pversion)

    logger.info(f"Decompiling pyc {file.resolve()} to {out_dir.resolve()}")
    result = Decompiler(pyc, out_dir, segmenter, translator, pversion, top_k, trust_lnotab).result

    logger.info("Decompilation complete")
    logger.info(f"{round(result.calculate_success_rate(), 2)}% code object success rate")
    logger.info(f"Result saved to {result.decompiled_source.resolve()}")
    return result
