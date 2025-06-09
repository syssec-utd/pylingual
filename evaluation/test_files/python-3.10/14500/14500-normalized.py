def get_token(s, pos, brackets_are_chars=True, environments=True, **parse_flags):
    """
    Parse the next token in the stream.

    Returns a `LatexToken`. Raises `LatexWalkerEndOfStream` if end of stream reached.

    .. deprecated:: 1.0
       Please use :py:meth:`LatexWalker.get_token()` instead.
    """
    return LatexWalker(s, **parse_flags).get_token(pos=pos, brackets_are_chars=brackets_are_chars, environments=environments)