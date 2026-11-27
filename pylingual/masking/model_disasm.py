from __future__ import annotations

import ast
import math
import pathlib
import re
from copy import deepcopy
from typing import TYPE_CHECKING, Pattern

from xdis import iscode

from pylingual.editable_bytecode.utils import comprehension_names
from pylingual.utils.use_escape_sequences import use_escape_sequences
from pylingual.utils.version import PythonVersion


if TYPE_CHECKING:
    from pylingual.editable_bytecode import EditableBytecode

from pylingual.masking.ast_masker import RewriteMasks, custom_unparse
from pylingual.masking.global_masker import Masker

mask_regex = re.compile(r"(?<=<mask_)(?:0|[1-9][0-9]*)(?=>)", re.ASCII)
# Full-token form used when rewriting model output back into the global mask namespace
mask_token_regex = re.compile(r"<mask_(0|[1-9][0-9]*)>", re.ASCII)
# Sentinels for masks the model invented that were never in the bytecode; they can never
# collide with a global_tab key because a mask token always carries a leading "<mask_".
OOB_MASK_PREFIX = "<oob_mask_"


def has_oob_masks(text: str) -> bool:
    """Whether text contains an out-of-bounds mask substituted by restore_masks."""
    return OOB_MASK_PREFIX in text


def create_global_masker(bytecode: EditableBytecode) -> Masker:
    """Creates four flat global tables of names, locals, consts, and freevars in given Bytecode for use with improved model view
    Global Tables map local code obj tables: name, varname, const, and freevar to the global table
    - For additional model context, values that match across the name and const tab will have their matching
        partner in the other table appended to their token. ex: <const_x>=<name_y>
    Access table in global dict via keywork of table optype"""

    global_masker = Masker()
    global_tab = global_masker.global_tab
    global_idx = 0

    future_flag = 0x1000000 if bytecode.version > (3, 7) else 0x100000
    global_masker.future_annotations = bool(bytecode.codeobj.co_flags & future_flag)
    global_masker.version = bytecode.version

    def intern(value):
        """Add a value to the global table without ever overwriting an existing mask entry."""
        nonlocal global_idx
        # Don't needlessly increment the global_idx
        if value in global_tab:
            return
        global_tab[value] = f"<mask_{global_idx}>"
        global_idx += 1

    for bc in bytecode.iter_bytecodes():
        bc_co = bc.to_code(no_lnotab=True)
        preprocessed = [inst.argval for inst in bc.instructions if getattr(inst, "preprocessed_container", False)]

        # create consts
        # Code objects are immutable and must never enter the global table, so don't copy them either
        consts = [value if iscode(value) else deepcopy(value) for value in (getattr(const, "codeobj", const) for const in bc.co_consts)]

        # add LOAD_SMALL_INT values to consts (3.14+)
        if bc.version >= (3, 14):
            for inst in bc.instructions:
                if inst.opname == "LOAD_SMALL_INT":  # duplicate consts will be filtered out later
                    consts.append(inst.argval)

        while consts:
            const = consts.pop(0)
            # Don't mask None
            if const is None:
                continue
            # Code objects are never mask keys; mask the resolved name they define instead.
            # Comprehension code objects keep their literal name in <codeobj:...> form.
            if iscode(const):
                if const.co_name not in comprehension_names:
                    intern(bc.resolve_namespace(const.co_name))
                continue
            if type(const) in (list, tuple, frozenset, set) and not any(type(const) is type(value) and const == value for value in preprocessed):
                if const in global_tab:
                    continue
                consts.extend(const)
            elif type(const) is slice:
                if const in global_tab:
                    continue
                # decompose slice constants for 3.14+
                consts.extend([const.start, const.stop, const.step])
            else:
                intern(bc.resolve_namespace(const))

        # create names
        for name in bc.co_names:
            if isinstance(name, tuple):
                for n in name:
                    intern(bc.resolve_namespace(n))
            else:
                intern(bc.resolve_namespace(name))

        for free in bc.codeobj.co_freevars:
            intern(free)

        if bc.version >= (3, 11):
            for cell in bc.codeobj.co_cellvars:
                intern(cell)

        for local in bc.co_varnames:
            if isinstance(local, tuple):
                for local_item in local:
                    intern(bc.resolve_namespace(local_item))
            else:
                intern(bc.resolve_namespace(local))

        # keep the first mask assigned to a code object's name, never overwrite it
        intern(bc_co.co_name)

    return global_masker


