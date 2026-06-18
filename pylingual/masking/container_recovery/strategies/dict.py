from __future__ import annotations

from ..recovery import register_recovery_strategy, recover
from ..segment import Recovery, Segment, INDENT
from ..utils import _non_empty_children, _get_build_map_size


@register_recovery_strategy(0)
def recover_dict(seg: Segment, indent: int) -> Recovery | None:
    size = _get_build_map_size(seg)
    if size is None:
        return None
    prefix = INDENT * indent
    inner = INDENT * (indent + 1)
    keys_values = [c for c in seg.ordered_children if not (isinstance(c, Segment) and c.tag == "BUILD")]
    if not keys_values:
        return Recovery("{}", True)
    pairs = []
    complete = True
    for i in range(0, len(keys_values), 2):
        key_r = recover(keys_values[i], indent + 1)
        val_r = recover(keys_values[i + 1], indent + 1)
        if not key_r.complete:
            complete = False
        if not val_r.complete:
            complete = False
        if key_r.complete and val_r.complete:
            pairs.append(f"{inner}{key_r.expr}: {val_r.expr}")
        elif key_r.complete:
            pairs.append(f"{inner}{key_r.expr}:\n{val_r.expr}")
        elif val_r.complete:
            pairs.append(f"{key_r.expr}\n{inner}: {val_r.expr}")
        else:
            pairs.append(f"{key_r.expr}\n{inner}:\n{val_r.expr}")
    body = ",\n".join(pairs)
    return Recovery("{" + f"\n{body}\n{prefix}" + "}", complete)