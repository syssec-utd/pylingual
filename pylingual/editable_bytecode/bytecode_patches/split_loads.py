from ..EditableBytecode import EditableBytecode
from ..Instruction import Inst


def split_loads(bytecode: EditableBytecode):
    double_load_fast = [(idx, inst) for idx, inst in enumerate(bytecode.instructions) if inst.opname == "LOAD_FAST_LOAD_FAST"]
    to_insert = dict()

    for idx, inst in double_load_fast:
        # LOAD_FAST_LOAD_FAST packs two local indices into one argument:
        # oparg = (val1_index << 4) | val2_index. Capture them before rewriting
        # the instruction so the two LOAD_FASTs load the correct locals.
        packed_arg = inst.arg if inst.arg is not None else 0
        arg1, arg2 = packed_arg >> 4, packed_arg & 0x0F

        # change load_fast_load_fast to load_fast
        val1, val2 = inst.argval
        inst.opname = "LOAD_FAST"
        inst.opcode = bytecode.opcode.LOAD_FAST
        inst.arg = arg1
        inst.argval = val1
        inst.argrepr = str(val1)

        # create 2nd load fast
        load_fast2 = Inst(
            bytecode=bytecode,
            opname="LOAD_FAST",
            opcode=bytecode.opcode.LOAD_FAST,
            optype="local",
            inst_size=2,
            arg=arg2,
            argval=val2,
            argrepr=str(val2),
            has_arg=True,
            offset=inst.offset + 2,
            starts_line=inst.starts_line,
            is_jump_target=False,
            has_extended_arg=False,
        )
        to_insert[idx + 1] = [load_fast2]

    bytecode.insert_insts(to_insert)
