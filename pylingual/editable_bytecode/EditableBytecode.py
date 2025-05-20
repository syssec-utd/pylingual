import copy as copy_module
import logging
import pprint
import itertools
from collections import defaultdict
from typing import Any, Optional

from xdis import Bytecode, iscode
from xdis.cross_dis import instruction_size, op_has_argument
from xdis.bytecode import parse_exception_table, _ExceptionTableEntry

from pylingual.utils.version import PythonVersion

from .Instruction import Inst
from .utils import codeobj_replace, comprehension_names, unwrap
from .control_flow_graph import bytecode_to_control_flow_graph

from typing import Callable


class EditableBytecode:
    """
    An editable representation of Pythonic bytecode. Many values in it, including its instructions, may be incorrect
    until the final "bake," when it's converted back into raw bytecode. However, it supports arbitrary accessing,
    insertion, deletion, and modification of instructions. It also annotates instructions and provides extra information
    regarding the control flow they describe.

    Baking functions: to_code() (EditableBytecode -> code object)
                      to_bytecode() (EditableBytecode -> co_code [bytes])
    """

    def __init__(
        self,
        codeobj,
        opcode,
        version,
        name_prefix: Optional[str] = None,
        parent=None,
    ):
        self.codeobj = codeobj
        self.opcode = opcode
        self.version = PythonVersion(version)
        self.parent = parent

        self.co_consts = unwrap(list(codeobj.co_consts))
        self.co_names = unwrap(list(codeobj.co_names))
        self.co_varnames = unwrap(list(codeobj.co_varnames))

        self.name_prefix = unwrap(name_prefix)
        self.name = unwrap(codeobj.co_name) if name_prefix is None else unwrap(name_prefix) + "." + unwrap(codeobj.co_name)

        self._edited = False

        self.instructions = [Inst.from_instruction(self, inst) for inst in Bytecode(self.codeobj, self.opcode)]

        self.offsets = {inst.offset: inst for inst in self.instructions}
        jump_targets = [inst.argval for inst in self.instructions if inst.is_jump]
        for inst in self.instructions:
            inst.is_jump_target = inst.offset in jump_targets

        # named exception table is a named tuple of the exception entries.
        # should be defined when an exception_table exists for a codeobj in python versions >= (3,11)
        self.named_exception_table = None
        if hasattr(codeobj, "co_exceptiontable"):
            self.named_exception_table = parse_exception_table(codeobj.co_exceptiontable)

        # maps starting offsets to ending offsets and target offsets
        self.exception_table = {}
        # maps ending offsets to the cause of the entry (i.e. with, finally, or except)
        self.end_table = {}

        # check for globals and nonlocals
        self.globals = set()
        self.nonlocals = set()
        for inst in self.instructions:
            if inst.opname == "STORE_GLOBAL":
                self.globals.add(inst.argval)
            elif inst.opname == "STORE_DEREF":
                self.nonlocals.add(inst.argval)

        if self.version >= (3, 11):
            self.fix_format_string_lno()

        # Prepare "deep analysis" structures - cycle detection and annotation
        self._preprocess_jumps()

        # make function argvals in python 3.13 are determined by a subsequent bytecode instruction
        if self.version >= (3, 13):
            self.fix_make_function_argval()

        low_information_instruction_blacklist = ["RESUME", "EXTENDED_ARG", "CACHE", "PRECALL", "MAKE_CELL"]
        self.remove_instructions({inst for inst in self.instructions if inst.opname in low_information_instruction_blacklist})

        # updates attribute of instructions that contains information about the exception table
        self._add_inst_exception_attrs()

        # Represents subsidiary EditableBytecode objects
        self.child_bytecodes = []
        self.bytecode_lookup = {}

        # Initialize recursive structure
        for i, const in enumerate(self.co_consts):
            if iscode(const):
                self.co_consts[i] = EditableBytecode(const, opcode, self.version, name_prefix=self.name, parent=self)
                self.child_bytecodes.append(self.co_consts[i])  # Keeps it in order
                self.bytecode_lookup[const.co_name] = self.co_consts[i]

    def fix_make_function_argval(self):
        """In Python 3.13 the argval for MAKE_FUNCTION is determined by an optional subsequent SET_FUNCTION_ATTRIBUTE instruction"""

        for inst, next_inst in itertools.pairwise(self.instructions):
            if inst.opname == "MAKE_FUNCTION":
                if next_inst.opname == "SET_FUNCTION_ATTRIBUTE":
                    inst.argval = next_inst.argval
                else:
                    inst.argval = 0

    def get_recursive_length(self):
        """Returns the recursive length of this bytecode and all its descendents"""
        return len(self) + sum(bytecode.get_recursive_length() for bytecode in self.child_bytecodes)

    #
    # INTERNAL PROCESSING
    #
    def _preprocess_jumps(self):
        """Preprocesses jumps by setting the instruction's "target" attribute to the Inst object rather than the numeric
        offset. O(N^2)."""
        for inst in self.instructions:
            target = self.get_jump_target_offset(inst)

            if target is not None:
                try:
                    inst._target = self.get_by_offset(target)
                except KeyError:
                    raise ValueError(f"Found invalid target when preprocessing jumps: offset {target} for instruction {inst}")

    def regenerate(self):
        """Regenerates correct offsets for the instruction list and resets the _edited field. This is called
        automatically, but calling it externally should do no harm. O(N)."""
        if not self._edited:
            return

        self.offsets = {}
        offset = 0
        for inst in self.instructions:
            inst.original_offset = offset
            self.offsets[offset] = inst

            offset += inst.real_size

        self._edited = False

    def create_arg_inst(self, opname: str, arg, offset: int = -1):
        opcode = getattr(self.opcode, opname)
        return Inst(self, opname, opcode, None, instruction_size(opcode, self.opcode), arg, arg, repr(arg), True, offset, None, False, False)

    def _bake_jumps(self, add_extended=False):
        """
        Bakes the correct jump target address into each jump's "arg" attribute and ensures the number of EXTENDED_ARGs preceeding it is
        sufficient. This is automatically called by to_bytecode. O(N^2).
        """

        while True:
            len_before = len(self)
            changed = False

            i = 0
            while i < len(self):
                instruction = self.instructions[i]

                if instruction.has_arg:
                    if instruction.is_jump:
                        # ensure that we jump to the start of the preceeding EXTENDED_ARG chain
                        current_jump_target_index = self.instructions.index(instruction.target)
                        for prev_instruction in self.instructions[current_jump_target_index - 1 :: -1]:
                            if prev_instruction.opcode == self.opcode.EXTENDED_ARG:
                                instruction.target = prev_instruction
                                changed = True
                            else:
                                # we have reached the end of the EXTENDED_ARG chain
                                break

                        if instruction.is_rel_jump:
                            instruction.arg = instruction.target.offset - instruction.offset - instruction.real_size
                            if self.version >= (3, 10):
                                instruction.arg = int(instruction.arg / 2)
                            instruction.argval = instruction.target.offset
                        elif instruction.is_abs_jump:
                            if self.version >= (3, 10):
                                instruction.arg = int(instruction.target.offset / 2)
                                instruction.argval = instruction.target.offset
                            else:
                                instruction.arg = instruction.argval = instruction.target.offset
                    if add_extended:
                        # count the number of necessary preceeding EXTENDED_ARG instructions
                        n_extendeds_needed = (instruction.arg > 0xFF) + (instruction.arg > 0xFFFF) + (instruction.arg > 0xFFFFFF)

                        # count the number of preceding EXTENDED_ARG instructions present in the bytecode
                        n_extendeds_found = 0
                        for current_instruction in self.instructions[i - 1 :: -1]:
                            if current_instruction.opcode == self.opcode.EXTENDED_ARG:
                                n_extendeds_found += 1
                            else:
                                break

                        if n_extendeds_found > 3:
                            raise ValueError("Incorrect bytecode -- more than 3 extended args found before instruction " + repr(instruction))

                        if instruction.arg > 0xFFFFFFFF:
                            raise ValueError("Incorrect bytecode -- more than 3 extended args needed for instruction" + repr(instruction))

                        new_extendeds = [self.create_arg_inst("EXTENDED_ARG", 0) for _ in range(n_extendeds_needed - n_extendeds_found)]

                        if new_extendeds:
                            self[i:i] = new_extendeds
                            i += len(new_extendeds)

                        n_extendeds = max([n_extendeds_found, n_extendeds_needed])
                        for j in range(n_extendeds):
                            self[i - j - 1].arg = ((0xFF << ((j + 1) * 8)) & instruction.arg) >> ((j + 1) * 8)

                        instruction.has_extended_arg = True

                i += 1

            if len(self) == len_before and not changed:
                break

        self.regenerate()

    ## INSTRUCTION LOOKUP

    def get_offset(self, instruction):
        """Gets the real, current offset of the instruction. O(N)."""
        self.regenerate()
        return instruction.original_offset  # Prevent theoretically-impossible infinite loops

    def get_jump_target_offset(self, instruction):
        """Returns the target initial offset of a jump instruction, or None if the instruction is not a jump. O(1)."""
        if instruction.is_abs_jump:
            # duct taping; arg is incorrect in 310
            return instruction.argval

        elif instruction.is_rel_jump:
            # duct taping; arg is incorrect in 310
            return instruction.argval

        return None

    def get_by_offset(self, offset):
        """Finds the instruction by its offset. O(N)."""
        self.regenerate()
        return self.offsets[offset]

    def _get_instruction_after(self, instruction):
        """Gets the instruction directly following the specified instruction, or None if it's at the end of the bytecode. O(N)."""
        next_offset = instruction.offset + instruction.real_size

        try:
            return self.get_by_offset(next_offset)
        except KeyError:
            return None

    def resolve_namespace(self, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        # true dunder methods (e.g., __init__, __myfunc__) don't get namespaced
        if value.endswith("__"):
            return value

        # try namespaces all the way up the tree
        def namespace_generator():
            current = self
            yield f"_{current.codeobj.co_name.lstrip('_')}"
            while current.parent:
                current = current.parent
                yield f"_{current.codeobj.co_name.lstrip('_')}"

        for namespace in namespace_generator():
            if value.startswith(f"{namespace}__"):
                return value[len(namespace) :]

        return value

    ## SUBSIDIARY OBJECTS

    def iter_bytecodes(self):
        """Iterates through all EditableBytecode objects in the recursive object."""

        yield self

        for bytecode in self.child_bytecodes:
            for bc in bytecode.iter_bytecodes():
                yield bc

    def copy(self):
        """Returns a copy of the current bytecode object, as it stands."""
        try:
            copy = EditableBytecode(
                self.to_code(),
                self.opcode,
                self.version,
                self.name_prefix,
                False,
            )
        except IndexError:
            # A sketchy workaround for what seems to be a strange bug with loading saved code objects
            copy = copy_module.copy(self)
            copy._edited = True

            instructions = [copy_module.copy(inst) for inst in copy.instructions]
            for inst in instructions:
                if inst.is_jump:
                    inst.target = instructions[copy.instructions.index(inst.target)]
            copy.instructions = instructions

            copy.child_bytecodes = []
            for const, i in enumerate(copy.co_consts):
                if isinstance(const, EditableBytecode):
                    new = const.copy()
                    new.parent = copy

                    copy.co_consts[i] = new
                    copy.bytecode_lookup[const.codeobj.co_name] = new
                    copy.child_bytecodes.append(new)

            copy.regenerate()

        return copy

    ## BYTECODE PREPARATION

    def _gen_lines(self, line_start=None):
        """Generates a line number table (co_lines) from the current instructions."""
        lines_table = []
        offset = 0
        last_line = line_start or getattr(self.codeobj, "co_firstlineno", None)

        for instruction in self:
            if instruction.starts_line:
                if offset:
                    if last_line is None:
                        lines_table.append(offset)
                        lines_table.append(-128)
                    else:
                        line_delta = instruction.starts_line - last_line

                        while line_delta > 127:
                            lines_table.append(0)
                            lines_table.append(127)
                            line_delta -= 127

                        while line_delta < -127:
                            lines_table.append(0)
                            lines_table.append(-127)
                            line_delta += 127

                        lines_table.append(offset)
                        lines_table.append(line_delta)

                last_line = instruction.starts_line

            offset += instruction.real_size

        return bytes(lines_table)

    def to_bytecode(self):
        """Converts the instruction list into valid bytecode, to be used with co_code. This was partially taken from the incomplete
        list2bytecode function in xdis. O(N)."""
        self._bake_jumps()

        bc = []
        for instruction in self:
            bc.extend([instruction.opcode, (instruction.arg & 0xFF) if instruction.arg is not None else 0])

        return bytes(bc)

    def to_code(self, no_lnotab=False):
        """Returns a fully-functioning 'code' or xdis code object from this edited bytecode."""

        # Here, we hotfix the potentially-edited EditableBytecode objects within this one's constant
        # array. This used to be processed by recursive_fix, but it makes more sense to have the
        # EditableBytecode objects do it directly.
        co_consts = tuple((const.to_code(no_lnotab=no_lnotab) if isinstance(const, EditableBytecode) else const) for const in self.co_consts)

        replacement_args = {
            "co_code": self.to_bytecode(),
            "co_consts": tuple(co_consts),
            "co_names": tuple(self.co_names),
            "co_varnames": tuple(self.co_varnames),
        }

        # co_lnotab deprecated in python >= 3.10
        if self.version < (3, 10):
            replacement_args.update({"co_lnotab": b"\x00\x01" if no_lnotab else self._gen_lines()})

        return codeobj_replace(self.codeobj, **replacement_args)

    ### INSTRUMENTATION FUNCTIONS

    def apply_patches(self, patch_functions: list[Callable[["EditableBytecode"], None]]) -> None:
        for patch in patch_functions:
            for bc in self.iter_bytecodes():
                patch(bc)

    def _change_jump_targets(self, from_inst: Inst, to_inst: Inst):
        """Changes the targets of any instructions jumping to "from_inst" to "to_inst".
        Before:
            InstA --> InstB
        After _change_jump_targets(InstB, InstC):
            InstA --> !!InstC!!
        """
        for i, inst in enumerate(self):
            if inst.is_jump and inst.target == from_inst:
                self[i]._target = to_inst

    def collapse_unconditional_jumps(self):
        """Causes unnecessary unconditional jumps to "collapse" into a single jump."""

        unconditional_jumps = set(instruction for instruction in self if instruction.is_uncond_jump and instruction.target.is_uncond_jump)
        instructions_changed = set()

        while unconditional_jumps:
            this_layer = set(jump for jump in unconditional_jumps if jump.target not in unconditional_jumps)

            if not this_layer:
                logger = logging.getLogger("transform")
                logger.warning("Two jumps are forming an infinite loop!\n" + pprint.pformat(unconditional_jumps))
                break

            for jump in this_layer:
                jump._target = jump._target._target
                instructions_changed.add(jump)

            unconditional_jumps.difference_update(this_layer)

        return len(instructions_changed)

    def remove_unreachable_instructions(self):
        """Removes unreachable instructions from the bytecode as cleanly as possible."""

        self.regenerate()

        cfg = bytecode_to_control_flow_graph(self)
        unreachable_instructions = set(self.instructions) - set(cfg.nodes)
        return self.remove_instructions(unreachable_instructions)

    def remove_useless_jumps(self):
        """Removes jumps that just jump to the next instruction."""
        useless_jumps = {inst for inst in self if inst.is_jump and inst.target.offset == inst.offset + inst.real_size}
        return self.remove_instructions(useless_jumps)

    def shrink(self):
        """Shrinks and optimizes bytecode using various heuristics."""
        n = self.collapse_unconditional_jumps()
        n += self.remove_unreachable_instructions()
        n += self.remove_useless_jumps()

        return n

    def remove_instructions(self, to_remove):
        """Removes every instruction in the provided list *fairly* gracefully, albeit not perfectly when ambiguity is involved."""
        if len(to_remove) == 0:
            return 0

        self.regenerate()
        self._edited = True

        # store a list of all jumps to avoid repeatedly searching for them
        jumps = [inst for inst in self.instructions if inst.is_jump]

        # store an instruction-based copy of the exception table to make offset fixing easier at the end
        temp_exception_table = {self.get_by_offset(start): (self.get_by_offset(end), self.get_by_offset(target)) for start, (end, target) in self.exception_table.items()}
        temp_named_exception_table = dict()
        if self.named_exception_table:
            temp_named_exception_table = [(self.get_by_offset(e.start), self.get_by_offset(e.end), self.get_by_offset(e.target), e.depth, e.lasti) for e in self.named_exception_table]

        # propagate jump targets backwards from the end of the bytecode and remove immediately
        removed = set()
        while self.instructions[-1] in to_remove:
            # update jump targets
            new_jump_target = self.instructions[-2]
            for jump in jumps:
                if jump.target is self.instructions[-1]:
                    jump._target = new_jump_target
                    new_jump_target.is_jump_target = True

            # update exception table entries
            new_exception_target = self.instructions[-2]
            for start, (end, target) in list(temp_exception_table.items()):
                # move start back if deleted
                if start is self.instructions[-1]:
                    temp_exception_table[new_exception_target] = (end, target)
                    del temp_exception_table[start]
                    start = new_exception_target
                # move end back if deleted
                if end is self.instructions[-1]:
                    temp_exception_table[start] = (new_exception_target, target)
                    end = new_exception_target
                # move target back if deleted
                if target is self.instructions[-1]:
                    temp_exception_table[start] = (end, new_exception_target)

            # update named exception table entries
            for exception_index, (start, end, target, depth, lasti) in enumerate(list(temp_named_exception_table)):
                if start is self.instructions[-1]:
                    temp_named_exception_table[exception_index] = (new_exception_target, end, target, depth, lasti)
                    start = new_exception_target
                if end is self.instructions[-1]:
                    temp_named_exception_table[exception_index] = (start, new_exception_target, target, depth, lasti)
                    end = new_exception_target
                if target is self.instructions[-1]:
                    temp_named_exception_table[exception_index] = (start, end, new_exception_target, depth, lasti)

            removed.add(self.instructions.pop())

        for inst in sorted(to_remove, key=lambda x: x.offset):
            if inst in removed:
                continue

            next_instruction = self._get_instruction_after(inst)

            # update line starts
            if next_instruction.starts_line is None:
                next_instruction.starts_line = inst.starts_line

            # update jump targets
            for jump in jumps:
                if jump.target is inst:
                    jump._target = next_instruction
                    next_instruction.is_jump_target = True

            # update exception table entries
            new_exception_target = next_instruction
            for start, (end, target) in list(temp_exception_table.items()):
                # move start back if deleted
                if start is inst:
                    temp_exception_table[new_exception_target] = (end, target)
                    del temp_exception_table[start]
                    start = new_exception_target
                # move end back if deleted
                if end is inst:
                    temp_exception_table[start] = (new_exception_target, target)
                    end = new_exception_target
                # move target back if deleted
                if target is inst:
                    temp_exception_table[start] = (end, new_exception_target)

            # update named exception table entries
            for exception_index, (start, end, target, depth, lasti) in enumerate(list(temp_named_exception_table)):
                if start is inst:
                    temp_named_exception_table[exception_index] = (new_exception_target, end, target, depth, lasti)
                    start = new_exception_target
                if end is inst:
                    temp_named_exception_table[exception_index] = (start, new_exception_target, target, depth, lasti)
                    end = new_exception_target
                if target is inst:
                    temp_named_exception_table[exception_index] = (start, end, new_exception_target, depth, lasti)

        # Now, removing them this way will have no side effects.
        self.instructions = [inst for inst in self.instructions if inst not in to_remove]
        self._edited = True
        self.regenerate()  # recalculate offsets

        # fix jump target argval and argrepr
        for jump in jumps:
            jump.argval = jump.target.offset
            jump.argrepr = f"to {jump.argval}"

        # fix exception table offsets
        self.exception_table = {start.offset: (end.offset, target.offset) for start, (end, target) in temp_exception_table.items()}
        if temp_named_exception_table:
            self.named_exception_table = [_ExceptionTableEntry(start.offset, end.offset, target.offset, depth, lasti) for (start, end, target, depth, lasti) in temp_named_exception_table]
        self._add_inst_exception_attrs()

        self._edited = True

        return len(to_remove)

    def new_instruction(self, *args, **kwargs):
        """Creates a new instruction for use with this EditableBytecode object. This function does NOT automatically insert the instruction."""
        return Inst(self, *args, **kwargs)

    ## OTHER UTILS

    def disasm_view(self, b_iter_bytecodes: bool = True) -> str:
        """Get a multi-line disassembled view of this bytecode obj
        b_iter_bytecodes (bool) True : Iter through all bytecodes in self (child bytecodes)"""
        disview = ""
        for bytecode in self.iter_bytecodes() if b_iter_bytecodes else [self]:
            for inst in bytecode:
                if inst.starts_line:
                    disview += f"# Line {inst.starts_line}\n"
                disview += inst.get_dis_view() + "\n"
            disview += "\n"
        return disview

    def _change_line_number_everywhere(self, original_line_number, new_line_number):
        """
        Updates all instances of original_line_number in the line_starts of instructions to become new_line_number
        """
        for bc in self.iter_bytecodes():
            for inst in bc:
                if inst.starts_line == original_line_number:
                    inst.starts_line = new_line_number

    def _patch_dummy_decorator(self, dummy_decorator_name="dummy"):
        """
        Exclusively used for python <= 3,7
        Removes "@dummy_decorator_name" decorators from bytecode.
        """
        for bc in self.iter_bytecodes():
            for inst in bc.instructions:
                if inst.opname.startswith("LOAD") and inst.argval == dummy_decorator_name:
                    # target found
                    target_idx = bc.instructions.index(inst)
                    for next_inst in bc.instructions[target_idx:]:
                        if (next_inst.opname, next_inst.arg) == ("CALL_FUNCTION", 1):
                            bc.remove_instructions([next_inst])
                            break
                    self._change_line_number_everywhere(inst.starts_line, inst.starts_line + 1)
                    bc.remove_instructions([inst])
        return

    def fix_while(self, source_lines):
        for i in range(len(source_lines)):
            if source_lines[i].startswith("while ") and source_lines[i] != "while True:":
                source_lines[i] = "if" + source_lines[i][5:]
        for bc in self.iter_bytecodes():
            for inst in bc:
                if inst.opname.startswith("POP_JUMP_BACKWARD_IF_") or inst.opname.startswith("POP_JUMP_IF_") and inst.argval < inst.offset:
                    prev = bc[inst.argval // 2 - 1]
                    while prev.starts_line is None:
                        if prev.offset == 0:
                            prev = None
                            break
                        else:
                            prev = bc[prev.offset // 2 - 1]
                    if prev is not None and source_lines[prev.starts_line - 1].startswith("if "):
                        source_lines[prev.starts_line - 1] = "while" + source_lines[prev.starts_line - 1][2:]

    def fix_while12(self, source_lines):
        for i in range(len(source_lines)):
            if source_lines[i].startswith("while ") and source_lines[i] != "while True:":
                source_lines[i] = "if" + source_lines[i][5:]
        for bc in self.iter_bytecodes():
            for inst in bc:
                if inst.opname == "JUMP_BACKWARD":
                    prev = bc[inst.offset // 2 - 1]
                    if prev.opname.startswith("POP_JUMP_IF") and prev.argval == inst.offset + 2:
                        prev = bc[inst.argval // 2 - 1]
                        while prev.starts_line is None:
                            if prev.offset == 0:
                                prev = None
                                break
                            else:
                                prev = bc[prev.offset // 2 - 1]
                        if prev is not None and source_lines[prev.starts_line - 1].startswith("if "):
                            source_lines[prev.starts_line - 1] = "while" + source_lines[prev.starts_line - 1][2:]

    def fix_format_string_lno(self):
        for a in range(len(self) - 1):
            if self[a + 1].starts_line is not None:
                if self[a].opname == "LOAD_CONST" and type(self[a].argval) == str:
                    self[a].starts_line = self[a + 1].starts_line
                    self[a + 1].starts_line = None

    def make_absolute(self, offset, target):
        return [
            self.new_instruction(
                "JUMP_ABSOLUTE",
                self.opcode.JUMP_ABSOLUTE,
                "jabs",
                instruction_size(self.opcode.JUMP_ABSOLUTE, self.opcode),
                target.offset,
                target.offset,
                repr(target.offset),
                op_has_argument(self.opcode.JUMP_ABSOLUTE, self.opcode),
                offset,
                None,
                False,
                False,
                target,
            )
        ]

    def make_relative(self, offset, target):
        return [
            self.new_instruction(
                "JUMP_FORWARD",
                self.opcode.JUMP_FORWARD,
                "jrel",
                instruction_size(self.opcode.JUMP_FORWARD, self.opcode),
                target.offset - offset,
                target.offset - offset,
                repr(target.offset - offset),
                op_has_argument(self.opcode.JUMP_FORWARD, self.opcode),
                offset,
                None,
                False,
                False,
                target,
            )
        ]

    def replace_duplicated_returns10(self, source_lines):
        for bc in self.iter_bytecodes():
            offsets = defaultdict(int)
            if bc.codeobj.co_name in comprehension_names:
                continue
            for inst in bc:
                if inst.starts_line is not None:
                    offsets[inst.starts_line] = max(offsets[inst.starts_line], inst.offset)
            for inst in bc:
                if inst.starts_line is not None and inst.offset != offsets[inst.starts_line]:
                    line = source_lines[inst.starts_line - 1].strip()
                    if line == "return" or line.startswith("return "):
                        target = bc[offsets[inst.starts_line] // 2]
                        bc[inst.offset // 2] = self.make_absolute(inst.offset, target)
            bc.remove_unreachable_instructions()

    def replace_duplicated_returns12(self, source_lines):
        for bc in self.iter_bytecodes():
            offsets = defaultdict(int)
            if bc.codeobj.co_name in comprehension_names:
                continue
            for inst in bc:
                if inst.starts_line is not None:
                    offsets[inst.starts_line] = max(offsets[inst.starts_line], inst.offset)
            for inst in bc:
                if inst.starts_line is not None and inst.offset != offsets[inst.starts_line]:
                    insts = [inst]
                    i = bc[inst.offset // 2 + 1]
                    while i.starts_line is None:
                        insts.append(i)
                        i = bc[i.offset // 2 + 1]
                    if len(insts) <= 4 and insts[-1].opname in ("RETURN_VALUE", "RETURN_CONST"):
                        target = bc[offsets[inst.starts_line] // 2]
                        bc[inst.offset // 2] = self.make_relative(inst.offset, target)
            bc.remove_unreachable_instructions()

    def get_lno_insts(self, hoist_comprehensions: bool = True, previously_seen_lines: set[int] = None) -> dict[int, list[Inst]]:
        """Get a dictionary that maps line numbers to sequences of bytecodes"""
        if hoist_comprehensions and self.is_comprehension:
            return dict()

        if previously_seen_lines is None:
            previously_seen_lines = set()

        # create a dict of line num : [bytecodes composing line]
        lno_bytecodes = {}
        seen_lnos = set(previously_seen_lines)
        current_line_bytecodes = []
        current_lno = None

        for inst in self:
            if inst.starts_line is not None and inst.starts_line not in seen_lnos:
                if current_line_bytecodes:
                    lno_bytecodes.update({current_lno: current_line_bytecodes})
                    current_line_bytecodes = []
                current_lno = inst.starts_line
                seen_lnos.add(current_lno)

            current_line_bytecodes.append(inst)

            if hoist_comprehensions and inst.opname == "LOAD_CONST" and getattr(inst.argval, "co_name", None) in self.bytecode_lookup:
                child_code = self.co_consts[inst.arg]
                if child_code.is_comprehension:
                    for decendant_code in child_code.iter_bytecodes():
                        current_line_bytecodes.extend(decendant_code.instructions)

        # update final list
        if current_line_bytecodes:
            lno_bytecodes.update({current_lno: current_line_bytecodes})

        # resolve unallocated starting instructions
        if None in lno_bytecodes and len(lno_bytecodes) > 1:
            unallocated_insts = lno_bytecodes.pop(None)
            earliest_line = min(lno_bytecodes.keys())
            lno_bytecodes[earliest_line] = unallocated_insts + lno_bytecodes[earliest_line]

        return lno_bytecodes

    def _add_inst_exception_attrs(self):
        """
        Update instruction attributes to add additional context if they are entries in the exception table
        for versions >= (3,11)
        """
        if self.named_exception_table is None:
            return
        for entry in self.named_exception_table:
            self.get_by_offset(entry.start).exception_start = entry.target
            self.get_by_offset(entry.end).exception_end = True
            self.get_by_offset(entry.target).exception_target = True

    ## PROPERTIES

    @property
    def is_comprehension(self):
        return self.codeobj.co_name in comprehension_names

    @property
    def first_instruction(self):
        return self.instructions[0]

    ## OVERLOADS

    def __iter__(self):
        return self.instructions.__iter__()

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.instructions[i]

        return self.instructions[i]

    def __setitem__(self, i, value):
        if not isinstance(i, slice):
            i = slice(i, i + 1)
        insts = self.instructions[i]
        if isinstance(insts, Inst):
            insts = [insts]

        instruction_before = self[i.start - 1] if i.start is not None and i.start > 0 else None
        instruction_after = self[i.stop] if i.stop is not None and i.stop <= len(self) else None

        for j, inst in enumerate(insts):
            if isinstance(value, (list, tuple)) and len(insts) == len(value):
                self._change_jump_targets(inst, value[j])
            else:
                new_target = instruction_before or instruction_after
                if not new_target and len(value) > 0:
                    new_target = value[0]
                elif len(value) == 0:
                    pass  # They should have used __del__

                if new_target:
                    self._change_jump_targets(inst, new_target)

        self.instructions[i] = value
        self._edited = True

    def __delitem__(self, i):
        if not isinstance(i, slice):
            i = slice(i, i + 1)
        insts = self.instructions[i]
        if isinstance(insts, Inst):
            insts = [insts]

        instruction_before = self[i.start - 1] if i.start is not None and i.start > 0 else None
        instruction_after = self[i.stop] if i.stop is not None and i.stop <= len(self) else None

        for inst in insts:
            new_target = instruction_before or instruction_after

            if new_target:
                self._change_jump_targets(inst, new_target)

        del self.instructions[i]
        self._edited = True

    def __hasitem__(self, value):
        return value in self.instructions

    def __len__(self):
        return len(self.instructions)

    def __str__(self):
        name = "" if self.name is None else self.name + ","
        return self.__class__.__name__ + "<" + name + "edited=" + repr(self._edited) + ">" + pprint.pformat(self.instructions)

    def __repr__(self):
        name = "" if self.name is None else self.name + ","
        return self.__class__.__name__ + "<" + name + "edited=" + repr(self._edited) + ">" + f"[{len(self.instructions)} instructions,{len(self.child_bytecodes)} code objects]"
