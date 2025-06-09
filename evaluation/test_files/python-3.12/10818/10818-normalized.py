def isregex_expr(expr):
    """
    Returns ``True`` is the given expression value is a regular expression
    like string with prefix ``re/`` and suffix ``/``, otherwise ``False``.

    Arguments:
        expr (mixed): expression value to test.

    Returns:
        bool
    """
    if not isinstance(expr, str):
        return False
    return all([len(expr) > 3, expr.startswith('re/'), expr.endswith('/')])