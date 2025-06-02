import contextlib
import difflib
import json
import multiprocessing
import os
import warnings

from collections import defaultdict
from enum import Enum
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory

import click
import rich
from rich.progress import track

from pylingual.control_flow_reconstruction.cfg import CFG
from pylingual.control_flow_reconstruction.structure import bc_to_cft
from pylingual.main import print_result
from pylingual.control_flow_reconstruction.source import SourceContext
from pylingual.editable_bytecode import PYCFile
from pylingual.equivalence_check import compare_pyc
from pylingual.utils.version import PythonVersion
from pylingual.utils.generate_bytecode import compile_version, CompileError
from dataset_generation.normalize_source import normalize_source


class Result(Enum):
    Success = "success"
    Failure = "failure"
    Error = "error"
    CompileError = "compile_error"


def edit_pyc_lines(pyc: PYCFile, src_lines: list[str]):
    if pyc.version == (3, 10):
        pyc.replace_duplicated_returns10(src_lines)
    elif pyc.version == (3, 12):
        pyc.replace_duplicated_returns12(src_lines)
    seen_lines = set()
    # multiple instructions can start the same lno, but the segmentation model will only assign the lno to the first one
    for bc in pyc.iter_bytecodes():
        if bc.is_comprehension:
            continue

        # create a dict of line num : [bytecodes composing line]
        lno_bytecodes = bc.get_lno_insts(previously_seen_lines=seen_lines)
        seen_lines.update(lno_bytecodes.keys())

        for lno, line_insts in lno_bytecodes.items():
            line_insts[0].starts_line = lno
            for inst in line_insts[1:]:
                inst.starts_line = None


def run(file: Path, out_dir: Path, version: PythonVersion, print=False):
    try:
        out_dir = get_unused(out_dir / file.stem, False)
        out_dir.mkdir(parents=True)
        if file.is_dir():
            file = next(file.iterdir())

        in_src = normalize_source(file.read_text(), replace_docstrings=True)
        src_lines = in_src.split("\n")
        in_path = out_dir / "a.py"
        in_path.write_text(in_src, encoding="utf-8")
        in_pyc = out_dir / "a.pyc"

        compile_version(in_path, in_pyc, version)
        pyc = PYCFile(in_pyc)
        edit_pyc_lines(pyc, src_lines)

        cfts = {bc.codeobj: bc_to_cft(bc) for bc in pyc.iter_bytecodes()}
        out_src = normalize_source(str(SourceContext(pyc, src_lines, cfts)))

        out_path = out_dir / "b.py"
        out_path.write_text(out_src, encoding="utf-8")
        out_pyc = out_dir / "b.pyc"
        compile_version(out_path, out_pyc, version)
        result = compare_pyc(in_pyc, out_pyc)
        if print:
            print_result(f"Equivalance results for {file}", result)
        return Result.Success if all(x.success for x in result) else Result.Failure, file, out_dir
    except (CompileError, SyntaxError):
        return Result.CompileError, file, out_dir
    except Exception:
        rich.get_console().print_exception()
        return Result.Error, file, out_dir


class NoPool:
    imap_unordered = map


def print_diff(a: Path, b: Path):
    a_text = a.read_text()
    b_text = b.read_text()
    a_lines = a_text.split("\n")
    b_lines = b_text.split("\n")
    console = rich.console.Console(highlight=False)
    print(a_text)
    print("=" * 40)
    print(b_text)
    print("=" * 40)
    line = None
    for line in difflib.unified_diff(a_lines, b_lines, str(a), str(b)):
        style = "red" if line[0] == "-" else "green" if line[0] == "+" else "blue" if line[0] == "@" else ""
        console.print(line, style=style)
    if line is None:
        print("equal")


def get_unused(a: Path, _=True):
    if not _ and not a.exists():
        return a
    stem = a.stem
    i = 0
    while True:
        a = a.with_stem(f"{stem}_{i}")
        i += 1
        if not a.exists():
            return a


@click.command(help="Run the control-flow reconstructor")
@click.argument("input", type=Path)
@click.argument("output", type=str, default="")
@click.option("-v", "--version", type=PythonVersion, default=PythonVersion((3, 12)), help="Python version to compile as")
@click.option("-p", "--processes", type=int, default=os.cpu_count(), help="Number of processes")
@click.option("-d", "--prefix", type=Path, default=Path("/tmp/cflow_test"), help="Base dir for all output")
@click.option("-g", "--graph", is_flag=False, flag_value="graph", help="Enable CFG visualization")
@click.option("-f", "--graph-format", default="jpg", help="Output format supported by pydot")
def main(input: Path, output: str, version: PythonVersion, graph: str | None, prefix: Path, processes: int, graph_format: str):
    warnings.filterwarnings("ignore")
    print = rich.get_console().print
    if graph:
        CFG.enable_graphing(prefix / graph, graph_format)
    if input.is_file() and input.suffix == ".py":
        if output:
            out = contextlib.nullcontext(output)
        else:
            out = TemporaryDirectory()
        with out as o:
            o = Path(o)
            results = run(input, o, version)[0]
            if results in [Result.CompileError, Result.Error]:
                print(results)
            else:
                print_diff(o / input.stem / "a.py", o / input.stem / "b.py")
    else:
        if not output:
            out_dir = get_unused(prefix / str(version) / input.stem)
        else:
            out_dir = prefix / output
        print(f"Saving results to {out_dir}")
        results = defaultdict(list)
        f = partial(run, out_dir=out_dir, version=version)
        if input.is_dir():
            files = list(input.iterdir())
        else:
            files = list(map(Path, input.read_text().strip().split("\n")))

        if processes > 1:
            pool = multiprocessing.Pool(processes=processes)
        else:
            pool = contextlib.nullcontext(NoPool)
        dir_map = {}
        with pool as p:
            for result, input, od in track(p.imap_unordered(f, files), total=len(files)):
                results[result].append(input)
                dir_map[str(input)] = str(od)

        for res in Result:
            print(f"{res}: {len(results[res])}")
        total = sum(len(x) for x in results.values())
        if total:
            print(f"{len(results[Result.Success])} / {total} succeeded ({len(results[Result.Success]) / total:.3%})")
        res = json.dumps({k.value: list(map(str, v)) for k, v in results.items()} | {'map': dir_map})
        (out_dir / "results.json").write_text(res)


if __name__ == "__main__":
    main()
