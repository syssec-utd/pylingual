from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
from pylingual.control_flow_reconstruction.cfg import CFG
from pylingual.editable_bytecode import EditableBytecode, Inst, PYCFile
from pylingual.editable_bytecode.bytecode_patches import fix_indirect_jump, fix_unreachable, remove_extended_arg, remove_nop, replace_firstlno, replace_borrow, split_loads, remove_comprehension_get_iter
from pylingual.editable_bytecode.control_flow_graph import bytecode_to_control_flow_graph


def is_control_flow_equivalent(basic_block_graph_1: nx.DiGraph, basic_block_graph_2: nx.DiGraph) -> bool:
    # for the graphs to be equal, they have to have the same number of nodes

    if len(basic_block_graph_1) != len(basic_block_graph_2):
        return False

    # create a node mapping based on bytecode offset
    # each node is (networkx node id, data_item); in this case, the data_item will be offset
    ordered_nodes_1 = sorted(basic_block_graph_1.nodes(data="offset", default=(float("inf"),)), key=lambda node: min(node[1]))
    ordered_nodes_2 = sorted(basic_block_graph_2.nodes(data="offset", default=(float("inf"),)), key=lambda node: min(node[1]))

    # map the node ids from graph 1 to those of graph 2
    node_id_mapping = {node1[0]: node2[0] for node1, node2 in zip(ordered_nodes_1, ordered_nodes_2)}

    for node1, edges1 in basic_block_graph_1.adjacency():
        # for each node in graph 1, find the corresponding node in graph 2
        node2 = node_id_mapping[node1]
        edges2 = basic_block_graph_2[node2]

        # map the graph 1 edge destinations to use graph 2 node ids
        # make a set of all the destinations for this node pair
        mapped_destinations1 = set(node_id_mapping[dest] for dest in edges1.keys())
        destinations2 = set(edges2.keys())

        # if the outgoing edges don't match, then the control flow is not equivalent
        if mapped_destinations1 != destinations2:
            return False

    # all checks passed; these graphs are equivalent
    return True


def compare_instruction(inst_a: Inst, inst_b: Inst):
    attr_list = ("opname", "opcode", "optype", "real_size", "has_arg", "has_extended_arg", "offset", "is_jump_target")

    # resolve different types of uncond jumps
    if inst_a.is_uncond_jump and inst_b.is_uncond_jump:
        return getattr(inst_a, "argval", None) == getattr(inst_b, "argval", None)

    if not all(getattr(inst_a, attr, None) == getattr(inst_b, attr, None) for attr in attr_list):
        return False

    argval_a = getattr(inst_a, "argval", None)
    argval_b = getattr(inst_b, "argval", None)

    if argval_a == argval_b:
        return True

    if hasattr(argval_a, "co_code") and hasattr(argval_b, "co_code"):
        # the co_code's will be checked in recursive call. so can be ignored here
        return True

    return False


def compare_bytecode(pyc_a: EditableBytecode, pyc_b: EditableBytecode) -> bcComparisonResult:
    """
    Directly Compares two pyc files by recursing through root bytecode and all child bytecodes of pyc files
    Ignores some forensically irrelevant data such as:
    white space / line differences,
    Code_obj addresses

    :param pyc_a: First pyc to compare
    :param pyc_b: Second pyc to compare
    """

    if len(pyc_a) != len(pyc_b):
        return bcComparisonResult(False)

    if pyc_a.named_exception_table != pyc_b.named_exception_table:
        return bcComparisonResult(False)

    # make sure all the instructions match at this node

    for inst_a, inst_b in zip(pyc_a, pyc_b):
        if not compare_instruction(inst_a, inst_b):
            # We purposefully check pyc_b as this is our candidate pyc in decompiler.py
            fail_offset = inst_b.offset
            insts_b = pyc_b.instructions
            inst_idx = insts_b.index(inst_b)
            try:
                lno = next(inst.starts_line for inst in reversed(insts_b[:inst_idx]) if inst.starts_line is not None)
            except StopIteration:
                lno = None
            return bcComparisonResult(False, lno, fail_offset)
    return bcComparisonResult(True)


@dataclass(frozen=True)
class TestResult:
    """
    This class stores the testing result of a code object, if the code object succeeds success will be true.
    If the code object does not succeed success will be false, additionally the error message and line number is saved.

    :param success: Stores whether the code object succeeded or failed.
    :param message: Error message if the code object failed
    :param name_a: Code object name of bytecode a
    :param name_b: Code object name of bytecode b
    :param failed_line_number: The line number where the code object failed
    :param failed offset: The offset where the code object failed
    """

    success: bool
    message: str
    bc_a: EditableBytecode | None
    bc_b: EditableBytecode | None
    failed_line_number: int | None = None
    failed_offset: int | None = None

    @property
    def name_a(self) -> str:
        return self.bc_a.name if self.bc_a is not None else "None"

    @property
    def name_b(self) -> str:
        return self.bc_b.name if self.bc_b is not None else "None"

    def names(self):
        if self.name_a == self.name_b:
            return self.name_a
        return f"{self.name_a}, {self.name_b}"

    def __str__(self):
        if self.success:
            return f"{self.names()}: Success: {self.message}"
        lno_message = ""
        if None not in (self.failed_line_number, self.failed_offset):
            lno_message = f" detected at line number {self.failed_line_number} and instruction offset {self.failed_offset}"
        return f"***{self.names()}: Failure{lno_message}: {self.message}"


