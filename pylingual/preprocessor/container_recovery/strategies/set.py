from __future__ import annotations

from ..recovery import register_recovery_strategy, recover
from ..segment import Recovery, Segment
from ..utils import _non_empty_children, _get_build_set_size


@register_recovery_strategy(2)
def recover_build_set(seg: Segment, indent: int) -> Recovery | None:
    size = _get_build_set_size(seg)
    if size is None or size == 0:
        return None
    elems = [c for c in seg.ordered_children if not (isinstance(c, Segment) and c.tag == "BUILD")]
    if not elems:
        return Recovery(set(), True)
    items = []
    complete = True
    for elem in elems:
        r = recover(elem, indent + 1)
        if not r.complete:
            complete = False
        items.append(r.value)
    return Recovery(set(items), complete)


@register_recovery_strategy(5)
def recover_set_update(seg: Segment, indent: int) -> Recovery | None:
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
    if build_instrs[0][1].opname != "BUILD_SET":
        return None
    extend_instrs = extend_child.ordered_children
    if len(extend_instrs) != 2 or not all(isinstance(i, tuple) for i in extend_instrs):
        return None
    names = [i[1].opname for i in extend_instrs]
    if names != ["LOAD_CONST", "SET_UPDATE"]:
        return None
    val = extend_instrs[0][1].argval
    if isinstance(val, (tuple, frozenset, set)):
        return Recovery(set(val), True)
    return Recovery(val, True)