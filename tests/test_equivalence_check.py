import py_compile

from pylingual.equivalence_check import PatchedPYC, compare_pyc

ORIGINAL = """
def f(x):
    return x + 1

class C:
    def g(self):
        for i in range(3):
            print(i)

    def h(self):
        return [y * 2 for y in range(4)]
"""


def _pyc(tmp_path, name: str, source: str):
    src = tmp_path / f"{name}.py"
    src.write_text(source)
    out = tmp_path / f"{name}.pyc"
    py_compile.compile(str(src), cfile=str(out), doraise=True)
    return out


def _key(results):
    return [(r.success, r.message, r.name_a, r.name_b, r.failed_line_number, r.failed_offset) for r in results]


def _fresh(original, candidate):
    return _key(compare_pyc(PatchedPYC(original), PatchedPYC(candidate).pyc))


def test_identical_code_objects_are_shared(tmp_path):
    original = _pyc(tmp_path, "original", ORIGINAL)
    shifted = _pyc(tmp_path, "shifted", "\n\n" + ORIGINAL)
    patched = PatchedPYC(original)
    results = compare_pyc(patched, shifted)
    assert all(r.success for r in results)
    # class bodies store __firstlineno__ in 3.13+, so only the functions are guaranteed to be shared
    assert {r.name_a for r in results if r.bc_a is r.bc_b} >= {"<module>.f", "<module>.C.g", "<module>.C.h"}


def test_chained_compares_match_fresh_compares(tmp_path):
    original = _pyc(tmp_path, "original", ORIGINAL)
    lines_before = [inst.starts_line for bc in PatchedPYC(original).pyc.iter_bytecodes() for inst in bc.instructions]
    # h keeps failing while the lines above it move, so its failure line must follow them
    failing = ORIGINAL.replace("y * 2", "y * 3")
    candidates = [
        failing,
        failing.replace("return x + 1", "y = x\n    return y + 1"),
        "\n\n\n" + failing.replace("print(i)", "print(i, i)"),
        ORIGINAL,
        "\n" + failing,
        failing,
    ]
    patched = PatchedPYC(original)
    for n, source in enumerate(candidates):
        candidate = _pyc(tmp_path, f"candidate{n}", source)
        assert _key(compare_pyc(patched, candidate)) == _fresh(original, candidate)
    # the original is shared with candidates, so it must not be edited by them
    assert [inst.starts_line for bc in patched.pyc.iter_bytecodes() for inst in bc.instructions] == lines_before
