"""Model-free regression tests for speculative segmentation correction."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pylingual.control_flow_reconstruction.cft import InstTemplate
from pylingual.control_flow_reconstruction.source import SourceContext
from pylingual.decompiler import Decompiler
from pylingual.equivalence_check import TestResult


class SequenceTemplate:
    def __init__(self, instructions):
        self.instructions = instructions
        self.templates = [InstTemplate(inst) for inst in instructions]
        self.header_lines = []

    def get_instructions(self):
        return self.instructions

    def to_indented_source(self, source):
        return [line for template in self.templates for line in source[template]]


def make_decompiler():
    d = Decompiler.__new__(Decompiler)
    codes = [compile(f"value = {i}", f"fixture_{i}", "exec") for i in range(3)]
    d.ordered_bytecodes = [SimpleNamespace(codeobj=co, name=f"fixture_{i}", globals=[], nonlocals=[], parent=None) for i, co in enumerate(codes)]
    d.ordered_instructions = []
    for bc in d.ordered_bytecodes:
        d.ordered_instructions.append([SimpleNamespace(bytecode=bc, starts_line=None, opname="NOP", offset=j * 2) for j in range(2)])
    d.segmentation_results = [[{"entity": "B", "score": 0.5}, {"entity": "B", "score": 0.5}] for _ in codes]
    d.translation_results = [[f"value = {i}", "value = MASK_10"] for i in range(3)]
    d.global_masker = SimpleNamespace(global_tab={10: "MASK_10"}, get_model_view=lambda inst: "NOP")
    d.pyc = SimpleNamespace(codeobj=codes[0], version=(3, 11), iter_bytecodes=lambda: iter(d.ordered_bytecodes), fix_while=lambda lines: None)
    d.version = (3, 11)
    d.top_k = 2
    d.highest_k_used = 0
    d.name = "fixture"
    d.update_starts_line()
    d.update_source_lines()
    d.unmask_lines()
    cfts = {bc.codeobj: SequenceTemplate(insts) for bc, insts in zip(d.ordered_bytecodes, d.ordered_instructions)}
    cfts[codes[0]] = SequenceTemplate([inst for insts in d.ordered_instructions for inst in insts])
    d.source_context = SourceContext(d.pyc, d.source_lines, cfts)
    d.reconstruct_source()
    d.equivalence_results = results(d, False, False, True)
    d.translator = Mock(return_value=["value = MASK_10"])
    d.check_reconstruction = Mock(return_value=results(d, False, False, True))
    return d


def results(d, *successes):
    return [TestResult(success, "Equal" if success else "Different bytecode", bc, bc) for bc, success in zip(d.ordered_bytecodes, successes)]


def predictions(*alternatives):
    return patch("pylingual.decompiler.get_top_k_predictions", return_value=["BB", *alternatives])


class SegmentationCorrectionTests(unittest.TestCase):
    def assert_restored(self, d, original):
        self.assertEqual(d.translation_results, original[0])
        self.assertEqual(d.source_lines, original[1])
        self.assertEqual(d.indented_source, original[2])
        self.assertEqual(d.source_context.lines, original[3])
        self.assertEqual(d.source_context.cache, original[4])
        self.assertEqual([[inst.starts_line for inst in insts] for insts in d.ordered_instructions], original[5])
        self.assertEqual([[r["entity"] for r in seg] for seg in d.segmentation_results], original[6])
        self.assertEqual(d.equivalence_results, original[7])
        self.assertEqual(str(d.source_context), original[2])

    def snapshot(self, d):
        return (
            [row[:] for row in d.translation_results], d.source_lines[:], d.indented_source,
            d.source_context.lines[:], d.source_context.cache.copy(),
            [[inst.starts_line for inst in insts] for insts in d.ordered_instructions],
            [[r["entity"] for r in seg] for seg in d.segmentation_results], d.equivalence_results[:],
        )

    def test_rejected_candidate_restores_all_source_state(self):
        d = make_decompiler()
        original = self.snapshot(d)
        with predictions("BI"):
            self.assertFalse(d.correct_segmentation(0))
        self.assert_restored(d, original)

    def test_rejected_merge_does_not_break_next_code_object(self):
        d = make_decompiler()
        with predictions("BI"):
            self.assertFalse(d.correct_segmentation(0))
            # The old translation row has one line instead of two. The next
            # attempt indexes line five in cft.py against only four lines.
            self.assertFalse(d.correct_segmentation(1))
        self.assertEqual(d.translation_results[0], ["value = 0", "value = MASK_10"])

    def test_exceptions_restore_state_and_propagate(self):
        for stage in ("translator", "unmask_lines", "reconstruct_source", "check_reconstruction"):
            with self.subTest(stage=stage):
                d = make_decompiler()
                original = self.snapshot(d)
                error = RuntimeError(stage)
                with patch.object(d, stage, side_effect=error), predictions("BI"):
                    with self.assertRaises(RuntimeError) as raised:
                        d.correct_segmentation(0)
                self.assertIs(raised.exception, error)
                self.assert_restored(d, original)

    def test_empty_checker_results_reject_candidate(self):
        d = make_decompiler()
        original = self.snapshot(d)
        d.check_reconstruction.return_value = []
        with predictions("BI"):
            self.assertFalse(d.correct_segmentation(1))
        self.assert_restored(d, original)

    def test_empty_checker_results_do_not_resolve_compile_error(self):
        d = make_decompiler()
        d.equivalence_results = [SyntaxError("invalid syntax")]
        original = self.snapshot(d)
        d.check_reconstruction.return_value = []
        with predictions("BI"):
            self.assertFalse(d.correct_segmentation(0, from_comp_error=True))
        self.assert_restored(d, original)

    def test_extra_candidate_code_object_does_not_select_wrong_result(self):
        d = make_decompiler()
        original = self.snapshot(d)
        extra = TestResult(True, "Equal", None, d.ordered_bytecodes[0])
        d.check_reconstruction.return_value = [extra, *results(d, False, False, True)]
        with predictions("BI"):
            self.assertFalse(d.correct_segmentation(0))
        self.assert_restored(d, original)

    def test_success_cannot_regress_previously_passing_code_object(self):
        d = make_decompiler()
        original = self.snapshot(d)
        d.check_reconstruction.return_value = results(d, True, False, False)
        with predictions("BI"):
            self.assertFalse(d.correct_segmentation(0))
        self.assert_restored(d, original)

    def test_success_stores_complete_results_for_current_source(self):
        d = make_decompiler()
        checked = [TestResult(False, "Extra bytecode", None, d.ordered_bytecodes[0]), *results(d, True, True, True)]
        d.check_reconstruction.return_value = checked
        with predictions("BI"):
            self.assertTrue(d.correct_segmentation(0))
        self.assertIs(d.equivalence_results, checked)
        self.assertEqual(d.translation_results[0], ["value = MASK_10"])
        self.assertEqual(d.highest_k_used, 1)
        self.assertEqual(d.indented_source, str(d.source_context))

    def test_correct_failures_maps_original_code_objects(self):
        d = make_decompiler()
        d.equivalence_results = [TestResult(False, "Extra bytecode", None, d.ordered_bytecodes[0]), *results(d, True, False, True)]
        with patch.object(d, "correct_segmentation", return_value=False) as correct:
            d.correct_failures()
        correct.assert_called_once_with(1)

    def test_purge_compile_errors_marks_the_original_code_object(self):
        d = make_decompiler()
        d.equivalence_results = [SyntaxError("invalid syntax")]
        extra = TestResult(False, "Extra bytecode", None, d.ordered_bytecodes[0])
        d.check_reconstruction.return_value = [extra, *results(d, True, True, True)]
        with patch.object(d, "find_comp_error_cause", return_value=0):
            purged = d.purge_comp_errors()
        self.assertIs(purged[0], extra)
        self.assertEqual(purged[1].message, "Compilation Error")
        self.assertIs(purged[1].bc_a, d.ordered_bytecodes[0])


if __name__ == "__main__":
    unittest.main()
