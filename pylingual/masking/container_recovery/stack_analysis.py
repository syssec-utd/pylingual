from __future__ import annotations

from .segment import Segment


VAR_STACK_SENTINEL = -3000


def stack_effect(opc, opcode: int, oparg: int | None = None, *, jump: bool | None = None) -> int:
    if oparg is None:
        oparg = 0
    push = opc.oppush[opcode]
    pop = opc.oppop[opcode]

    opname = opc.opname[opcode]

    if opname == "BUILD_MAP":
        return 1 - 2 * oparg
    if opname == "CALL":
        return -(oparg + 1)
    if opname == "UNPACK_EX":
        return (oparg & 0xFF) + ((oparg >> 8) & 0xFF) - 1
    if opname == "LOAD_GLOBAL" and oparg & 1:
        return 2
    if opname == "LOAD_ATTR" and oparg & 1:
        return 1
    if opname == "LOAD_SUPER_ATTR" and oparg & 1:
        return -1

    if push == VAR_STACK_SENTINEL:
        if pop == VAR_STACK_SENTINEL:
            return oparg
        return oparg - pop

    if pop == VAR_STACK_SENTINEL:
        return push - oparg

    if pop < 0:
        return push + oparg * pop

    if push < 0:
        return oparg * (-push) - pop

    return push - pop


def analyze_stack(bytecode) -> list[tuple[int, object]]:
    opc = bytecode.opcode
    depth = 0
    results = []
    for instr in bytecode.instructions:
        arg = instr.arg if instr.arg is not None else 0
        effect = stack_effect(opc, instr.opcode, arg)
        depth += effect
        results.append((depth, instr))
    return results


