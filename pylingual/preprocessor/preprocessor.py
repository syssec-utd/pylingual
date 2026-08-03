from __future__ import annotations

import logging

from xdis.cross_dis import instruction_size, xstack_effect

from pylingual.editable_bytecode import EditableBytecode, Inst
from .container_recovery.recovery import recover
from .container_recovery.segment import Segment
from .container_recovery.stack_analysis import analyze_stack, parse_bytecode_recursive

_CONTAINER_TAGS = {"LIST", "SET", "TUPLE", "DICT"}

logger = logging.getLogger(__name__)


def _constants_match(left, right) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(_constants_match(a, b) for a, b in zip(left, right))
    if type(left) is dict:
        return len(left) == len(right) and all(
            _constants_match(a_key, b_key) and _constants_match(a_value, b_value)
            for (a_key, a_value), (b_key, b_value) in zip(left.items(), right.items())
        )
    if type(left) in (set, frozenset):
        return len(left) == len(right) and all(any(_constants_match(a, b) for b in right) for a in left)
    if type(left) is slice:
        return (
            _constants_match(left.start, right.start)
            and _constants_match(left.stop, right.stop)
            and _constants_match(left.step, right.step)
        )
    return left is right or left == right


def _make_function_stack_effect(arg, version) -> int:
    return -int(arg or 0).bit_count() - (version < (3, 11))


class Tracer:
    """Trace an object placed on the stack before an instruction sequence."""

    def __init__(self, instructions: list[Inst]):
        self.instructions = instructions

    def trace(self) -> tuple[int, int] | None:
        """Return the consuming instruction index and its zero-based TOS argument."""
        depth = 1
        for index, inst in enumerate(self.instructions):
            effect = xstack_effect(inst.opcode, inst.bytecode.opcode, inst.arg or 0)
            if effect is None and inst.opname == "MAKE_FUNCTION":
                effect = _make_function_stack_effect(inst.arg, inst.bytecode.version)
            elif effect is None:
                effect = inst.bytecode.opcode.oppush[inst.opcode] - inst.bytecode.opcode.oppop[inst.opcode]

            push = 1 if inst.opname.startswith("BUILD_") else inst.bytecode.opcode.oppush[inst.opcode]
            pop = push - effect
            if push >= 0 and pop >= depth:
                return index, depth - 1
            depth += effect
            if depth <= 0:
                break
        return None


def _preserve_container(consumer: Inst, argnum: int) -> bool:
    if consumer.opname in ("MAKE_FUNCTION", "SET_FUNCTION_ATTRIBUTE"):
        return True
    if consumer.opname == "DICT_MERGE" and argnum in (0, 1):
        return True
    if consumer.opname == "CALL_FUNCTION_EX" and argnum == 0:
        return consumer.arg is None or isinstance(consumer.arg, int) and bool(consumer.arg & 1)
    return False


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
                    end_index = bc.instructions.index(bc.get_by_offset(seg.end_offset))
                    following = bc.instructions[end_index + 1:]
                    consumption = Tracer(following).trace()
                    crosses_merge = consumption is not None and any(
                        inst.opname.endswith("_MERGE") for inst in following[:consumption[0] + 1]
                    )
                    if crosses_merge:
                        logger.debug(
                            "Tracer does not support tracing consumers through *_MERGE instructions; "
                            "skipping container folding"
                        )
                    elif consumption is None or not _preserve_container(following[consumption[0]], consumption[1]):
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
            if _constants_match(value, existing):
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
        new_inst.arg = const_index
