import tempfile
from pathlib import Path
from pylingual.utils.generate_bytecode import compile_version
from pylingual.editable_bytecode import PYCFile
from pylingual.editable_bytecode.control_flow_graph import bytecode_to_control_flow_graph
from pylingual.control_flow_reconstruction.cfg import CFG


def analyze_cfg(code, name):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        src_path = tmpdir / "test.py"
        src_path.write_text(code)
        pyc_path = tmpdir / "test.pyc"

        compile_version(src_path, pyc_path, (3, 14))
        pyc = PYCFile(pyc_path)

        module_bc = pyc.iter_bytecodes().__next__()
        func_bc = None
        for const in module_bc.co_consts:
            if const is not None and hasattr(const, "instructions"):
                func_bc = const
                break
        if func_bc is None:
            print("No function found in constants")
            return

        cfg_nx = bytecode_to_control_flow_graph(func_bc)
        cfg = CFG.from_graph(cfg_nx, func_bc, source=code.split("\n"))

        print(f"=== {name} ===")
        print("Nodes:")
        for node in cfg.ordered_iter():
            insts = [(i.offset, i.opname) for i in node.get_instructions()]
            in_deg = cfg.in_degree(node)
            print(f"{node.offset}: {insts} (in_deg={in_deg})")

        print()
        print("Edges by category:")
        for src in cfg.ordered_iter():
            for dst in cfg.successors(src):
                edge_data = cfg.edges.get((src, dst), {})
                if isinstance(edge_data, dict):
                    kind = edge_data.get("kind", "unknown")
                else:
                    kind = getattr(edge_data, "kind", "unknown")
                category = "natural" if kind in ["fall", "jump"] else ("conditional" if kind in ["true_jump", "false_jump"] else "exception" if kind == "exception" else "meta")
                print(f"{src.offset} -> {dst.offset}: kind={kind}, category={category}")
        print()


# While loop with with statement
code_with = """
def test():
    while True:
        with a:
            print("inside while with")
"""

analyze_cfg(code_with, "While loop with with statement")