def parse_list_recursive(remaining: list[tuple[int, object]]) -> Segment:
    (post_base_depth, build_instr) = remaining.pop()
    base_depth = remaining[-1][0] if remaining else post_base_depth
    size = build_instr.arg
    end_depth = base_depth - size
    cur_elem_id = size
    output_segs = [Segment("BUILD", [(post_base_depth, build_instr)])]

    if size == 0:
        return Segment("LIST", output_segs[::-1])

    cur_seg = []

    while remaining:
        if base_depth == end_depth or cur_elem_id <= 0:
            break
        (stack_depth, instr) = remaining.pop()
        if stack_depth < base_depth:
            output_segs.append(Segment(f"ELEM {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
            cur_elem_id -= 1
            base_depth -= 1
            cur_seg = []
        cur_seg.append((stack_depth, instr))

    if cur_seg and cur_elem_id > 0:
        output_segs.append(Segment(f"ELEM {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
    elif cur_seg:
        remaining.extend(cur_seg)

    return Segment("LIST", output_segs[::-1])


def parse_set_recursive(remaining: list[tuple[int, object]]) -> Segment:
    (post_base_depth, build_instr) = remaining.pop()
    base_depth = remaining[-1][0] if remaining else post_base_depth
    size = build_instr.arg
    end_depth = base_depth - size
    cur_elem_id = size
    output_segs = [Segment("BUILD", [(post_base_depth, build_instr)])]

    if size == 0:
        return Segment("SET", output_segs[::-1])

    cur_seg = []

    while remaining:
        if base_depth == end_depth or cur_elem_id <= 0:
            break
        (stack_depth, instr) = remaining.pop()
        if stack_depth < base_depth:
            output_segs.append(Segment(f"ELEM {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
            cur_elem_id -= 1
            base_depth -= 1
            cur_seg = []
        cur_seg.append((stack_depth, instr))

    if cur_seg and cur_elem_id > 0:
        output_segs.append(Segment(f"ELEM {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
    elif cur_seg:
        remaining.extend(cur_seg)

    return Segment("SET", output_segs[::-1])


def parse_tuple_recursive(remaining: list[tuple[int, object]]) -> Segment:
    (post_base_depth, build_instr) = remaining.pop()
    base_depth = remaining[-1][0] if remaining else post_base_depth
    size = build_instr.arg
    end_depth = base_depth - size
    cur_elem_id = size
    output_segs = [Segment("BUILD", [(post_base_depth, build_instr)])]

    if size == 0:
        return Segment("TUPLE", output_segs[::-1])

    cur_seg = []

    while remaining:
        if base_depth == end_depth or cur_elem_id <= 0:
            break
        (stack_depth, instr) = remaining.pop()
        if stack_depth < base_depth:
            output_segs.append(Segment(f"ELEM {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
            cur_elem_id -= 1
            base_depth -= 1
            cur_seg = []
        cur_seg.append((stack_depth, instr))

    if cur_seg and cur_elem_id > 0:
        output_segs.append(Segment(f"ELEM {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
    elif cur_seg:
        remaining.extend(cur_seg)

    return Segment("TUPLE", output_segs[::-1])


def parse_dict_recursive(remaining: list[tuple[int, object]]) -> Segment:
    (post_base_depth, build_instr) = remaining.pop()
    base_depth = remaining[-1][0] if remaining else post_base_depth
    size = build_instr.arg
    end_depth = base_depth - size * 2
    cur_elem_id = size * 2
    output_segs = [Segment("BUILD", [(post_base_depth, build_instr)])]

    if size == 0:
        return Segment("DICT", output_segs[::-1])

    cur_seg = []

    is_key = False

    while remaining:
        if base_depth == end_depth or cur_elem_id <= 0:
            break
        (stack_depth, instr) = remaining.pop()
        if stack_depth < base_depth:
            output_segs.append(Segment(f"KEY {(cur_elem_id + 1) // 2}" if is_key else f"VALUE {(cur_elem_id + 1) // 2}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
            cur_elem_id -= 1
            base_depth -= 1
            cur_seg = []
            is_key = not is_key
        cur_seg.append((stack_depth, instr))

    if cur_seg and cur_elem_id > 0:
        output_segs.append(Segment(f"KEY {(cur_elem_id + 1) // 2}" if is_key else f"VALUE {(cur_elem_id + 1) // 2}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
    elif cur_seg:
        remaining.extend(cur_seg)

    return Segment("DICT", output_segs[::-1])


def parse_bytecode_recursive(remaining: list[tuple[int, object]]) -> list[Segment]:
    output_segs = []
    cur_seg = []

    while remaining:
        (stack_depth, instr) = remaining[-1]
        if instr.opname == "BUILD_MAP":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            dict_seg = parse_dict_recursive(remaining)
            output_segs.append(dict_seg)
        elif instr.opname in ("LIST_EXTEND", "LIST_APPEND"):
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            trigger_opname = instr.opname
            remaining.pop()
            raw = [(stack_depth, instr)]
            while remaining:
                (_, i) = remaining[-1]
                remaining.pop()
                raw.append((_, i))
                if i.opname == "BUILD_LIST":
                    break
            reversed_raw = raw[::-1]
            children = [Segment("BUILD", [reversed_raw[0]])]
            if trigger_opname == "LIST_APPEND":
                elem_id = 1
                i = 1
                while i + 1 < len(reversed_raw):
                    children.append(Segment(f"ELEM {elem_id}", [reversed_raw[i], reversed_raw[i + 1]]))
                    elem_id += 1
                    i += 2
                if i < len(reversed_raw):
                    children.append(Segment("UNKNOWN", reversed_raw[i:]))
            else:
                children.append(Segment("EXTEND", reversed_raw[1:]))
            output_segs.append(Segment("LIST", children))
        elif instr.opname == "SET_UPDATE":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            remaining.pop()
            raw = [(stack_depth, instr)]
            while remaining:
                (_, i) = remaining[-1]
                remaining.pop()
                raw.append((_, i))
                if i.opname == "BUILD_SET":
                    break
            reversed_raw = raw[::-1]
            children = [Segment("BUILD", [reversed_raw[0]]), Segment("EXTEND", reversed_raw[1:])]
            output_segs.append(Segment("SET", children))
        elif instr.opname == "BUILD_LIST":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            list_seg = parse_list_recursive(remaining)
            output_segs.append(list_seg)
        elif instr.opname == "BUILD_SET":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            set_seg = parse_set_recursive(remaining)
            output_segs.append(set_seg)
        elif instr.opname == "BUILD_TUPLE":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            tuple_seg = parse_tuple_recursive(remaining)
            output_segs.append(tuple_seg)
        elif instr.opname == "LOAD_CONST" and isinstance(instr.argval, (tuple, list, dict, set, frozenset)):
            remaining.pop()
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            output_segs.append(Segment("LOAD_CONST_CONTAINER", [(stack_depth, instr)]))
        else:
            remaining.pop()
            cur_seg.append((stack_depth, instr))

    if cur_seg:
        output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))

    return output_segs[::-1]