def mask_source(file_path: pathlib.Path, masker: Masker, python_version: PythonVersion) -> str:
    """Replace source strings with tokens from keys in global_tab,
    masks source and provides offsets incured by multiline string replacements"""
    text = file_path.read_text()
    tree = ast.parse(text, feature_version=python_version.as_tuple())

    line_offsets = dict()
    tree = RewriteMasks(masker, line_offsets, python_version).generic_visit(tree)

    source_text = custom_unparse(tree, masker)
    source_lines = source_text.splitlines()

    re_added_lines = 0
    for line_offset, lines_to_add in line_offsets.items():
        insertion_target = line_offset + re_added_lines
        source_lines[insertion_target:insertion_target] = [""] * lines_to_add

    return "\n".join(source_lines)


def restore_masked_source(file_path: pathlib.Path, masker: Masker, python_version: PythonVersion) -> str:
    """Creates a large regex of all the tokens and their respective values
    Replaces everything in file text in one pass."""
    return restore_masked_source_text(file_path.read_text(), masker, python_version)


def format_source_replacement(mask_value: str) -> str:
    if type(mask_value) is slice:
        start = "" if mask_value.start is None else format_source_replacement(mask_value.start)
        stop = "" if mask_value.stop is None else format_source_replacement(mask_value.stop)
        if mask_value.step is None:
            return f"{start}:{stop}"
        step = format_source_replacement(mask_value.step)
        return f"{start}:{stop}:{step}"
    if type(mask_value) in (list, tuple) and any(type(value) is slice for value in mask_value):
        return ", ".join(format_source_replacement(value) for value in mask_value)
    if type(mask_value) is tuple and any(value is ... for value in mask_value):
        # a folded subscript tuple containing Ellipsis must restore as comma-joined
        # subscript syntax (x[[0], ...]), not a parenthesized repr (x[([0], Ellipsis)])
        # which would recompile to a LOAD_NAME Ellipsis instead of LOAD_CONST Ellipsis
        return ", ".join(format_source_replacement(value) for value in mask_value)
    if mask_value is ...:
        return "..."
    if isinstance(mask_value, float) and math.isinf(mask_value):  # infinity literals
        return "(-9e999)" if mask_value < 0 else "9e999"
    if type(mask_value) in (int, float) and mask_value < 0:
        return f"({mask_value})"
    if type(mask_value) != str:
        return str(mask_value)
    return mask_value


re_rel_pattern = re.compile(r"^(\s*)(import|from)\s*(\d+)(.*)", re.MULTILINE)
string_prefix_chars = "rRbBuUfFtT"


CODE, STRING_LITERAL, FSTRING_LITERAL = 0, 1, 2


def string_literal_positions(line: str) -> list[int]:
    """Classifies each character of a source line as CODE, STRING_LITERAL, or FSTRING_LITERAL (literal text of an f-string).
    f-string replacement fields are code, but their format specs and nested strings are literal text.
    Tolerates unterminated strings and masks, since the line is model output."""
    in_literal = [CODE] * len(line)

    def scan_code(i: int, closers: str) -> int:
        # scan code until an unmatched character in closers (used for f-string replacement fields)
        depth = 0
        while i < len(line):
            c = line[i]
            if c in "'\"":
                j = i
                while j > 0 and line[j - 1] in string_prefix_chars:
                    j -= 1
                # a prefix only counts if it doesn't continue a name like `rb_value'`
                prefix = line[j:i] if j == 0 or not (line[j - 1].isalnum() or line[j - 1] == "_") else ""
                i = scan_string(i, prefix.lower())
                continue
            if c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0 and c in closers:
                    return i
                depth = max(depth - 1, 0)
            elif c in closers and depth == 0:
                return i
            i += 1
        return i

    def scan_string(i: int, prefix: str) -> int:
        quote = line[i : i + 3] if line[i : i + 3] in ("'''", '"""') else line[i]
        i += len(quote)
        raw = "r" in prefix
        formatted = "f" in prefix or "t" in prefix
        kind = FSTRING_LITERAL if formatted else STRING_LITERAL
        while i < len(line):
            if line.startswith(quote, i):
                return i + len(quote)
            c = line[i]
            if c == "\\" and not raw:
                in_literal[i : i + 2] = [kind] * len(in_literal[i : i + 2])
                i += 2
                continue
            if formatted and c in "{}":
                if line[i : i + 2] in ("{{", "}}"):
                    in_literal[i : i + 2] = [kind, kind]
                    i += 2
                    continue
                if c == "{":
                    i = scan_replacement_field(i + 1)
                    continue
            in_literal[i] = kind
            i += 1
        return i

    def scan_replacement_field(i: int) -> int:
        i = scan_code(i, ":}")
        if i < len(line) and line[i] == ":":
            # format spec is literal text that may hold nested replacement fields
            i += 1
            while i < len(line) and line[i] != "}":
                if line[i] == "{":
                    i = scan_replacement_field(i + 1)
                    continue
                in_literal[i] = FSTRING_LITERAL
                i += 1
        return i + 1  # skip the closing brace

    scan_code(0, "")
    return in_literal


