from __future__ import annotations

from ..recovery import register_recovery_strategy, recover
from ..segment import Recovery, Segment
from ..utils import _non_empty_children, _single_instr


@register_recovery_strategy(7)
def recover_const_container(seg: Segment, indent: int) -> Recovery | None:
    if seg.tag != "LOAD_CONST_CONTAINER":
        return None
    instr = _single_instr(seg)
    if instr is None:
        return None
    val = instr[1].argval
    if isinstance(val, frozenset):
        val = set(val)
    return Recovery(val, True)


@register_recovery_strategy(8)
def recover_load_const(seg: Segment, indent: int) -> Recovery | None:
    instr = _single_instr(seg)
    if instr is None or instr[1].opname != "LOAD_CONST":
        return None
    return Recovery(instr[1].argval, True)


@register_recovery_strategy(9)
def recover_small_int(seg: Segment, indent: int) -> Recovery | None:
    instr = _single_instr(seg)
    if instr is None or instr[1].opname != "LOAD_SMALL_INT":
        return None
    return Recovery(instr[1].argval, True)


@register_recovery_strategy(10)
def recover_common_constant(seg: Segment, indent: int) -> Recovery | None:
    instr = _single_instr(seg)
    if instr is None or instr[1].opname != "LOAD_COMMON_CONSTANT":
        return None
    return Recovery(instr[1].argval, True)


@register_recovery_strategy(11)
def recover_delegate(seg: Segment, indent: int) -> Recovery | None:
    children = _non_empty_children(seg)
    if len(children) == 1 and isinstance(children[0], Segment):
        return recover(children[0], indent)
    return None