def is_def_stmt(line, frame):
    """Return True if we are looking at a def statement"""
    return line and _re_def.match(line) and (op_at_frame(frame) == 'LOAD_CONST') and stmt_contains_opcode(frame.f_code, frame.f_lineno, 'MAKE_FUNCTION')