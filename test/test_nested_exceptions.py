"""Real Python 3.11 bytecode regressions, without model downloads.

Requires an existing Python 3.11 interpreter discoverable by uv (offline).
Compilation uses stdin/stdout, so the fixtures contain no local paths.
"""

import ast
import subprocess
import unittest

from pylingual.control_flow_reconstruction.source import SourceContext, sanitize_lines
from pylingual.control_flow_reconstruction.structure import bc_to_cft
from pylingual.editable_bytecode import PYCFile
from pylingual.equivalence_check import compare_pyc


NESTED_EMPTY = '''def main():
    try:
        try:
            try:
                pass
            except Exception as e:
                pass
        except Exception as e:
            pass
    except Exception as e:
        try:
            try:
                pass
            except Exception as e:
                pass
        except Exception as e:
            try:
                pass
            except Exception as e:
                pass
if __name__ == "__main__":
    main()
'''

NESTED_RAISE = '''def run(kind=0):
    events = []
    try:
        try:
            try:
                if kind == 1:
                    raise TypeError("escape")
                if kind == 2:
                    return ["early"]
                raise ValueError("inner")
            except ValueError as inner:
                events.append(str(inner))
                raise KeyError("middle")
        except KeyError as middle:
            events.append("middle")
            raise RuntimeError("outer")
    except RuntimeError as outer:
        try:
            try:
                raise LookupError("handler")
            except LookupError as nested:
                events.append(str(nested))
        except Exception as unexpected:
            events.append("unexpected")
        events.append("outer")
    return events
'''


class NestedExceptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiler = subprocess.check_output(["uv", "python", "find", "3.11", "--offline"], text=True, encoding="utf-8").strip()

    def pyc(self, source):
        command = "import importlib.util, marshal, sys; source = sys.stdin.read(); sys.stdout.buffer.write(importlib.util.MAGIC_NUMBER + bytes(12) + marshal.dumps(compile(source, 'nested_fixture.py', 'exec')))"
        return PYCFile(subprocess.check_output([self.compiler, "-c", command], input=source.encode("utf-8")))

    def reconstruct(self, source, predicted=False):
        pyc = self.pyc(source)
        if predicted:
            lines = ["def main():", "if __name__ == '__main__':", "main()", "while True:", "while True:", "try:", "pass", "except Exception as e:", "break", "except Exception as e:", "return None", "except Exception as e:", "return", "pass", "except Exception as e:", "pass", "except Exception as e:", "try:", "break", "except Exception as e:", "return None"]
            starts = [{0: 1, 6: 2, 14: 3}, {0: 4, 2: 5, 4: 6, 6: 7, 10: 8, 18: 9, 54: 10, 62: 11, 92: 12, 100: 13, 102: 14, 108: 15, 116: 16, 146: 17, 154: 18, 156: 19, 160: 20, 168: 21}]
            for bc, mapping in zip(pyc.iter_bytecodes(), starts):
                for inst in bc:
                    inst.starts_line = mapping.get(inst.offset)
        else:
            lines = source.splitlines()
            seen = set()
            for bc in pyc.iter_bytecodes():
                lno_insts = bc.get_lno_insts(previously_seen_lines=seen)
                seen.update(lno_insts)
                for line, instructions in lno_insts.items():
                    for i, inst in enumerate(instructions):
                        inst.starts_line = line if i == 0 else None
        lines = sanitize_lines(lines)
        cfts = {bc.codeobj: bc_to_cft(bc, lines) for bc in pyc.iter_bytecodes()}
        restored = str(SourceContext(pyc, lines, cfts))
        self.assertNotIn("cdg fallback", restored)
        ast.parse(restored)
        results = compare_pyc(pyc, self.pyc(restored))
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r.success for r in results), "\n".join(map(str, results)) + "\n" + restored)
        return restored

    def test_issue109_exact_source_lines(self):
        restored = self.reconstruct(NESTED_EMPTY)
        self.assertEqual(sum(isinstance(node, ast.Try) for node in ast.walk(ast.parse(restored))), 6)

    def test_issue109_model_source_lines(self):
        restored = self.reconstruct(NESTED_EMPTY, predicted=True)
        self.assertEqual(sum(isinstance(node, ast.Try) for node in ast.walk(ast.parse(restored))), 6)

    def test_empty_handlers_keep_their_actual_names(self):
        self.reconstruct(NESTED_EMPTY.replace("Exception", "LookupError").replace(" as e:", " as caught:"))

    def test_reachable_nested_raises_and_early_return(self):
        restored = self.reconstruct(NESTED_RAISE)
        original, candidate = {}, {}
        exec(NESTED_RAISE, original)
        exec(restored, candidate)
        for namespace in (original, candidate):
            self.assertEqual(namespace["run"](), ["inner", "middle", "handler", "outer"])
            self.assertEqual(namespace["run"](2), ["early"])
            with self.assertRaisesRegex(TypeError, "escape"):
                namespace["run"](1)


if __name__ == "__main__":
    unittest.main()
