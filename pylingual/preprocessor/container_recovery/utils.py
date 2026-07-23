from __future__ import annotations

from .segment import Recovery, Segment


_COMMON_CONSTANTS = {
    "AssertionError": AssertionError,
    "NotImplementedError": NotImplementedError,
    "tuple": tuple,
    "all": all,
    "any": any,
    "list": list,
    "set": set,
    "None": None,
    '""': "",
    "True": True,
    "False": False,
    "-1": -1,
    "frozenset": frozenset,
    "()": (),
}


def _resolve_common_constant(instr):
    return instr.argval if instr.argval != instr.arg else _COMMON_CONSTANTS[instr.argrepr]


def _get_build_map_size(seg: Segment) -> int | None:
    for child in reversed(seg.ordered_children):
        if isinstance(child, Segment) and child.tag == "BUILD":
            if len(child.ordered_children) == 1 and isinstance(child.ordered_children[0], tuple):
                instr = child.ordered_children[0][1]
                if instr.opname == "BUILD_MAP":
                    return instr.arg
    return None


def _get_build_list_size(seg: Segment) -> int | None:
    for child in reversed(seg.ordered_children):
        if isinstance(child, Segment) and child.tag == "BUILD":
            if len(child.ordered_children) == 1 and isinstance(child.ordered_children[0], tuple):
                instr = child.ordered_children[0][1]
                if instr.opname == "BUILD_LIST":
                    return instr.arg
    return None


def _get_build_set_size(seg: Segment) -> int | None:
    for child in reversed(seg.ordered_children):
        if isinstance(child, Segment) and child.tag == "BUILD":
            if len(child.ordered_children) == 1 and isinstance(child.ordered_children[0], tuple):
                instr = child.ordered_children[0][1]
                if instr.opname == "BUILD_SET":
                    return instr.arg
    return None


def _get_build_tuple_size(seg: Segment) -> int | None:
    for child in reversed(seg.ordered_children):
        if isinstance(child, Segment) and child.tag == "BUILD":
            if len(child.ordered_children) == 1 and isinstance(child.ordered_children[0], tuple):
                instr = child.ordered_children[0][1]
                if instr.opname == "BUILD_TUPLE":
                    return instr.arg
    return None


def _has_list_append_pattern(seg: Segment) -> bool:
    for c in seg.ordered_children:
        if isinstance(c, Segment) and c.tag.startswith("ELEM"):
            for instr in c.ordered_children:
                if isinstance(instr, tuple) and instr[1].opname == "LIST_APPEND":
                    return True
        if isinstance(c, Segment) and c.tag == "EXTEND":
            for instr in c.ordered_children:
                if isinstance(instr, tuple) and instr[1].opname == "LIST_EXTEND":
                    return True
    return False


def _non_empty_children(seg: Segment) -> list:
    return [c for c in seg.ordered_children
            if not (isinstance(c, Segment) and c.tag == "UNKNOWN" and len(c.ordered_children) == 0)]


def _single_instr(seg: Segment) -> tuple | None:
    children = _non_empty_children(seg)
    if len(children) == 1 and isinstance(children[0], tuple):
        return children[0]
    if len(children) == 1 and isinstance(children[0], Segment) and children[0].tag == "UNKNOWN" and len(children[0].ordered_children) == 1 and isinstance(children[0].ordered_children[0], tuple):
        return children[0].ordered_children[0]
    return None


def _recover_load_instr(instr) -> Recovery | None:
    if instr.opname == "LOAD_SMALL_INT":
        return Recovery(instr.argval, True)
    if instr.opname == "LOAD_CONST":
        return Recovery(instr.argval, True)
    if instr.opname == "LOAD_COMMON_CONSTANT":
        return Recovery(_resolve_common_constant(instr), True)
    return None
