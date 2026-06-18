from __future__ import annotations

from ..recovery import register_recovery_strategy, recover
from ..segment import Recovery, Segment, INDENT
from ..utils import _non_empty_children, _recover_load_instr, _get_build_list_size, _has_list_append_pattern


@register_recovery_strategy(1)
def recover_build_list(seg: Segment, indent: int) -> Recovery | None:
    size = _get_build_list_size(seg)
    if size is None:
        return None
    if _has_list_append_pattern(seg):
        return None
    prefix = INDENT * indent
    inner = INDENT * (indent + 1)
    elems = [c for c in seg.ordered_children if not (isinstance(c, Segment) and c.tag == "BUILD")]
    if not elems:
        return Recovery("[]", True)
    items = []
    complete = True
    for elem in elems:
        r = recover(elem, indent + 1)
        if not r.complete:
            complete = False
        if r.complete:
            items.append(f"{inner}{r.expr}")
        else:
            items.append(r.expr)
    body = ",\n".join(items)
    return Recovery("[" + f"\n{body}\n{prefix}" + "]", complete)


@register_recovery_strategy(4)
def recover_list_extend(seg: Segment, indent: int) -> Recovery | None:
    children = _non_empty_children(seg)
    if len(children) != 2:
        return None
    build_child, extend_child = children
    if not (isinstance(build_child, Segment) and build_child.tag == "BUILD"):
        return None
    if not (isinstance(extend_child, Segment) and extend_child.tag == "EXTEND"):
        return None
    build_instrs = build_child.ordered_children
    if len(build_instrs) != 1 or not isinstance(build_instrs[0], tuple):
        return None
    if build_instrs[0][1].opname != "BUILD_LIST":
        return None
    extend_instrs = extend_child.ordered_children
    if len(extend_instrs) != 2 or not all(isinstance(i, tuple) for i in extend_instrs):
        return None
    names = [i[1].opname for i in extend_instrs]
    if names != ["LOAD_CONST", "LIST_EXTEND"]:
        return None
    val = extend_instrs[0][1].argval
    return Recovery(repr(list(val)) if isinstance(val, tuple) else repr(val), True)


@register_recovery_strategy(6)
def recover_list_append(seg: Segment, indent: int) -> Recovery | None:
    children = _non_empty_children(seg)
    if len(children) < 2:
        return None
    build_child = children[0]
    if not (isinstance(build_child, Segment) and build_child.tag == "BUILD"):
        return None
    build_instrs = build_child.ordered_children
    if len(build_instrs) != 1 or not isinstance(build_instrs[0], tuple):
        return None
    if build_instrs[0][1].opname != "BUILD_LIST":
        return None
    elem_children = children[1:]
    if not all(isinstance(c, Segment) and c.tag.startswith("ELEM") for c in elem_children):
        return None
    items = []
    for elem in elem_children:
        inner = elem.ordered_children
        if len(inner) < 1 or not isinstance(inner[0], tuple):
            return None
        load_instr = inner[0][1]
        r = _recover_load_instr(load_instr)
        if r is None:
            return Recovery("", False)
        items.append(r.expr)
    return Recovery("[" + ", ".join(items) + "]", True)