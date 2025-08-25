from __future__ import annotations

from xdis import Code3

Code3.__eq__ = (
    lambda self, o: isinstance(o, Code3)
    and self.co_argcount == o.co_argcount
    and self.co_nlocals == o.co_nlocals
    and self.co_flags == o.co_flags
    and self.co_code == o.co_code
    and self.co_consts == o.co_consts
    and self.co_names == o.co_names
    and self.co_varnames == o.co_varnames
    and self.co_filename == o.co_filename
    and self.co_name == o.co_name
    and self.co_stacksize == o.co_stacksize
    and self.co_firstlineno == o.co_firstlineno
    and self.co_freevars == o.co_freevars
    and self.co_cellvars == o.co_cellvars
    and self.co_kwonlyargcount == o.co_kwonlyargcount
)
Code3.__hash__ = lambda self: hash(self.co_code)

import datetime
import functools
import importlib.resources
import itertools
import logging
import re
import tempfile
import sys
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from xdis.magics import magicint2version

from pylingual.control_flow_reconstruction.source import SourceContext, SourceLine
from pylingual.control_flow_reconstruction.structure import bc_to_cft
from pylingual.control_flow_reconstruction.cft import MetaTemplate
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


def has_comp_error(results: list[TestResult]) -> bool:
    return bool(results) and isinstance(results[0], Exception)


@dataclass
class DecompilerResult:
    """
    Dataclass containing relevant results from decompiling a pyc

    :param decompiled_source: str containing the decompiler output
    :param equivalence_results: list of internal bytecode comparison results
    :param original_pyc: original pyc
    :param version: python version of pyc
    """

    decompiled_source: str
    equivalence_results: list[TestResult]
    original_pyc: PYCFile
    version: PythonVersion

    def calculate_success_rate(self) -> float:
        if not self.equivalence_results:
            return 0
        return sum(1 for x in self.equivalence_results if x.success) / len(self.equivalence_results)