@dataclass(frozen=True)
class bcComparisonResult:
    result: bool
    failed_line: int | None = None
    failed_offset: int | None = None


def matching_iter(pyc_a, pyc_b):
    """
    Matches bytecodes in pyc_a and pyc_b with the same name
    """
    bc_a = list(pyc_a.iter_bytecodes())
    bc_b = list(pyc_b.iter_bytecodes())
    sm = difflib.SequenceMatcher(a=[x.name for x in bc_a], b=[x.name for x in bc_b])
    i_a = 0
    i_b = 0
    for block in sm.get_matching_blocks():
        while i_a < block.a:
            yield bc_a[i_a], None
            i_a += 1
        while i_b < block.b:
            yield None, bc_b[i_b]
            i_b += 1
        for i in range(block.size):
            yield bc_a[i_a + i], bc_b[i_b + i]
        i_a += block.size
        i_b += block.size
    while i_a < len(bc_a):
        yield bc_a[i_a], None
        i_a += 1
    while i_b < len(bc_b):
        yield None, bc_b[i_b]
        i_b += 1


PATCHES = [remove_extended_arg, remove_nop, remove_comprehension_get_iter, fix_indirect_jump, fix_unreachable, remove_extended_arg, replace_firstlno, replace_borrow, split_loads]


class PatchedPYC:
    """
    Patched copy of a pyc with lazily built block graphs.
    Pass one to compare_pyc to avoid re-preparing a pyc that is compared repeatedly.
    Code objects identical to ones in reference (ignoring line info) are shared with it instead of rebuilt,
    and ones identical to previous (apart from moved lines) are taken from it, so previous must not be used afterwards.
    """

    def __init__(self, pyc: PYCFile | Path, reference: PatchedPYC | None = None, previous: PatchedPYC | None = None):
        if isinstance(pyc, PYCFile):
            self.pyc = pyc.copy()
        else:
            self.pyc = PYCFile(pyc, reference=reference and reference.pyc, previous=previous and previous.pyc)
        self.pyc.apply_patches(PATCHES)
        self.block_graphs = {}
        if previous is not None:
            self.block_graphs = {bc: previous.block_graphs[bc] for bc in self.pyc.iter_bytecodes() if bc in previous.block_graphs}
        self.last_compared = None

    def block_graph(self, bytecode: EditableBytecode) -> CFG:
        if bytecode not in self.block_graphs:
            self.block_graphs[bytecode] = CFG.from_graph(bytecode_to_control_flow_graph(bytecode), bytecode, iterate=False)
        return self.block_graphs[bytecode]


def compare_pyc(pyc_a: PYCFile | Path | PatchedPYC, pyc_b: PYCFile | Path) -> list[TestResult]:
    """
    Tests the control flow of the two pyc files
    Should not be imported as it relies on TestResult class.

    note: will always patch out unreachable code

    :param pyc_path_a: First pyc to compare
    :param pyc_path_b: Second pyc to compare
    """

    pyc_a = pyc_a if isinstance(pyc_a, PatchedPYC) else PatchedPYC(pyc_a)
    # consecutive candidates compared against pyc_a usually differ in only a few code objects
    previous, pyc_a.last_compared = pyc_a.last_compared, None
    pyc_b = PatchedPYC(pyc_b, reference=pyc_a, previous=previous)
    pyc_a.last_compared = pyc_b

    results = []

    for bytecode_a, bytecode_b in matching_iter(pyc_a.pyc, pyc_b.pyc):
        if bytecode_a is None:
            test_result = TestResult(False, "Extra bytecode", None, bytecode_b)
            results.append(test_result)
            continue
        if bytecode_b is None:
            test_result = TestResult(False, "Missing bytecode", bytecode_a, None)
            results.append(test_result)
            continue
        if bytecode_a is bytecode_b:
            # shared with pyc_a since the code object was identical
            results.append(TestResult(True, "Equal", bytecode_a, bytecode_b))
            continue
        bytecode_result = compare_bytecode(bytecode_a, bytecode_b)
        if bytecode_result.result:
            # identical bytecode always has identical control flow, so the graphs are only built on a mismatch
            test_result = TestResult(True, "Equal", bytecode_a, bytecode_b)
            results.append(test_result)
            continue

        if not is_control_flow_equivalent(pyc_a.block_graph(bytecode_a), pyc_b.block_graph(bytecode_b)):
            test_result = TestResult(False, "Different control flow", bytecode_a, bytecode_b)
            results.append(test_result)
            continue

        test_result = TestResult(False, "Different bytecode", bytecode_a, bytecode_b, bytecode_result.failed_line, bytecode_result.failed_offset)
        results.append(test_result)

    return results
