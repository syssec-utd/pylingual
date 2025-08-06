# seperate import for type checking to prevent circular reference with EditableBytecode
from typing import TYPE_CHECKING, Optional

from xdis import iscode
from xdis.cross_dis import instruction_size, xstack_effect
from .utils import unwrap

if TYPE_CHECKING:
    from typing import Any
    from .EditableBytecode import EditableBytecode


class Inst:
    """This is a more object-oriented, editable version of the xdis Instruction class. For use with EditableBytecode."""

    def __init__(
        self,
        bytecode: "EditableBytecode",
        opname: str,
        opcode,
        optype: str,
        inst_size: int,
        arg: int,
        argval: "Any",
        argrepr: str,
        has_arg: bool,
        offset: int,
        starts_line: int,
        is_jump_target: bool,
        has_extended_arg: bool,
        target: Optional["Inst"] = None,
    ):
        self.bytecode = bytecode

        self.opname = opname
        self.opcode = opcode
        self.optype = optype
        self.inst_size = inst_size
        self.arg = unwrap(arg)
        self.argval = unwrap(argval)
        self.argrepr = unwrap(argrepr)
        self.has_arg = has_arg
        self.original_offset = offset  # We typically calculate the offset on-the-fly and cache it as necessary
        self.starts_line = starts_line
        self.is_jump_target = is_jump_target
        self.has_extended_arg = has_extended_arg
        self._target = target  # Will be set by the containing EditableBytecode object

        # exception table information used for model view, values are assigned during init of parent bytecode
        # only set in versions >= 3,11
        self.exception_start: int | bool = False  # will either be false
        self.exception_end = False
        self.exception_target = False

        # dependency graph for obfuscation
        self.deps = []
        self.reqs = []
        self.stack = []
        self.pop = []

    @property
    def offset(self):
        return self.bytecode.get_offset(self)

    @property
    def real_size(self):
        return instruction_size(self.opcode, self.bytecode.opcode)

    @property
    def is_jump(self):
        return self.optype in ("jabs", "jrel") or self.is_cond_jump

    @property
    def is_abs_jump(self):
        return self.optype == "jabs"

    @property
    def is_rel_jump(self):
        return self.optype == "jrel"

    @property
    def is_cond_jump(self):
        """
        It's technically inaccurate that SETUP_WITH and SETUP_FINALLY are jumps, but they cause jumps in subsequent
        instructions, so this theoretically preserves the control flow

        @return:
        @rtype:
        """

        return self.opname in (
            "POP_JUMP_IF_FALSE",
            "POP_JUMP_IF_TRUE",
            "POP_JUMP_FORWARD_IF_FALSE",
            "POP_JUMP_FORWARD_IF_TRUE",
            "POP_JUMP_BACKWARD_IF_FALSE",
            "POP_JUMP_BACKWARD_IF_TRUE",
            "JUMP_IF_TRUE_OR_POP",
            "JUMP_IF_FALSE_OR_POP",
            "JUMP_IF_TRUE",
            "JUMP_IF_FALSE",
            "FOR_ITER",
            "POP_JUMP_IF_NONE",
            "POP_JUMP_IF_NOT_NONE",
            "POP_JUMP_BACKWARD_IF_NONE",
            "POP_JUMP_BACKWARD_IF_NOT_NONE",
            "POP_JUMP_FORWARD_IF_NONE",
            "POP_JUMP_FORWARD_IF_NOT_NONE",
            "JUMP_IF_NOT_EXC_MATCH",
            "SETUP_WITH",
            "SETUP_FINALLY",
            "SEND",
        )

    @property
    def is_uncond_jump(self):
        """
        @return:
        @rtype:
        """

        return self.opcode in self.bytecode.opcode.JUMP_UNCONDITIONAL

    @property
    def target(self):
        if not self.is_jump:
            raise AttributeError("Only jump instructions have target attributes, not " + repr(self))
        return self._target

    @target.setter
    def target(self, value):
        if not self.is_jump:
            raise AttributeError("Only jump instructions have target attributes, not " + repr(self))
        self._target = value

    def add_reqs(self, *reqs):
        for r in reqs:
            if isinstance(r, tuple):
                r = r[0]
            if isinstance(r, Inst):
                r.deps.append(self)
            self.reqs.append(r)

    @property
    def next_instructions(self):
        """Returns the instruction(s) that follow this one, including a jump target (if any)."""
        next = []
        if self.is_jump:
            next.append(self.target)
        if not self.is_uncond_jump and self.opname not in ("RETURN_VALUE", "RAISE_VARARGS", "RETURN_CONST"):
            inst_after = self.bytecode._get_instruction_after(self)
            if inst_after:
                next.append(inst_after)
        if self.offset in self.bytecode.exception_table:
            target_offset = self.bytecode.exception_table[self.offset][1]
            next.append(self.bytecode[target_offset // 2])

        return next

    @property
    def next_instructions_basic(self):
        """Returns the next instruction(s), IGNORING control flow from exceptions"""

        if self.opname in ("SETUP_WITH", "SETUP_FINALLY"):
            inst_after = self.bytecode._get_instruction_after(self)
            return [inst_after] if inst_after else []

        next = []
        if self.is_jump:
            next.append(self.target)
        if not self.is_uncond_jump:
            inst_after = self.bytecode._get_instruction_after(self)
            if inst_after:
                next.append(inst_after)

        return next

    def get_next_instructions(self, follow_uncond_jumps: bool = False):
        """
        A slightly more robust version of the property "next_instructions" that allows for following unconditional
        jumps.

        @param follow_uncond_jumps:
        @type follow_uncond_jumps:
        @return:
        @rtype:
        """
        next_instructions = set(self.next_instructions)
        last_next = next_instructions

        while follow_uncond_jumps:
            new_next = set()

            for inst in last_next:
                if (inst.is_jump and not inst.is_cond_jump) or inst.opcode == self.bytecode.opcode.EXTENDED_ARG:
                    new_next.update(inst.next_instructions)

            before = len(next_instructions)
            next_instructions.update(new_next)

            if len(next_instructions) > before:
                last_next = new_next
            else:
                break

        return next_instructions

    def get_stack_effect(self, jump: bool = True):
        """Returns the "effect" this instruction will have on the stack. May occasionally return None?"""
        return xstack_effect(self.opcode, self.bytecode.opcode, oparg=self.arg, jump=jump)

    ### DIS VIEWS ###

    @property
    def jumped_to_from_insts(self) -> list["Inst"]:
        if not self.is_jump_target:
            return []

        return [inst for inst in self.bytecode if hasattr(inst, "target") and self is inst.target]

    def get_dis_view(self) -> str:
        """Get a dissassembled view of the instruction, similar to that of dis output"""
        if iscode(self.argval):
            argrepr = f"code object {self.argval.co_name}"
        else:
            argrepr = self.argrepr
        return f"{self.offset} {self.opname}{' ' + str(self.arg) if self.has_arg else ''}{' (' + argrepr + ')' if argrepr else ''}"

    #####

    def __repr__(self):
        attr_list = (
            "opname",
            "opcode",
            "optype",
            "real_size",
            "arg",
            "argval",
            "argrepr",
            "has_arg",
            "offset",
            "starts_line",
            "is_jump_target",
            "has_extended_arg",
        )

        return self.__class__.__name__ + "(" + ", ".join((attr + "=" + repr(getattr(self, attr))) for attr in attr_list) + ")"

    @classmethod
    def from_instruction(self, bytecode, inst):
        """Creates an Inst from an xdis Instruction object"""
        return Inst(
            bytecode,
            inst.opname,
            inst.opcode,
            inst.optype,
            inst.inst_size,
            inst.arg,
            inst.argval,
            inst.argrepr,
            inst.has_arg,
            inst.offset,
            inst.starts_line,
            inst.is_jump_target,
            inst.has_extended_arg,
        )
