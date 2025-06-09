def get_latex_maybe_optional_arg(s, pos, **parse_flags):
    """
    Attempts to parse an optional argument. Returns a tuple `(groupnode, pos, len)` if
    success, otherwise returns None.

    .. deprecated:: 1.0
       Please use :py:meth:`LatexWalker.get_latex_maybe_optional_arg()` instead.
    """
    return LatexWalker(s, **parse_flags).get_latex_maybe_optional_arg(pos=pos)