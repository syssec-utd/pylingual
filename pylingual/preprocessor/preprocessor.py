from __future__ import annotations

from xdis.cross_dis import instruction_size, xstack_effect

from pylingual.editable_bytecode import EditableBytecode
from .container_recovery.recovery import recover
from .container_recovery.segment import Segment
from .container_recovery.stack_analysis import analyze_stack, parse_bytecode_recursive

_CONTAINER_TAGS = {"LIST", "SET", "TUPLE", "DICT"}


def _make_function_stack_effect(arg, version) -> int:
    return -int(arg or 0).bit_count() - (version < (3, 11))


class Preprocessor:
    """Rewrites container construction bytecode into single LOAD_CONST instructions.

    For each code object, analyzes the stack to identify container construction
    patterns (lists, dicts, sets, tuples, frozensets), recovers their values via
    strategy-based recovery, and replaces the bytecode span with a single
    LOAD_CONST referencing the materialized value in co_consts.
    """

    def preprocess(self, bc: EditableBytecode) -> None:
        """Process all code objects (top-level + nested)."""
        for code_obj in bc.iter_bytecodes():
            self._process_code_object(code_obj)

    def _process_code_object(self, bc: EditableBytecode) -> None:
        depths = analyze_stack(bc)
        segments = parse_bytecode_recursive(depths)
        for seg in reversed(segments):
            self._process_segment(bc, seg)
        bc._bake_jumps()

    def _process_segment(self, bc: EditableBytecode, seg: Segment) -> None:
        if seg.tag in _CONTAINER_TAGS:
            seg.compute_offsets()
            if seg.start_offset is not None and seg.end_offset is not None:
                recovery = recover(seg)
                if recovery.complete:
                    depth = 1
                    for inst in bc.instructions[bc.instructions.index(bc.get_by_offset(seg.end_offset)) + 1:]:
                        effect = xstack_effect(inst.opcode, bc.opcode, inst.arg or 0)
                        if effect is None and inst.opname == "MAKE_FUNCTION":
                            effect = _make_function_stack_effect(inst.arg, bc.version)
                        elif effect is None:
                            effect = bc.opcode.oppush[inst.opcode] - bc.opcode.oppop[inst.opcode]
                        push = 1 if inst.opname.startswith("BUILD_") else bc.opcode.oppush[inst.opcode]
                        if push >= 0 and push - effect >= depth:
                            if inst.opname in ("MAKE_FUNCTION", "SET_FUNCTION_ATTRIBUTE"):
                                return
                            break
                        depth += effect
                        if depth <= 0:
                            break
                    self._collapse_segment(bc, seg, recovery.value)
                    return
        for child in reversed(seg.ordered_children):
            if isinstance(child, Segment):
                self._process_segment(bc, child)

    def _collapse_segment(self, bc: EditableBytecode, seg: Segment, value) -> None:
        if len(value) == 0:
            return

        const_index = None
        for i, existing in enumerate(bc.co_consts):
            if value is existing or (type(value) is type(existing) and value == existing):
                const_index = i
                break
        if const_index is None:
            bc.co_consts.append(value)
            const_index = len(bc.co_consts) - 1

        start_inst = bc.get_by_offset(seg.start_offset)
        end_inst = bc.get_by_offset(seg.end_offset)
        start_idx = bc.instructions.index(start_inst)
        end_idx = bc.instructions.index(end_inst)

        opcode = bc.opcode.opmap["LOAD_CONST"]
        new_inst = bc.new_instruction(
            "LOAD_CONST",
            opcode,
            "const",
            instruction_size(opcode, bc.opcode),
            const_index,
            value,
            repr(value),
            True,
            -1,
            None,
            False,
            False,
        )
        new_inst.preprocessed_container = True

        bc.remove_instructions(bc.instructions[start_idx : end_idx + 1])
        bc.insert_instruction(start_idx, new_inst)