def unmask(source_line: str, replacements: dict, container_masks: set[str], re_pattern: Pattern[str], string_masks: set[str] = None):
    in_literal = None

    def m(match):
        nonlocal in_literal
        r = replacements[match.group()]
        if match.group() in container_masks:
            return r
        # add parenthesis to integers if they are being accessed
        if r.isdigit() and match.end() < len(match.string) and match.string[match.end()] == ".":
            return f"({r})"
        # only string values need escaping, and only when they are spliced into a string literal
        if string_masks is not None and match.group() not in string_masks:
            return r
        if in_literal is None:
            in_literal = string_literal_positions(match.string)
        context = in_literal[match.start()]
        if context == CODE:
            return r
        r = use_escape_sequences(r)
        if context == FSTRING_LITERAL:
            r = r.replace("{", "{{").replace("}", "}}")
        return r

    text = re_pattern.sub(m, source_line)
    return re_rel_pattern.sub(lambda match: f"{match.group(1)}{match.group(2)} {'.' * int(match.group(3))}{match.group(4)}", text)


def fix_jump_targets(disasm: str) -> str:
    jump_target_re = r"to (\d+) ([\^v]~>)"
    jump_target_map = {target: f"TARGET_{ind}" for ind, target in enumerate(sorted(set(match.group(1) for match in re.finditer(jump_target_re, disasm))))}

    # remove external jump entry points
    incoming_jump_re = r"([\^v]~>) (\d+) "
    result = re.sub(incoming_jump_re, lambda match: f"{match.group(1)} {jump_target_map[match.group(2)]} " if match.group(2) in jump_target_map else f"{match.group(1)} ", disasm)

    # only enforce order on external jumps
    result = re.sub(jump_target_re, lambda match: f"to {jump_target_map[match.group(1)]} {match.group(2)}", result)
    return result


def restore_masked_source_text(lines: list[str], masker: Masker) -> list[str]:
    """Creates a large regex of all the tokens and their respective values
    Replaces everything in file text in one pass."""
    replacements = {}
    container_masks = set()
    string_masks = set()
    for value, mask in masker.global_tab.items():
        # code objects are not source values and must never be spliced into the source
        if iscode(getattr(value, "codeobj", value)):
            continue
        replacement = format_source_replacement(value)
        if isinstance(value, (list, tuple, frozenset, set, dict)):
            # The model sometimes quotes an atomic container mask as though it were a string.
            # Consume those wrapper quotes rather than escaping the container's contents.
            replacements[re.escape(f"'{mask}'")] = replacement
            replacements[re.escape(f'"{mask}"')] = replacement
            container_masks.update((f"'{mask}'", f'"{mask}"', mask))
        elif isinstance(value, str):
            string_masks.add(mask)
        replacements[re.escape(mask)] = replacement
    # an empty pattern matches between every character, so only compile one when we have replacements
    if not replacements:
        return list(lines)
    re_pattern = re.compile("|".join(replacements.keys()))
    return [unmask(x, replacements, container_masks, re_pattern, string_masks) for x in lines]


# replace mask values to start at 0 and count up
def normalize_masks(statement: str) -> tuple[str, list[str]]:
    masks = mask_regex.findall(statement)
    mask_order = [x for i, x in enumerate(masks) if masks.index(x) == i]
    return mask_regex.sub(lambda x: str(mask_order.index(x.group(0))), statement), mask_order


# reverts masks to their original value
def restore_masks(translation: str, mask_order: list[str]):
    def restore_mask(match):
        i = int(match.group(1))
        # sometimes model adds random masks that did not appear in bytecode,
        # so we have to check if mask is in bounds
        if 0 <= i < len(mask_order):
            return f"<mask_{mask_order[i]}>"
        # an out-of-bounds mask must never fall back onto an unrelated global mask,
        # so rewrite it as a sentinel that cannot match any global_tab key
        return f"{OOB_MASK_PREFIX}{i}>"

    return mask_token_regex.sub(restore_mask, translation)