class Decompiler:
    """
    Decompiles a PYC file after masking bytecode, segmenting bytecode, and translating bytecode back into source statements, then reconstructs the control flow.
    Additionally saves the decompiled file into the specified output directory.

    :param pyc: The PYCFile loaded into memory
    :param segmenter: The loaded segmentation model
    :param translator: The loaded translation model
    :param version: The python version
    :param top_k: Value of k to use for top k segmentation
    :param trust_lnotab: Decides whether or not to use line number information
    """

    def __init__(self, pyc: PYCFile, segmenter: transformers.Pipeline, translator: CacheTranslator, version: PythonVersion, top_k=10, trust_lnotab=False):
        self.pyc = pyc
        self.pyc.copy()
        self.name = pyc.pyc_path.name if pyc.pyc_path is not None else repr(pyc)
        self.segmenter = segmenter
        self.translator = translator
        self.version = version
        self.top_k = top_k
        self.highest_k_used = 0
        self.tmpn = 0
        self.trust_lnotab = trust_lnotab

    def __call__(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.tmp = Path(tmp)

            self.mask_bytecode()
            self.run_segmentation()
            self.run_translation()
            self.unmask_lines()
            self.run_cflow_reconstruction()
            self.reconstruct_source()

            self.equivalence_results = self.check_reconstruction(self.indented_source)
            self.correct_failures()

            if has_comp_error(self.equivalence_results):
                self.equivalence_results += self.purge_comp_errors()

            for tr in self.equivalence_results:
                if tr.bc_a is not None and not tr.success:
                    self.source_context.cfts[tr.bc_a.codeobj].add_header(f"# {tr}", meta=True)

            return DecompilerResult(str(self.source_context), self.equivalence_results, self.pyc, self.version)

    def find_comp_error_cause(self, results: list[TestResult]):
        # parse lno from exception
        lno = lno_regex.search(str(results[0]))
        if lno is None:
            return None
        lno = int(lno.group(0)) - 1
        # get offending codeobj
        bad_codeobj = self.source_context.source_lines()[lno].blame

        bad_idx = next(i for i, e in enumerate(self.ordered_bytecodes) if e.codeobj == bad_codeobj)
        return bad_idx

    def correct_failures(self):
        try:
            # fix compile errors
            corrected_comp_errors = set()
            while has_comp_error(self.equivalence_results):
                bad_idx = self.find_comp_error_cause(self.equivalence_results)
                if bad_idx is None or bad_idx in corrected_comp_errors:
                    return
                if not self.correct_segmentation(bad_idx, from_comp_error=True):
                    return
                corrected_comp_errors.add(bad_idx)
            failed = TrackedList(CORRECTION_STEP, [i for i, result in enumerate(self.equivalence_results) if not result.success])
            for i in failed:
                if self.correct_segmentation(i):
                    continue
                # other fixes...
        except Exception as e:
            e.add_note("From error correction")
            raise

    # get eq results after replacing all codeobjs with comp errors with pass, preserving nested codeobjs
    def purge_comp_errors(self):
        logger.info("Removing compile errors")
        try:
            equivalence_results = self.equivalence_results
            purged = []
            while has_comp_error(equivalence_results):
                bad_idx = self.find_comp_error_cause(equivalence_results)
                if bad_idx is None:
                    logger.info("Could not find line number of error, unable to fix compile errors")
                    self.source_context.purged_cfts = []
                    return []
                bad_bc = self.ordered_bytecodes[bad_idx]
                if bad_idx in purged:
                    logger.info(f"{bad_bc.name} was already purged, unable to fix compile errors")
                    self.source_context.purged_cfts = []
                    return []
                logger.info(f"Purging {bad_bc.name}")
                purged.append(bad_idx)
                self.source_context.purge(bad_bc.codeobj)
                equivalence_results = self.check_reconstruction(str(self.source_context))
            for i in purged:
                r = equivalence_results[i]
                equivalence_results[i] = TestResult(False, "Compilation Error", r.bc_a, r.bc_b)
            self.source_context.purged_cfts = []
            return equivalence_results
        except:
            self.source_context.purged_cfts = []
            return []

    def mask_bytecode(self):
        logger.info(f"Masking bytecode for {self.name}...")
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

    def unmask_lines(self):
        logger.info(f"Unmasking lines for {self.name}...")
        try:
            self.source_lines = restore_masked_source_text(self.source_lines, self.global_masker)
        except Exception as e:
            e.add_note("From masking bytecode")
            raise

    def run_segmentation(self):
        if self.trust_lnotab:
            return self.update_segmentation_from_lnotab()
        logger.info(f"Segmenting bytecode for {self.name}...")
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
        logger.info(f"Translating statements for {self.name}...")
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
        logger.info(f"Reconstructing control flow for {self.name}...")
        try:
            cfts = {bc.codeobj: bc_to_cft(bc, self.source_lines) for bc in TrackedList(CFLOW_STEP, self.ordered_bytecodes)}
            self.source_context = SourceContext(self.pyc, self.source_lines, cfts)
            version = magicint2version.get(self.pyc.magic, "?")
            time = datetime.datetime.fromtimestamp(self.pyc.timestamp, datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
            self.source_context.header_lines = [
                SourceLine("# Decompiled with PyLingual (https://pylingual.io)", 0, self.pyc.codeobj, meta=True),
                SourceLine(f"# Internal filename: {self.pyc.codeobj.co_filename!r}", 0, self.pyc.codeobj, meta=True),
                SourceLine(f"# Bytecode version: {version} ({self.pyc.magic})", 0, self.pyc.codeobj, meta=True),
                SourceLine(f"# Source timestamp: {time} ({self.pyc.timestamp})", 0, self.pyc.codeobj, meta=True),
                SourceLine("", 0, self.pyc.codeobj, meta=True),
            ]
        except Exception as e:
            e.add_note("From control flow reconstruction")
            raise

    # merge sources and unmask source
    def reconstruct_source(self):
        logger.info(f"Reconstructing source for {self.name}...")
        try:
            self.indented_source = str(self.source_context)
        except Exception as e:
            e.add_note("From source reconstruction")
            raise

    # make a translation request from a segmentation result
    def make_translation_request(self, instructions: list[list["Inst"]], boundary_predictions: list[dict]) -> list[str]:
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

    def tmpfile(self):
        self.tmpn += 1
        return self.tmp / str(self.tmpn)

    # compiles and compares result to original pyc
    def check_reconstruction(self, source: str) -> list[TestResult]:
        logger.info(f"Checking decompilation for {self.name}...")
        src = self.tmpfile()
        pyc = self.tmpfile()
        src.write_text(source)
        try:
            compile_version(src, pyc, self.version)
        except CompileError as e:
            return [e]
        else:
            return compare_pyc(self.pyc, pyc)

    # try to correct the segmentation of the ith code object
    def correct_segmentation(self, i: int, from_comp_error=False) -> bool:
        if not self.segmentation_results[i]:
            return False
        if isinstance(self.source_context.cfts[self.ordered_bytecodes[i].codeobj], MetaTemplate):
            return False
        logger.info(f"Trying to fix segmentation for {self.ordered_bytecodes[i].name}")
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
            previous_lines, previous_indented_source = self.source_lines, self.indented_source
            try:
                self.translation_results[i] = self.translator(translation_request)
                self.update_source_lines()
                self.unmask_lines()
            except Exception as e:
                e.add_note("From translation")
                raise
            self.source_context.update_lines(self.source_lines)
            # check if new reconstruction is correct
            self.reconstruct_source()
            equivalence_results = self.check_reconstruction(self.indented_source)
            if from_comp_error:
                if not has_comp_error(equivalence_results) or self.find_comp_error_cause(equivalence_results) not in [None, i]:
                    self.equivalence_results = equivalence_results
                    self.highest_k_used = max(self.highest_k_used, k)
                    logger.info(f"Updated segmentation for {self.ordered_bytecodes[i].name}")
                    return True
            elif not has_comp_error(equivalence_results) and equivalence_results[i].success:
                self.equivalence_results[i] = equivalence_results[i]
                self.highest_k_used = max(self.highest_k_used, k)
                logger.info(f"Updated segmentation for {self.ordered_bytecodes[i].name}")
                return True
            # correction failed, roll back changes to internal source code storage
            self.indented_source = previous_indented_source
            self.source_lines = previous_lines
            self.source_context.update_lines(previous_lines)
        # revert to original segmentation
        for r, p in zip(self.segmentation_results[i], original_prediction):
            r["entity"] = p
        self.update_starts_line()
        logger.info(f"Could not fix segmentation for {self.ordered_bytecodes[i].name}")
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


def decompile(pyc: PYCFile | Path, save_to: Path | None = None, config_file: Path | None = None, version: str | None = None, top_k: int = 10, trust_lnotab: bool = False) -> DecompilerResult:
    """
    Decompile a PYC file.

    :param pyc: PYCFile or Path to decompile.
    :param save_to: Path to save decompilation results to or None.
    :param config_file: Path to decompiler_config.yaml to load. Use None to load the default PyLingual config (recommended).
    :param version: Loads the models corresponding to this python version. if None, automatically detects version based on input PYC file.
    :param top_k: Max number of pyc segmentations to consider.
    :param trust_lnotab: Trust the lnotab in the input PYC for segmentation (False recommended).
    :return: DecompilerResult class including important information about decompilation
    """
    logger.info(f"Loading {pyc}...")
    if isinstance(pyc, Path):
        pyc = PYCFile(pyc)

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

    if save_to:
        logger.info(f"Decompiling pyc {pyc.pyc_path.resolve() if pyc.pyc_path else repr(pyc)} to {save_to.resolve()}")
    else:
        logger.info(f"Decompiling pyc {pyc.pyc_path.resolve() if pyc.pyc_path else repr(pyc)}")
    decompiler = Decompiler(pyc, segmenter, translator, pversion, top_k, trust_lnotab)
    result = decompiler()

    logger.info("Decompilation complete")
    logger.info(f"{result.calculate_success_rate():.2%} code object success rate")
    if save_to:
        save_to.write_text(result.decompiled_source)
        logger.info(f"Result saved to {save_to}")
    return result
