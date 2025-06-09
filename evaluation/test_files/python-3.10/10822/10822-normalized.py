def compare(expr, value, regex_expr=False):
    """
    Compares an string or regular expression againast a given value.

    Arguments:
        expr (str|regex): string or regular expression value to compare.
        value (str): value to compare against to.
        regex_expr (bool, optional): enables string based regex matching.

    Raises:
        AssertionError: in case of assertion error.

    Returns:
        bool
    """
    if expr == value:
        return True
    negate = False
    if isinstance(expr, str):
        negate = expr.startswith(NEGATE)
        expr = strip_negate(expr) if negate else expr
    try:
        test(expr, value, regex_expr=regex_expr)
    except Exception as err:
        if negate:
            return True
        else:
            raise err
    return True