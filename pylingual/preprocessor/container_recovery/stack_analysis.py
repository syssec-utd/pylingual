from __future__ import annotations

from xdis.cross_dis import xstack_effect

from .segment import Segment


def stripped_precall_effect(instr) -> int:
    """3.11 splits a call into PRECALL argc (pops argc) and CALL argc (pops 1), but PRECALL is stripped from the bytecode."""
    if instr.opname == "CALL" and instr.bytecode.version == (3, 11):
        return -(instr.arg or 0)
    return 0


def analyze_stack(bytecode) -> list[tuple[int, object]]:
    opc = bytecode.opcode
    depth = 0
    results = []
    for instr in bytecode.instructions:
        arg = instr.arg if instr.arg is not None else 0
        effect = xstack_effect(instr.opcode, opc, arg)
        if effect is None:
            effect = opc.oppush[instr.opcode] - opc.oppop[instr.opcode]
        effect += stripped_precall_effect(instr)
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
            cur_elem_id -= base_depth - stack_depth
            base_depth = stack_depth
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
            cur_elem_id -= base_depth - stack_depth
            base_depth = stack_depth
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
            cur_elem_id -= base_depth - stack_depth
            base_depth = stack_depth
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
            cur_elem_id -= base_depth - stack_depth
            base_depth = stack_depth
            cur_seg = []
            is_key = not is_key
        cur_seg.append((stack_depth, instr))

    if cur_seg and cur_elem_id > 0:
        output_segs.append(Segment(f"KEY {(cur_elem_id + 1) // 2}" if is_key else f"VALUE {(cur_elem_id + 1) // 2}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
    elif cur_seg:
        remaining.extend(cur_seg)

    return Segment("DICT", output_segs[::-1])


def parse_const_key_map_recursive(remaining: list[tuple[int, object]]) -> Segment:
    (post_base_depth, build_instr) = remaining.pop()
    size = build_instr.arg
    output_segs = [Segment("BUILD", [(post_base_depth, build_instr)])]

    if size == 0:
        return Segment("DICT", output_segs[::-1])

    (key_depth, key_instr) = remaining.pop()
    output_segs.append(Segment("KEY_TUPLE", [(key_depth, key_instr)]))

    base_depth = remaining[-1][0] if remaining else post_base_depth
    end_depth = base_depth - size
    cur_elem_id = size
    cur_seg = []

    while remaining:
        if base_depth == end_depth or cur_elem_id <= 0:
            break
        (stack_depth, instr) = remaining.pop()
        if stack_depth < base_depth:
            output_segs.append(Segment(f"VALUE {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
            cur_elem_id -= base_depth - stack_depth
            base_depth = stack_depth
            cur_seg = []
        cur_seg.append((stack_depth, instr))

    if cur_seg and cur_elem_id > 0:
        output_segs.append(Segment(f"VALUE {cur_elem_id}", parse_bytecode_recursive(cur_seg[::-1]), base_depth))
    elif cur_seg:
        remaining.extend(cur_seg)

    return Segment("DICT", output_segs[::-1])


def parse_map_add_recursive(remaining: list[tuple[int, object]]) -> Segment | None:
    """Parse 3.10+ dict literals with 16+ items: BUILD_MAP 0 + MAP_ADD 1 chunks merged by DICT_UPDATE 1.

    Parses on a copy and returns None without touching `remaining` if the pattern doesn't match.
    """
    trial = list(remaining)
    output_segs = []

    while trial:
        (stack_depth, instr) = trial[-1]
        if instr.opname == "DICT_UPDATE" and instr.arg == 1:
            trial.pop()
            output_segs.append(Segment("UPDATE", [(stack_depth, instr)]))
            if not trial:
                return None
            chunk_instr = trial[-1][1]
            if chunk_instr.opname == "BUILD_MAP" and chunk_instr.arg:
                output_segs.append(parse_dict_recursive(trial))
            elif chunk_instr.opname == "BUILD_CONST_KEY_MAP":
                output_segs.append(parse_const_key_map_recursive(trial))
            elif chunk_instr.opname == "MAP_ADD" and chunk_instr.arg == 1:
                chunk = parse_map_add_recursive(trial)
                if chunk is None:
                    return None
                output_segs.append(chunk)
            else:
                return None
        elif instr.opname == "MAP_ADD" and instr.arg == 1:
            trial.pop()
            output_segs.append(Segment("ADD", [(stack_depth, instr)]))
            # the value sits above the key, which sits above the dict
            value_seg, key_seg = [], []
            while trial and trial[-1][0] >= stack_depth + 2:
                value_seg.append(trial.pop())
            while trial and trial[-1][0] >= stack_depth + 1:
                key_seg.append(trial.pop())
            if not value_seg or not key_seg:
                return None
            # the key must sit directly on the dict, otherwise the stack depths are off
            if not trial or trial[-1][0] != stack_depth or trial[-1][1].opname not in ("MAP_ADD", "BUILD_MAP"):
                return None
            output_segs.append(Segment("VALUE", parse_bytecode_recursive(value_seg[::-1]), stack_depth + 2))
            output_segs.append(Segment("KEY", parse_bytecode_recursive(key_seg[::-1]), stack_depth + 1))
        elif instr.opname == "BUILD_MAP" and instr.arg == 0 and output_segs:
            # the compiler emits chunks of 16 or 17 pairs, anything else is a partial chunk
            if sum(seg.tag == "ADD" for seg in output_segs) not in (16, 17):
                return None
            trial.pop()
            output_segs.append(Segment("BUILD", [(stack_depth, instr)]))
            remaining[:] = trial
            return Segment("DICT", output_segs[::-1])
        else:
            return None
    return None


def parse_bytecode_recursive(remaining: list[tuple[int, object]]) -> list[Segment]:
    output_segs = []
    cur_seg = []
    # after a failed map_add parse, a retry from a later MAP_ADD could match a partial dict
    map_add_failed = False

    while remaining:
        (stack_depth, instr) = remaining[-1]
        if instr.arg == 1 and (instr.opname == "DICT_UPDATE" or instr.opname == "MAP_ADD" and not map_add_failed) and (dict_seg := parse_map_add_recursive(remaining)) is not None:
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            output_segs.append(dict_seg)
        elif instr.opname == "BUILD_MAP":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            dict_seg = parse_dict_recursive(remaining)
            output_segs.append(dict_seg)
        elif instr.opname == "BUILD_CONST_KEY_MAP":
            if cur_seg: output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))
            cur_seg = []
            dict_seg = parse_const_key_map_recursive(remaining)
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
            if instr.opname == "MAP_ADD" and instr.arg == 1:
                map_add_failed = True
            remaining.pop()
            cur_seg.append((stack_depth, instr))

    if cur_seg:
        output_segs.append(Segment("UNKNOWN", cur_seg[::-1]))

    return output_segs[::-1]