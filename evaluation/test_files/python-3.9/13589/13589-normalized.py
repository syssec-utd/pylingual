def _remove_extra_delims(expr, ldelim='(', rdelim=')', fcount=None):
    """
    Remove unnecessary delimiters (parenthesis, brackets, etc.).

    Internal function that can be recursed
    """
    if not expr.strip():
        return ''
    fcount = [0] if fcount is None else fcount
    tfuncs = _get_functions(expr, ldelim=ldelim, rdelim=rdelim)
    for fdict in reversed(tfuncs):
        fcount[0] += 1
        fdict['token'] = '__' + str(fcount[0])
        expr = expr[:fdict['start']] + fdict['token'] + expr[fdict['stop'] + 1:]
        fdict['expr'] = _remove_extra_delims(fdict['expr'], ldelim=ldelim, rdelim=rdelim, fcount=fcount)
    expr = _build_expr(_parse_expr(expr, ldelim=ldelim, rdelim=rdelim), ldelim=ldelim, rdelim=rdelim)
    for fdict in tfuncs:
        expr = expr.replace(fdict['token'], fdict['fname'] + ldelim + fdict['expr'] + rdelim)
    return expr