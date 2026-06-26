from __future__ import annotations

from ..recovery import register_recovery_strategy, recover
from ..segment import Recovery, Segment
from ..utils import _non_empty_children, _get_build_map_size


@register_recovery_strategy(0)
def recover_dict(seg: Segment, indent: int) -> Recovery | None:
    size = _get_build_map_size(seg)
    if size is None:
        return None
    keys_values = [c for c in seg.ordered_children if not (isinstance(c, Segment) and c.tag == "BUILD")]
    if not keys_values:
        return Recovery({}, True)
    result = {}
    complete = True
    for i in range(0, len(keys_values), 2):
        key_r = recover(keys_values[i], indent + 1)
        val_r = recover(keys_values[i + 1], indent + 1)
        if not key_r.complete:
            complete = False
        if not val_r.complete:
            complete = False
        result[key_r.value] = val_r.value
    return Recovery(result, complete)


@register_recovery_strategy(0)
def recover_const_key_map(seg: Segment, indent: int) -> Recovery | None:
    build_instr = None
    for child in reversed(seg.ordered_children):
        if isinstance(child, Segment) and child.tag == "BUILD":
            if len(child.ordered_children) == 1 and isinstance(child.ordered_children[0], tuple):
                instr = child.ordered_children[0][1]
                if instr.opname == "BUILD_CONST_KEY_MAP":
                    build_instr = instr
                    break
    if build_instr is None:
        return None

    key_tuple_seg = None
    values = []
    for child in seg.ordered_children:
        if isinstance(child, Segment):
            if child.tag == "KEY_TUPLE":
                key_tuple_seg = child
            elif child.tag.startswith("VALUE"):
                values.append(child)
    if key_tuple_seg is None:
        return None

    keys = key_tuple_seg.ordered_children[0][1].argval

    value_recoveries = [recover(v, indent + 1) for v in values]
    complete = all(r.complete for r in value_recoveries)

    result = {keys[i]: value_recoveries[i].value for i in range(min(len(keys), len(value_recoveries)))}
    return Recovery(result, complete)