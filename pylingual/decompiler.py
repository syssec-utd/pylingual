from __future__ import annotations

from xdis import Code3

Code3.__eq__ = lambda self, o: (
    isinstance(o, Code3)
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
Code3.__hash__ = lambda self: hash((self.co_code, self.co_name, self.co_firstlineno))

import datetime
import functools
import importlib.resources
import io
import itertools
import logging
import re
import tempfile
import sys
import shutil
import time
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from xdis.magics import magicint2version

from pylingual.control_flow_reconstruction.model_view import CflowRequest, cflow_request
from pylingual.control_flow_reconstruction.source import SourceContext, SourceLine
from pylingual.control_flow_reconstruction.skeleton_template import SkeletonTemplate
from pylingual.equivalence_check import PatchedPYC, TestResult, compare_pyc
from pylingual.models import CacheTranslator, load_models
from pylingual.utils.generate_bytecode import CompileError, PyenvError, compile_version
from pylingual.masking.model_disasm import create_global_masker, restore_masked_source_text
from pylingual.preprocessor import Preprocessor
from pylingual.editable_bytecode import PYCFile
from pylingual.segmentation.segmentation_search_strategies import get_top_k_predictions, m_deep_top_k, naive_confidence_priority, filter_subwords
from pylingual.segmentation.sliding_window import merge, sliding_window
from pylingual.utils.lists import unflatten
from pylingual.utils.version import PythonVersion
from pylingual.utils.tracked_list import CFLOW_STEP, CORRECTION_STEP, SEGMENTATION_STEP, TrackedList, TrackedDataset

if TYPE_CHECKING:
    import transformers
    from pylingual.editable_bytecode.Instruction import Inst
    from pylingual.models import ControlFlowPredictor

logger = logging.getLogger(__name__)

bytecode_separator = " <SEP> "
lno_regex = re.compile(r"(?<=line )\d+")
# control flow model candidates tried for a failing code object; each one costs a recompile. Files equivalent level off
# at 16 to 20, and up to 32 the decompiler stays faster than the control flow templates were, on an RTX 2080 or 4090
CFLOW_BEAMS = 16


def has_comp_error(results: list[TestResult]) -> bool:
    return bool(results) and isinstance(results[0], Exception)


# an unclosed bracket makes python report the next statement, so find the line that opened it
def unclosed_bracket_line(source: str, lno: int) -> int | None:
    stack = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.start[0] >= lno:
                break
            if tok.type == tokenize.OP and tok.string in "([{":
                stack.append(tok.start[0])
            elif tok.type == tokenize.OP and tok.string in ")]}" and stack:
                stack.pop()
    except (tokenize.TokenError, SyntaxError):
        pass
    return stack[0] if stack else None


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
    :param cflow_model: The loaded control flow model
    """

    def __init__(self, pyc: PYCFile, segmenter: transformers.Pipeline, translator: CacheTranslator, version: PythonVersion, top_k=10, trust_lnotab=False, timeout=None, *, cflow_model: ControlFlowPredictor):
        if cflow_model is None:
            raise ValueError("control flow reconstruction needs a control flow model")
        self.pyc = pyc
        self.name = pyc.pyc_path.name if pyc.pyc_path is not None else repr(pyc)
        self.segmenter = segmenter
        self.translator = translator
        self.version = version
        self.top_k = top_k
        self.highest_k_used = 0
        self.tmpn = 0
        self.trust_lnotab = trust_lnotab
        self.timeout = timeout
        self.cflow_model = cflow_model
        self.cflow_requests = []
        self.cflow_results = []
        # code object index -> (its request, the candidates for it), predicted in one batch for every failing code object
        self.beam_cache: dict[int, tuple[CflowRequest, list[list[str]] | None]] = {}
        self.start_time = time.time()
        self.unmask_cache = {}
        self.unmask_cache_size = None

    def check_timeout(self):
        if self.timeout is not None and time.time() - self.start_time > self.timeout:
            raise TimeoutError(f"Decompilation of {self.name} timed out after {self.timeout} seconds")

    def __call__(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.tmp = Path(tmp)

            self.preprocess_bytecode()
            self.check_timeout()
            self.mask_bytecode()
            self.check_timeout()
            self.run_segmentation()
            self.check_timeout()
            self.run_translation()
            self.check_timeout()
            self.unmask_lines()
            self.check_timeout()
            self.run_cflow_prediction()
            self.check_timeout()
            self.run_cflow_reconstruction()
            self.check_timeout()
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
        lno = int(lno.group(0))
        lno = unclosed_bracket_line(str(self.source_context), lno) or lno
        # get offending codeobj, counting physical lines since unmasked strings can span several
        source_lines = self.source_context.source_lines()
        ends = itertools.accumulate(x.line.count("\n") + 1 for x in source_lines)
        bad_codeobj = source_lines[next((i for i, end in enumerate(ends) if end >= lno), len(source_lines) - 1)].blame

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
                if not (self.correct_cflow(bad_idx, from_comp_error=True) or self.correct_segmentation(bad_idx, from_comp_error=True)):
                    return
                corrected_comp_errors.add(bad_idx)
            failed = [i for i in range(len(self.ordered_bytecodes)) if (result := self.result_for_bytecode(i, self.equivalence_results)) is not None and not result.success]
            self.prefetch_beams(failed)
            for i in TrackedList(CORRECTION_STEP, failed):
                if self.correct_cflow(i) or self.correct_segmentation(i):
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
            recovered = set()
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
                # once other code objects are purged, a wrong skeleton can be the only error left
                if purged and bad_idx not in recovered:
                    recovered.add(bad_idx)
                    if self.correct_cflow(bad_idx, from_comp_error=True):
                        equivalence_results = self.equivalence_results
                        continue
                logger.info(f"Purging {bad_bc.name}")
                purged.append(bad_idx)
                self.source_context.purge(bad_bc.codeobj)
                equivalence_results = self.check_reconstruction(str(self.source_context))
            for i in purged:
                r = self.result_for_bytecode(i, equivalence_results)
                if r is not None:
                    equivalence_results[equivalence_results.index(r)] = TestResult(False, "Compilation Error", r.bc_a, r.bc_b)
            self.source_context.purged_cfts = []
            return equivalence_results
        except TimeoutError:
            self.source_context.purged_cfts = []
            raise
        except:
            self.source_context.purged_cfts = []
            return []

    def preprocess_bytecode(self):
        logger.info(f"Preprocessing bytecode for {self.name}...")
        try:
            Preprocessor().preprocess(self.pyc)
        except Exception as e:
            logger.warning(f"Preprocessing failed for {self.name}, continuing without container recovery: {e}")

    def mask_bytecode(self):
        logger.info(f"Masking bytecode for {self.name}...")
        try:
            self.global_masker = create_global_masker(self.pyc)
            # create a dict of line num : [bytecodes composing line]
            self.ordered_instructions = [list(itertools.chain.from_iterable(bc.get_lno_insts().values())) for bc in self.pyc.iter_bytecodes()]
            self.ordered_bytecodes = [bc for bc in self.pyc.iter_bytecodes()]
            self.codeobj_instruction_lists = [[self.global_masker.get_model_view(inst) for inst in insts] for insts in self.ordered_instructions]
            self.segmentation_requests = [bytecode_separator.join(views) for views in self.codeobj_instruction_lists]
        except Exception as e:
            e.add_note("From masking bytecode")
            raise

    def unmask_lines(self):
        logger.info(f"Unmasking lines for {self.name}...")
        try:
            # lines are unmasked independently, so lines of unchanged code objects are only unmasked once
            if self.unmask_cache_size != len(self.global_masker.global_tab):
                self.unmask_cache = {}
                self.unmask_cache_size = len(self.global_masker.global_tab)
            new_lines = [line for line in dict.fromkeys(self.source_lines) if line not in self.unmask_cache]
            self.unmask_cache.update(zip(new_lines, restore_masked_source_text(new_lines, self.global_masker)))
            self.source_lines = [self.unmask_cache[line] for line in self.source_lines]
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

            window_segmentation_results = [filter_subwords(segmentation_result) for segmentation_result in self.segmenter(TrackedDataset(SEGMENTATION_STEP, list(flat_window_requests), check_timeout=self.check_timeout), batch_size=8)]

            self.segmentation_results = merge(list(window_coordinates), window_segmentation_results, list(inst_index), MAX_WINDOW_LENGTH, STEP_SIZE)  # merge everything

            # force each code object to start with a 'B'

            for codeobj in self.segmentation_results:
                if codeobj:  # hoisted comprehensions have no instructions of their own
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
            for model_views, boundary_predictions in zip(self.codeobj_instruction_lists, self.segmentation_results):
                translation_requests.append(self.make_translation_request(model_views, boundary_predictions))
            flattened_translation_requests = list(itertools.chain.from_iterable(translation_requests))
            self.translation_results = self.translator(flattened_translation_requests, check_timeout=self.check_timeout)
            unflatten(self.translation_results, translation_requests)
            self.update_source_lines()
        except Exception as e:
            e.add_note("From translation")
            raise

    def run_cflow_prediction(self):
        logger.info(f"Predicting control flow for {self.name}...")
        try:
            self.cflow_requests = [cflow_request(bc, self.source_lines) for bc in self.ordered_bytecodes]
            self.cflow_results = self.predict_skeletons(self.cflow_requests)
        except Exception as e:
            e.add_note("From control flow prediction")
            raise

    def run_cflow_reconstruction(self):
        logger.info(f"Reconstructing control flow for {self.name}...")
        try:
            cfts = {self.ordered_bytecodes[i].codeobj: self.make_cft(i) for i in TrackedList(CFLOW_STEP, list(range(len(self.ordered_bytecodes))), check_timeout=self.check_timeout)}
            self.source_context = SourceContext(self.pyc, self.source_lines, cfts)
            version = magicint2version.get(self.pyc.magic, "?")
            time = datetime.datetime.fromtimestamp(self.pyc.timestamp, datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC") if self.pyc.timestamp is not None else "unknown"
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
    def make_translation_request(self, model_views: list[str], boundary_predictions: list[dict]) -> list[str]:
        translation_requests = []
        for model_view, boundary_prediction in zip(model_views, boundary_predictions):
            if boundary_prediction["entity"] == "B":
                translation_requests.append(model_view)
            else:
                translation_requests[-1] += bytecode_separator + model_view
        return translation_requests

    # candidate skeletons for each request, None where there is no request
    def predict_skeletons(self, requests: list[CflowRequest | None], num_beams=1) -> list[list[list[str]] | None]:
        return self.cflow_model(requests, num_beams=num_beams, check_timeout=self.check_timeout)

    # the model's candidates for the failing code objects, in one batch rather than one call each in correct_cflow
    def prefetch_beams(self, indices: list[int]):
        todo = [i for i in indices if self.cflow_requests[i] is not None]
        if todo:
            for i, skeletons in zip(todo, self.predict_skeletons([self.cflow_requests[i] for i in todo], num_beams=CFLOW_BEAMS)):
                self.beam_cache[i] = (self.cflow_requests[i], skeletons)

    # the model's candidates for the ith code object's current request
    def beams(self, i: int) -> list[list[str]] | None:
        request = self.cflow_requests[i]
        cached = self.beam_cache.get(i)
        if cached is not None and cached[0] is request:
            return cached[1]
        return self.predict_skeletons([request], num_beams=CFLOW_BEAMS)[0]

    # the model's best skeleton for the ith code object
    def make_cft(self, i: int) -> SkeletonTemplate:
        skeletons = self.cflow_results[i]
        return SkeletonTemplate.for_request(self.ordered_bytecodes[i], self.cflow_requests[i], skeletons[0] if skeletons else None)

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
        src.write_text(source, encoding="utf-8")
        try:
            compile_version(src, pyc, self.version)
        except CompileError as e:
            return [e]
        except PyenvError as e:
            logger.error(f"Could not check decompilation due to pyenv error: {e}")
            return []
        else:
            return compare_pyc(self.patched_pyc, pyc)

    # the original pyc only needs to be patched once, it is compared after every candidate fix
    @functools.cached_property
    def patched_pyc(self) -> PatchedPYC:
        return PatchedPYC(self.pyc)

    def result_for_bytecode(self, i: int, results: list[TestResult]) -> TestResult | None:
        codeobj = self.ordered_bytecodes[i].codeobj
        return next((r for r in results if isinstance(r, TestResult) and r.bc_a is not None and r.bc_a.codeobj == codeobj), None)

    def passing_bytecodes(self) -> list[int]:
        return [j for j in range(len(self.ordered_bytecodes)) if (r := self.result_for_bytecode(j, self.equivalence_results)) is not None and r.success]

    # whether results fix the ith code object without breaking a passing one
    def accepts(self, i: int, results: list[TestResult], passing: list[int], from_comp_error: bool) -> bool:
        if from_comp_error:
            improved = bool(results) and (not has_comp_error(results) or self.find_comp_error_cause(results) not in [None, i])
        else:
            improved = not has_comp_error(results) and (r := self.result_for_bytecode(i, results)) is not None and r.success
        return improved and all((r := self.result_for_bytecode(j, results)) is not None and r.success for j in passing)

    # try the control flow model's other candidates for the ith code object; if none passes, the best one stays, since
    # it fits the block grammar, and correct_segmentation tries other segmentations, asking the model again for each
    def correct_cflow(self, i: int, from_comp_error=False) -> bool:
        bc = self.ordered_bytecodes[i]
        original = self.source_context.cfts[bc.codeobj]
        if self.cflow_requests[i] is None:
            return False
        logger.info(f"Trying to fix control flow for {bc.name}")
        passing = self.passing_bytecodes()
        previous_indented_source = self.indented_source
        accepted = False
        try:
            # beam search only runs for code objects that fail
            beams = [tokens for tokens in self.beams(i) or [] if tokens != original.tokens]
            for tokens in beams:
                self.source_context.update_cft(bc, SkeletonTemplate(bc, original.stmts, tokens))
                self.reconstruct_source()
                equivalence_results = self.check_reconstruction(self.indented_source)
                if accepted := self.accepts(i, equivalence_results, passing, from_comp_error):
                    self.equivalence_results = equivalence_results
                    logger.info(f"Updated control flow for {bc.name}")
                    return True
            logger.info(f"Could not fix control flow for {bc.name}")
            return False
        except Exception as e:
            e.add_note("From control flow correction")
            raise
        finally:
            if not accepted:
                self.source_context.update_cft(bc, original)
                self.indented_source = previous_indented_source

    # try to correct the segmentation of the ith code object
    def correct_segmentation(self, i: int, from_comp_error=False) -> bool:
        if len(self.segmentation_results) <= i or not self.segmentation_results[i]:
            return False
        logger.info(f"Trying to fix segmentation for {self.ordered_bytecodes[i].name}")
        original_prediction = [r["entity"] for r in self.segmentation_results[i]]
        original_translation = self.translation_results[i]
        previous_request, previous_result = self.cflow_requests[i], self.cflow_results[i]
        previous_lines, previous_indented_source = self.source_lines, self.indented_source
        previous_context = self.source_context.snapshot()
        previous_starts = [(inst, inst.starts_line) for insts in self.ordered_instructions for inst in insts]
        passing = self.passing_bytecodes()
        strategy = functools.partial(m_deep_top_k, priority_function=naive_confidence_priority, m=2, k=self.top_k + 1)
        # skip first prediction since it is the same as original
        candidates = [(k, prediction) for k, prediction in enumerate(get_top_k_predictions(strategy, self.segmentation_results[i])[1:], start=1) if prediction[0] == "B"]
        bc = self.ordered_bytecodes[i]

        def apply(prediction, translation=None):
            # All source representations and instruction line numbers belong
            # to the same candidate. Keep them together until it is checked.
            for r, p in zip(self.segmentation_results[i], prediction):
                r["entity"] = p
            self.update_starts_line()
            if translation is not None:
                self.translation_results[i] = translation
                self.update_source_lines()
                self.unmask_lines()

        def restore():
            for r, p in zip(self.segmentation_results[i], original_prediction):
                r["entity"] = p
            for inst, starts_line in previous_starts:
                inst.starts_line = starts_line
            self.translation_results[i] = original_translation
            self.cflow_requests[i], self.cflow_results[i] = previous_request, previous_result
            self.source_lines = previous_lines
            self.indented_source = previous_indented_source
            self.source_context.restore(previous_context)

        # translate and predict every candidate in one batch each, then check them in order as before
        try:
            translation_requests = []
            for _, prediction in candidates:
                apply(prediction)
                translation_requests.append(self.make_translation_request(self.codeobj_instruction_lists[i], self.segmentation_results[i]))
            try:
                flat = self.translator(list(itertools.chain.from_iterable(translation_requests)), check_timeout=self.check_timeout) if translation_requests else []
            except Exception as e:
                e.add_note("From translation")
                raise
            translations = []
            for request in translation_requests:
                translations.append(flat[: len(request)])
                flat = flat[len(request) :]
            requests = []
            for (_, prediction), translation in zip(candidates, translations):
                apply(prediction, translation)
                # skeletons refer to the old statements, so predict again
                requests.append(cflow_request(bc, self.source_lines))
            skeletons = self.predict_skeletons(requests) if requests else []
        finally:
            restore()

        for (k, prediction), translation, request, skeleton in zip(candidates, translations, requests, skeletons):
            accepted = False
            try:
                try:
                    apply(prediction, translation)
                except Exception as e:
                    e.add_note("From translation")
                    raise
                self.source_context.update_lines(self.source_lines)
                self.cflow_requests[i], self.cflow_results[i] = request, skeleton
                self.source_context.update_cft(bc, self.make_cft(i))
                self.reconstruct_source()
                equivalence_results = self.check_reconstruction(self.indented_source)
                accepted = self.accepts(i, equivalence_results, passing, from_comp_error)
                if accepted:
                    self.equivalence_results = equivalence_results
                    self.highest_k_used = max(self.highest_k_used, k)
                    logger.info(f"Updated segmentation for {self.ordered_bytecodes[i].name}")
                    return True
            finally:
                if not accepted:
                    restore()
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


def decompile(
    pyc: PYCFile | Path,
    save_to: Path | None = None,
    config_file: Path | None = None,
    version: str | None = None,
    top_k: int = 10,
    trust_lnotab: bool = False,
    timeout: int | None = None,
    redis_cache_server_ip: str = None,
    redis_port: int = 1679,
) -> DecompilerResult:
    """
    Decompile a PYC file.

    :param pyc: PYCFile or Path to decompile.
    :param save_to: Path to save decompilation results to or None.
    :param config_file: Path to decompiler_config.yaml to load. Use None to load the default PyLingual config (recommended).
    :param version: Loads the models corresponding to this python version. if None, automatically detects version based on input PYC file.
    :param top_k: Max number of pyc segmentations to consider.
    :param trust_lnotab: Trust the lnotab in the input PYC for segmentation (False recommended).
    :param timeout: Maximum time in seconds to allow decompilation to run.
    :param redis_cache_server_ip: IP for the Redis cache server.
    :param redis_port: Port for the Redis cache server.
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

    segmenter, translator, cflow_model = load_models(config_file, pversion, redis_cache_server_ip, redis_port)

    if save_to:
        logger.info(f"Decompiling pyc {pyc.pyc_path.resolve() if pyc.pyc_path else repr(pyc)} to {save_to.resolve()}")
    else:
        logger.info(f"Decompiling pyc {pyc.pyc_path.resolve() if pyc.pyc_path else repr(pyc)}")
    decompiler = Decompiler(pyc, segmenter, translator, pversion, top_k, trust_lnotab, timeout, cflow_model=cflow_model)
    result = decompiler()

    logger.info("Decompilation complete")
    logger.info(f"{result.calculate_success_rate():.2%} code object success rate")
    if save_to:
        save_to.write_text(result.decompiled_source, encoding="utf-8")
        logger.info(f"Result saved to {save_to}")
    return result
