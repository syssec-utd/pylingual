from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
from pylingual.control_flow_reconstruction.cfg import CFG
from pylingual.editable_bytecode import EditableBytecode, Inst, PYCFile
from pylingual.editable_bytecode.bytecode_patches import fix_indirect_jump, fix_unreachable, remove_extended_arg, remove_nop
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
        return self.bc_a.name if self.bc_a is not None else "None"

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


def compare_pyc(pyc_a: PYCFile | Path, pyc_b: PYCFile | Path) -> list[TestResult]:
    """
    Tests the control flow of the two pyc files
    Should not be imported as it relies on TestResult class.

    note: will always patch out unreachable code

    :param pyc_path_a: First pyc to compare
    :param pyc_path_b: Second pyc to compare
    """

    pyc_a = pyc_a.copy() if isinstance(pyc_a, PYCFile) else PYCFile(pyc_a)
    pyc_b = pyc_b.copy() if isinstance(pyc_b, PYCFile) else PYCFile(pyc_b)

    pyc_a.apply_patches([remove_extended_arg, remove_nop, fix_indirect_jump, fix_unreachable, remove_extended_arg])
    pyc_b.apply_patches([remove_extended_arg, remove_nop, fix_indirect_jump, fix_unreachable, remove_extended_arg])

    results = []

    for bytecode_a, bytecode_b in matching_iter(pyc_a, pyc_b):
        if bytecode_a is None:
            test_result = TestResult(False, "Extra bytecode", None, bytecode_b)
            results.append(test_result)
            continue
        if bytecode_b is None:
            test_result = TestResult(False, "Missing bytecode", bytecode_a, None)
            results.append(test_result)
            continue
        cfg_a = bytecode_to_control_flow_graph(bytecode_a)
        cfg_b = bytecode_to_control_flow_graph(bytecode_b)
        block_graph_a = CFG.from_graph(cfg_a, bytecode_a, False)
        block_graph_b = CFG.from_graph(cfg_b, bytecode_b, False)
        if not is_control_flow_equivalent(block_graph_a, block_graph_b):
            test_result = TestResult(False, "Different control flow", bytecode_a, bytecode_b)
            results.append(test_result)
            continue

        bytecode_result = compare_bytecode(bytecode_a, bytecode_b)
        if not bytecode_result.result:
            test_result = TestResult(False, "Different bytecode", bytecode_a, bytecode_b, bytecode_result.failed_line, bytecode_result.failed_offset)
            results.append(test_result)
            continue

        test_result = TestResult(True, "Equal", bytecode_a, bytecode_b)
        results.append(test_result)

    return results
