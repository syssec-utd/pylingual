from ..EditableBytecode import EditableBytecode


def remove_comprehension_get_iter(bytecode: EditableBytecode):
    # 3.13.1+ emits an extra GET_ITER right before FOR_ITER in comprehensions and generator expressions, 3.13.0 does not.
    # The magic number is the same, so drop every run of GET_ITERs directly before a FOR_ITER to compare both the same way.
    if bytecode.version != (3, 13):
        return
    to_remove = []
    for idx, inst in enumerate(bytecode.instructions):
        if inst.opname != "FOR_ITER":
            continue
        prev = idx - 1
        while prev >= 0 and bytecode.instructions[prev].opname == "GET_ITER":
            to_remove.append(bytecode.instructions[prev])
            prev -= 1
    bytecode.remove_instructions(to_remove)
