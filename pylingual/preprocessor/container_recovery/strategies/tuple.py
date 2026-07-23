from __future__ import annotations

from ..recovery import register_recovery_strategy, recover
from ..segment import Recovery, Segment
from ..utils import _get_build_tuple_size


@register_recovery_strategy(3)
def recover_build_tuple(seg: Segment, indent: int) -> Recovery | None:
    size = _get_build_tuple_size(seg)
    if size is None or size == 0:
        return None
    elems = [c for c in seg.ordered_children if not (isinstance(c, Segment) and c.tag == "BUILD")]
    if not elems:
        return Recovery((), True)
    items = []
    complete = True
    for elem in elems:
        r = recover(elem, indent + 1)
        if not r.complete:
            complete = False
        items.append(r.value)
    return Recovery(tuple(items), complete)